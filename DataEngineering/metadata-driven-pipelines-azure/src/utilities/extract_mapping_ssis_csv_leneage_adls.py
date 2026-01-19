"""
Enhanced SSIS mapping extractor that captures lineage + transformation metadata.

For every .dtsx in a folder (optionally filtered), the script emits a CSV with:
    * Package file name (first column) for downstream traceability
    * Source column/table info inferred from upstream component metadata
    * Target column/table info from destination metadata
    * Component responsible for the final transformation + its expression text

Note: SSIS lineage metadata does not always expose the full multi-hop chain.
This script surfaces the immediate upstream component for each destination
column plus any expression defined on that component's output column. Complex
script components or multi-column expressions are captured verbatim when SSIS
stores them in the package XML.
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import tempfile
from pathlib import Path
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET

try:
    from notebookutils import mssparkutils  # type: ignore
except ImportError:
    mssparkutils = None

try:
    from pyspark.sql import SparkSession  # type: ignore
except ImportError:
    SparkSession = None  # type: ignore

DEFAULT_INPUT_ADLS = "abfss://xyz@abc.dfs.core.windows.net/bronze/sources/SSISPackages/*.dtsx"
DEFAULT_OUTPUT_ADLS = "abfss://xyz@abc.dfs.core.windows.net/bronze/sources/SSISPackages/extract/"

COLUMN_HEADERS = [
    "package_file",
    "source_table",
    "source_column",
    "source_data_type",
    "target_table",
    "target_column",
    "target_data_type",
    "alias",
    "transformation_component",
    "transformation_expression",
]


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def extract_properties(elem: ET.Element) -> Dict[str, str]:
    props: Dict[str, str] = {}
    for child in elem:
        if local_name(child.tag) != "properties":
            continue
        for prop in child:
            if local_name(prop.tag) != "property":
                continue
            name = prop.attrib.get("name")
            if not name:
                continue
            value = prop.attrib.get("value")
            if value is None:
                value = (prop.text or "").strip()
            props[name] = value
    return props


def parse_inputs(component_elem: ET.Element) -> List[Dict]:
    inputs: List[Dict] = []
    for child in component_elem:
        if local_name(child.tag) != "inputs":
            continue
        for input_elem in child:
            if local_name(input_elem.tag) != "input":
                continue
            info = {
                "ref_id": input_elem.attrib.get("refId"),
                "name": input_elem.attrib.get("name"),
                "columns": [],
                "external_metadata": {},
            }
            for input_child in input_elem:
                tag = local_name(input_child.tag)
                if tag == "inputColumns":
                    for col in input_child:
                        if local_name(col.tag) != "inputColumn":
                            continue
                        info["columns"].append(
                            {
                                "ref_id": col.attrib.get("refId"),
                                "name": col.attrib.get("name"),
                                "lineageId": col.attrib.get("lineageId")
                                or col.attrib.get("lineageID"),
                                "externalMetadataColumnId": col.attrib.get("externalMetadataColumnId")
                                or col.attrib.get("externalMetadataColumnID"),
                            }
                        )
                elif tag == "externalMetadataColumns":
                    for ext in input_child:
                        if local_name(ext.tag) != "externalMetadataColumn":
                            continue
                        ref_id = ext.attrib.get("refId")
                        if not ref_id:
                            continue
                        info["external_metadata"][ref_id] = {
                            "name": ext.attrib.get("name"),
                            "dataType": ext.attrib.get("dataType"),
                            "length": ext.attrib.get("length"),
                            "precision": ext.attrib.get("precision"),
                            "scale": ext.attrib.get("scale"),
                        }
            inputs.append(info)
    return inputs


def parse_outputs(component_elem: ET.Element) -> List[Dict]:
    outputs: List[Dict] = []
    for child in component_elem:
        if local_name(child.tag) != "outputs":
            continue
        for output_elem in child:
            if local_name(output_elem.tag) != "output":
                continue
            info = {
                "ref_id": output_elem.attrib.get("refId"),
                "name": output_elem.attrib.get("name"),
                "columns": [],
            }
            for output_child in output_elem:
                if local_name(output_child.tag) != "outputColumns":
                    continue
                for col in output_child:
                    if local_name(col.tag) != "outputColumn":
                        continue
                    column_info = {
                        "ref_id": col.attrib.get("refId"),
                        "name": col.attrib.get("name"),
                        "lineageId": col.attrib.get("lineageId") or col.attrib.get("lineageID"),
                        "dataType": col.attrib.get("dataType"),
                        "properties": extract_properties(col),
                    }
                    info["columns"].append(column_info)
            outputs.append(info)
    return outputs


def infer_table_name(properties: Dict[str, str]) -> Optional[str]:
    candidate_keys = [
        "OpenRowset",
        "OpenRowsetVariable",
        "SqlCommand",
        "SqlCommandVariable",
        "CommandTableName",
        "TableOrViewName",
        "ObjectName",
    ]
    for key in candidate_keys:
        value = properties.get(key)
        if value:
            return value
    return None


def collect_components(root: ET.Element) -> Dict[str, Dict]:
    components: Dict[str, Dict] = {}
    for comp in root.iter():
        if local_name(comp.tag) != "component":
            continue
        ref_id = comp.attrib.get("refId")
        if not ref_id:
            continue
        properties = extract_properties(comp)
        component_info = {
            "ref_id": ref_id,
            "name": comp.attrib.get("name") or ref_id,
            "class_id": comp.attrib.get("componentClassID"),
            "properties": properties,
            "inputs": parse_inputs(comp),
            "outputs": parse_outputs(comp),
            "table_name": infer_table_name(properties),
        }
        components[ref_id] = component_info
    return components


def build_lineage_lookup(components: Dict[str, Dict]) -> Dict[str, Dict]:
    lineage: Dict[str, Dict] = {}
    for comp in components.values():
        table_name = comp.get("table_name") or comp.get("name")
        for output in comp.get("outputs", []):
            for column in output.get("columns", []):
                lineage_id = column.get("lineageId")
                if not lineage_id:
                    continue
                lineage[lineage_id] = {
                    "component_ref": comp["ref_id"],
                    "component_name": comp["name"],
                    "component_class_id": comp.get("class_id"),
                    "table_name": table_name,
                    "column_name": column.get("name"),
                    "data_type": column.get("dataType"),
                    "expression": column.get("properties", {}).get("Expression")
                    or column.get("properties", {}).get("expression"),
                }
    return lineage


def extract_mappings_with_lineage(package_path: Path) -> List[Dict[str, Optional[str]]]:
    tree = ET.parse(package_path)
    root = tree.getroot()
    components = collect_components(root)
    lineage_lookup = build_lineage_lookup(components)

    rows: List[Dict[str, Optional[str]]] = []
    for comp in components.values():
        if not comp.get("inputs"):
            continue
        target_table = comp.get("table_name") or comp.get("name")
        for input_block in comp["inputs"]:
            external_meta = input_block.get("external_metadata", {})
            for column in input_block.get("columns", []):
                lineage_id = column.get("lineageId")
                if not lineage_id:
                    continue
                upstream = lineage_lookup.get(lineage_id)
                if not upstream:
                    continue
                target_meta = external_meta.get(column.get("externalMetadataColumnId"))
                rows.append(
                    {
                        "package_file": package_path.name,
                        "source_table": upstream.get("table_name"),
                        "source_column": upstream.get("column_name"),
                        "source_data_type": upstream.get("data_type"),
                        "target_table": target_table,
                        "target_column": (target_meta or {}).get("name") or column.get("name"),
                        "target_data_type": (target_meta or {}).get("dataType"),
                        "alias": column.get("name"),
                        "transformation_component": upstream.get("component_name"),
                        "transformation_expression": upstream.get("expression"),
                    }
                )
    return rows


def write_csv(rows: List[Dict[str, Optional[str]]], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMN_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract SSIS mappings with lineage + transformation metadata. "
            "Processes every .dtsx in a folder (optionally filtered). "
            "Defaults read from ADLS paths; users need not pass arguments."
        )
    )
    parser.add_argument(
        "--input-path",
        default=DEFAULT_INPUT_ADLS,
        help=f"Input ADLS folder or glob for .dtsx files (default: {DEFAULT_INPUT_ADLS})",
    )
    parser.add_argument(
        "--output-path",
        default=DEFAULT_OUTPUT_ADLS,
        help=f"Output ADLS folder for CSV/Excel (default: {DEFAULT_OUTPUT_ADLS})",
    )
    parser.add_argument(
        "--file-names",
        nargs="+",
        help="Optional list of specific file names to process (with or without .dtsx)",
    )
    parser.add_argument(
        "--combined-excel",
        help="Optional Excel filename for aggregated lineage results. Defaults to '<input-folder-name>_lineage.xlsx' in the output path.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging for path resolution and transfers.",
    )
    args, _unknown = parser.parse_known_args(argv)
    return args


def normalize_filenames(file_names: List[str]) -> List[str]:
    normalized = []
    for name in file_names:
        candidate = name.strip()
        if not candidate:
            continue
        if not candidate.lower().endswith(".dtsx"):
            candidate = f"{candidate}.dtsx"
        normalized.append(candidate.lower())
    return normalized


def clean_path(path: str) -> str:
    trimmed = (path or "").strip().strip('\'"')
    if trimmed and trimmed[0] in {"'", '"'}:
        trimmed = trimmed[1:]
    if trimmed and trimmed[-1] in {"'", '"'}:
        trimmed = trimmed[:-1]
    return trimmed.strip()


def discover_packages(folder: Path, file_names: Optional[List[str]]) -> List[Path]:
    candidates = sorted(folder.glob("*.dtsx"))
    if not file_names:
        return candidates
    targets = set(normalize_filenames(file_names))
    return [path for path in candidates if path.name.lower() in targets]


def list_and_download_adls(source: str, work_dir: Path, file_names: Optional[List[str]], verbose: bool) -> List[Path]:
    if mssparkutils is None:
        raise RuntimeError("mssparkutils is required for abfss paths in this environment.")

    raw = clean_path(source).rstrip("/")
    pattern = None
    if "*" in raw:
        raw, pattern = raw.rsplit("/", 1)
    list_base = raw.rstrip("/")
    list_path = f"{list_base}/"

    desired = set(normalize_filenames(file_names)) if file_names else None
    downloaded: List[Path] = []

    # Fast path: mssparkutils ls/cp
    if not mssparkutils.fs.exists(list_path):
        raise FileNotFoundError(f"Input path not found: {list_path}")
    for entry in mssparkutils.fs.ls(list_path):
        name_only = Path(entry.name).name
        if pattern and not fnmatch.fnmatch(name_only, pattern):
            continue
        if not name_only.lower().endswith(".dtsx"):
            continue
        if desired and name_only.lower() not in desired:
            continue
        local_path = work_dir / name_only
        local_path.parent.mkdir(parents=True, exist_ok=True)
        mssparkutils.fs.cp(entry.path, local_path.as_uri(), True)
        downloaded.append(local_path)
    if downloaded:
        if verbose:
            print(f"[DEBUG] Downloaded {len(downloaded)} packages from {list_path}")
        return downloaded

    # Fallback: Spark binaryFile enumeration (handles glob)
    if SparkSession is None:
        raise RuntimeError("SparkSession not available to enumerate ADLS files.")
    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    glob_path = f"{list_base}/{pattern or '*'}"
    if verbose:
        print(f"[DEBUG] Spark binaryFile load glob={glob_path}")
    df = spark.read.format("binaryFile").load(glob_path)
    for row in df.collect():
        remote_path = row.path
        name_only = Path(remote_path).name
        if not name_only.lower().endswith(".dtsx"):
            continue
        if pattern and not fnmatch.fnmatch(name_only, pattern):
            continue
        if desired and name_only.lower() not in desired:
            continue
        local_path = work_dir / name_only
        local_path.parent.mkdir(parents=True, exist_ok=True)
        content = getattr(row, "content", None)
        if content is None:
            mssparkutils.fs.cp(remote_path, local_path.as_uri(), True)
        else:
            with local_path.open("wb") as handle:
                handle.write(bytes(content))
        downloaded.append(local_path)
    if verbose:
        print(f"[DEBUG] Spark binaryFile downloaded files={len(downloaded)} from glob={glob_path}")
    return downloaded


def upload_outputs_adls(output_dir: Path, dest: str, verbose: bool) -> None:
    if mssparkutils is None:
        raise RuntimeError("mssparkutils is required to write to abfss paths.")
    dest_base = clean_path(dest).rstrip("/")
    for produced in output_dir.glob("*"):
        remote_path = f"{dest_base}/{produced.name}"
        mssparkutils.fs.cp(produced.as_uri(), remote_path, True)
        if verbose:
            print(f"[OK] Uploaded {produced.name} -> {remote_path}")


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    input_path = clean_path(args.input_path or DEFAULT_INPUT_ADLS)
    output_path = clean_path(args.output_path or DEFAULT_OUTPUT_ADLS)

    work_dir = Path(tempfile.mkdtemp(prefix="ssis_lineage_"))
    local_input_dir = work_dir / "packages"
    local_output_dir = work_dir / "outputs"
    local_input_dir.mkdir(parents=True, exist_ok=True)
    local_output_dir.mkdir(parents=True, exist_ok=True)

    # Download packages from ADLS (abfss) into local workspace
    packages = list_and_download_adls(input_path, local_input_dir, args.file_names, args.verbose)
    if not packages:
        if args.file_names:
            raise FileNotFoundError(
                f"No matching .dtsx files found at {input_path} for: {', '.join(args.file_names)}"
            )
        raise FileNotFoundError(f"No .dtsx files found at: {input_path}")

    all_rows: List[Dict[str, Optional[str]]] = []
    for package_path in packages:
        rows = extract_mappings_with_lineage(package_path)
        all_rows.extend(rows)
        output_file = local_output_dir / f"{package_path.stem}_lineage.csv"
        if not rows:
            print(f"[WARN] No lineage rows detected in {package_path.name}; writing empty CSV.")
        write_csv(rows, output_file)
        print(f"[OK] {package_path.name} -> {output_file} ({len(rows)} rows)")

    if not all_rows:
        print("No lineage rows found across all packages; skipping combined Excel.")
        return

    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("pandas is required to build the combined Excel workbook") from exc

    if args.combined_excel:
        combined_filename = Path(args.combined_excel).expanduser().resolve()
    else:
        # Derive a stable base name even when the input path includes globs like "*.dtsx"
        input_path_clean = input_path.rstrip("/").rstrip("\\")
        base_candidate = Path(input_path_clean).name
        if "*" in base_candidate or not base_candidate:
            base_candidate = Path(input_path_clean).parent.name or "lineage"
        combined_filename = local_output_dir / f"{base_candidate}_lineage.xlsx"
    df = pd.DataFrame(all_rows)
    df.to_excel(combined_filename, index=False, sheet_name="lineage")
    print(f"[OK] Combined Excel written to {combined_filename} ({len(df)} rows)")

    # Upload outputs back to ADLS
    upload_outputs_adls(local_output_dir, output_path, args.verbose)


if __name__ == "__main__":
    main()

