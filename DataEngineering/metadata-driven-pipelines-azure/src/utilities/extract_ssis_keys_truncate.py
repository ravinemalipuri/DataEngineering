"""
SSIS utility: extract key usage and truncate-before-load behavior per package.

For each .dtsx in the supplied folder it captures:
    * Target table inferred for each destination component.
    * Key columns used to identify rows (when exposed in metadata/properties).
    * Whether the package truncates the same target table before loading.

Outputs:
    * Single CSV summarizing all destinations across the supplied packages (package file is a column).
    * Combined Excel workbook aggregating the same rows.
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import re
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Set
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

DESTINATION_CLASS_IDS = {
    "{E2568106-FB15-11d1-82C3-00A0C9138C37}",  # OLE DB Destination
    "{1640830E-3C90-4d1b-AC0D-F0A5C2BA5B1A}",  # SQL Server Destination
    "{334AA9C6-E4B6-4bde-88E4-13F37B28E2F0}",  # ADO.NET Destination
    "{8C0D815B-D5AE-47c9-83CC-36BCBD9EDC25}",  # ODBC Destination
    "{4ADA7EAA-136C-4215-8098-D7A7C27FC0D1}",  # OLE DB Destination (newer CLSID)
}

COLUMN_HEADERS = [
    "package_file",
    "component_name",
    "target_table",
    "key_columns",
    "truncate_before_load",
    "truncate_source",
    "truncate_detected_tables",
]

TRUNCATE_REGEX = re.compile(r"truncate\s+table\s+([^\s;]+)", re.IGNORECASE)


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def clean_path(path: str) -> str:
    trimmed = (path or "").strip().strip('\'"')
    if trimmed and trimmed[0] in {"'", '"'}:
        trimmed = trimmed[1:]
    if trimmed and trimmed[-1] in {"'", '"'}:
        trimmed = trimmed[:-1]
    return trimmed.strip()


def log_debug(verbose: bool, message: str) -> None:
    if verbose:
        print(f"[DEBUG] {message}")


def normalize_table_name(name: Optional[str]) -> str:
    """
    Normalize table names for comparison:
    - strip brackets/quotes
    - lower-case
    - drop schema if present (keep last identifier)
    """
    if not name:
        return ""
    cleaned = name.strip().strip("[]`\"")
    parts = [p.strip("[]`\"") for p in cleaned.split(".") if p]
    if not parts:
        return ""
    return parts[-1].lower()


def parse_properties(elem: ET.Element) -> Dict[str, str]:
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
                        meta = {
                            "name": ext.attrib.get("name"),
                            "dataType": ext.attrib.get("dataType"),
                            "length": ext.attrib.get("length"),
                            "precision": ext.attrib.get("precision"),
                            "scale": ext.attrib.get("scale"),
                        }
                        # Some components expose IsKey/KeyType flags as child properties.
                        for prop in ext:
                            if local_name(prop.tag) == "property" and prop.attrib.get("name"):
                                meta[prop.attrib["name"]] = prop.attrib.get("value") or (prop.text or "").strip()
                        info["external_metadata"][ref_id] = meta
            inputs.append(info)
    return inputs


def parse_components(root: ET.Element) -> Dict[str, Dict]:
    components: Dict[str, Dict] = {}
    for comp in root.iter():
        if local_name(comp.tag) != "component":
            continue
        ref_id = comp.attrib.get("refId")
        if not ref_id:
            continue
        component_info = {
            "ref_id": ref_id,
            "name": comp.attrib.get("name") or ref_id,
            "class_id": comp.attrib.get("componentClassID"),
            "properties": parse_properties(comp),
            "inputs": parse_inputs(comp),
        }
        components[ref_id] = component_info
    return components


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


def extract_key_columns(component: Dict) -> List[str]:
    keys: Set[str] = set()
    for input_block in component.get("inputs", []):
        external_meta = input_block.get("external_metadata", {})
        for column in input_block.get("columns", []):
            ref_id = column.get("externalMetadataColumnId")
            if not ref_id:
                continue
            metadata = external_meta.get(ref_id, {})
            if metadata.get("IsKey", "").lower() == "true" or metadata.get("KeyType"):
                keys.add(metadata.get("name") or column.get("name"))
    # Fallback to SQL text heuristics (MERGE / UPDATE). Parse ON/WHERE predicates for equality.
    sql_command = (component.get("properties") or {}).get("SqlCommand", "")
    if sql_command:
        for clause_pattern in (r"\bON\b\s+([^;]+)", r"\bWHERE\b\s+([^;]+)"):
            for clause in re.findall(clause_pattern, sql_command, flags=re.IGNORECASE | re.MULTILINE):
                # Find column tokens on either side of '='
                for col in re.findall(r"(?:\b[\w\[\]]+\.)?([\w\[\]]+)\s*=", clause):
                    keys.add(col)
    return sorted(keys)


def collect_truncate_targets(root: ET.Element) -> Dict[str, str]:
    truncate_map: Dict[str, str] = {}
    for elem in root.iter():
        tag_name = local_name(elem.tag)
        # Existing execute SQL task properties
        if tag_name == "executeSQLTask":
            props = parse_properties(elem)
            sql_text = props.get("SqlStatementSource") or props.get("SqlStatementSourceExpression") or ""
            if "truncate table" in sql_text.lower():
                match = TRUNCATE_REGEX.search(sql_text)
                if match:
                    normalized = normalize_table_name(match.group(1))
                    truncate_map[normalized] = (
                        elem.attrib.get("refId")
                        or elem.attrib.get("name")
                        or elem.attrib.get("ObjectName")
                        or "ExecuteSQLTask"
                    )
            continue
        # Generic scan for SqlStatementSource attributes on any node (handles SqlTaskData)
        for attr, val in elem.attrib.items():
            if local_name(attr) in {"SqlStatementSource", "SqlStatementSourceExpression"}:
                sql_text = val or ""
                if "truncate table" not in sql_text.lower():
                    continue
                match = TRUNCATE_REGEX.search(sql_text)
                if not match:
                    continue
                normalized = normalize_table_name(match.group(1))
                source_name = (
                    elem.attrib.get("refId")
                    or elem.attrib.get("ObjectName")
                    or elem.attrib.get("name")
                    or tag_name
                )
                truncate_map[normalized] = source_name
    return truncate_map


def discover_packages(folder: Path, file_names: Optional[List[str]]) -> List[Path]:
    candidates = sorted(folder.glob("*.dtsx"))
    if not file_names:
        return candidates
    normalized = set(
        name.lower() if name.lower().endswith(".dtsx") else f"{name.lower()}.dtsx" for name in file_names
    )
    return [path for path in candidates if path.name.lower() in normalized]


def list_and_download_adls(source: str, work_dir: Path, file_names: Optional[List[str]], verbose: bool) -> List[Path]:
    if mssparkutils is None:
        raise RuntimeError("mssparkutils is required for abfss paths in this environment.")

    raw = clean_path(source).rstrip("/")
    pattern = None
    if "*" in raw:
        raw, pattern = raw.rsplit("/", 1)
    list_base = raw.rstrip("/")
    list_path = f"{list_base}/"

    desired = set(
        name.lower() if name.lower().endswith(".dtsx") else f"{name.lower()}.dtsx"
        for name in (file_names or [])
    ) or None
    downloaded: List[Path] = []

    if not mssparkutils.fs.exists(list_path):
        raise FileNotFoundError(f"Input path not found: {list_path}")
    log_debug(verbose, f"mssparkutils.fs.ls path={list_path} pattern={pattern} desired={desired}")
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
        log_debug(verbose, f"Downloaded {len(downloaded)} packages from {list_path}")
        return downloaded

    if SparkSession is None:
        raise RuntimeError("SparkSession not available to enumerate ADLS files.")
    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    glob_path = f"{list_base}/{pattern or '*'}"
    log_debug(verbose, f"Spark binaryFile load glob={glob_path}")
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
    log_debug(verbose, f"Spark binaryFile downloaded files={len(downloaded)} from glob={glob_path}")
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


def copy_outputs_local(output_dir: Path, dest_dir: Path, verbose: bool) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for produced in output_dir.glob("*"):
        target = dest_dir / produced.name
        if target.exists():
            target.unlink()
        shutil.copy2(produced, target)
        if verbose:
            print(f"[OK] Wrote {target}")


def write_csv(rows: List[Dict[str, Optional[str]]], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMN_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract SSIS key usage + truncate behavior for each Data Flow destination. "
            "Defaults to ADLS paths so no arguments are required."
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
        help="Optional subset of packages to parse (with or without .dtsx).",
    )
    parser.add_argument(
        "--combined-excel",
        help="Optional filename for combined workbook (default: <input-folder-name>_keys_truncate.xlsx).",
    )
    parser.add_argument(
        "--combined-csv",
        help="Optional filename for combined CSV (default: <input-folder-name>_keys_truncate.csv).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging for path resolution and transfers.",
    )
    args, _unknown = parser.parse_known_args(argv)
    return args


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    input_path = clean_path(args.input_path or DEFAULT_INPUT_ADLS)
    output_path = clean_path(args.output_path or DEFAULT_OUTPUT_ADLS)

    work_dir = Path(tempfile.mkdtemp(prefix="ssis_keys_truncate_"))
    local_input_dir = work_dir / "packages"
    local_output_dir = work_dir / "outputs"
    local_input_dir.mkdir(parents=True, exist_ok=True)
    local_output_dir.mkdir(parents=True, exist_ok=True)

    # If input is abfss/https, use mssparkutils; otherwise treat as local path/file/glob.
    if input_path.lower().startswith(("abfs://", "abfss://")):
        packages = list_and_download_adls(input_path, local_input_dir, args.file_names, args.verbose)
    else:
        path_obj = Path(input_path)
        packages = []
        if path_obj.is_file() and path_obj.suffix.lower() == ".dtsx":
            target = local_input_dir / path_obj.name
            shutil.copy2(path_obj, target)
            packages.append(target)
        elif path_obj.is_dir():
            candidates = sorted(path_obj.glob("*.dtsx"))
            desired = (
                set(
                    name.lower() if name.lower().endswith(".dtsx") else f"{name.lower()}.dtsx"
                    for name in (args.file_names or [])
                )
                if args.file_names
                else None
            )
            for cand in candidates:
                if desired and cand.name.lower() not in desired:
                    continue
                target = local_input_dir / cand.name
                shutil.copy2(cand, target)
                packages.append(target)
        else:
            raise FileNotFoundError(f"Input path not found or not a .dtsx file/dir: {input_path}")

    if not packages:
        if args.file_names:
            raise FileNotFoundError(
                f"No matching .dtsx files found at {input_path} for: {', '.join(args.file_names)}"
            )
        raise FileNotFoundError(f"No .dtsx files found at: {input_path}")

    combined_rows: List[Dict[str, Optional[str]]] = []
    for package_path in packages:
        tree = ET.parse(package_path)
        root = tree.getroot()
        truncate_map = collect_truncate_targets(root)
        components = parse_components(root)
        for component in components.values():
            if component.get("class_id") not in DESTINATION_CLASS_IDS:
                continue
            target_table = infer_table_name(component.get("properties", {})) or component.get("name")
            keys = extract_key_columns(component)
            normalized_target = normalize_table_name(target_table)
            # Match truncates by normalized name; if schemas differ, also match on base table name.
            truncate_sources = []
            base_target = normalized_target.split(".")[-1] if "." in normalized_target else normalized_target
            for tname, source in truncate_map.items():
                if tname == normalized_target:
                    truncate_sources.append(source)
                    continue
                base_t = tname.split(".")[-1] if "." in tname else tname
                if base_t and base_t == base_target:
                    truncate_sources.append(source)
            combined_rows.append(
                {
                    "package_file": package_path.name,
                    "component_name": component.get("name"),
                    "target_table": target_table,
                    "key_columns": ";".join(keys),
                    "truncate_before_load": "true" if truncate_sources else "false",
                    "truncate_source": ";".join(truncate_sources),
                    "truncate_detected_tables": ";".join(sorted(truncate_map.keys())),
                }
            )

    # Write combined CSV locally
    input_base = Path(input_path.rstrip("/").rstrip("\\"))
    base_name = input_base.name
    if "*" in base_name or not base_name:
        base_name = input_base.parent.name or "lineage"

    combined_csv = (
        Path(args.combined_csv).expanduser().resolve()
        if args.combined_csv
        else local_output_dir / f"{base_name}_keys_truncate.csv"
    )
    write_csv(combined_rows, combined_csv)
    print(f"[OK] Combined CSV written to {combined_csv} ({len(combined_rows)} rows)")

    # Write combined Excel locally (always create/overwrite)
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("pandas is required to build the combined Excel workbook") from exc

    combined_excel = (
        Path(args.combined_excel).expanduser().resolve()
        if args.combined_excel
        else local_output_dir / "SSISPackages_keys.xlsx"
    )
    pd.DataFrame(combined_rows, columns=COLUMN_HEADERS).to_excel(
        combined_excel, index=False, sheet_name="keys_truncate"
    )
    print(f"[OK] Combined Excel written to {combined_excel} ({len(combined_rows)} rows)")

    # Upload outputs back to destination
    if output_path.lower().startswith(("abfs://", "abfss://")):
        upload_outputs_adls(local_output_dir, output_path, args.verbose)
    else:
        copy_outputs_local(local_output_dir, Path(output_path).expanduser().resolve(), args.verbose)


if __name__ == "__main__":
    main()

