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
from pathlib import Path
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET

DEFAULT_INPUT_ONEDRIVE = Path.home() / "OneDrive" / "Downloads"
DEFAULT_OUTPUT_ONEDRIVE = Path.home() / "OneDrive" / "Documents" / "LineageOutputs"

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract SSIS mappings with lineage + transformation metadata. "
            "Processes every .dtsx in a folder (optionally filtered)."
        )
    )
    parser.add_argument(
        "--onedrive-folder",
        default=str(DEFAULT_INPUT_ONEDRIVE),
        help=(
            "OneDrive directory containing SSIS .dtsx files "
            f"(default: {DEFAULT_INPUT_ONEDRIVE})"
        ),
    )
    parser.add_argument(
        "--output-onedrive-folder",
        default=str(DEFAULT_OUTPUT_ONEDRIVE),
        help=(
            "OneDrive directory for CSV/Excel outputs "
            f"(default: {DEFAULT_OUTPUT_ONEDRIVE})"
        ),
    )
    parser.add_argument(
        "--file-names",
        nargs="+",
        help="Optional list of specific file names to process (with or without .dtsx)",
    )
    parser.add_argument(
        "--output-dir",
        help="Destination directory for CSV outputs (defaults to the OneDrive folder)",
    )
    parser.add_argument(
        "--combined-excel",
        help="Optional Excel filename for aggregated lineage results. Defaults to '<folder name>_lineage.xlsx' in the same folder.",
    )
    return parser.parse_args()


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


def discover_packages(folder: Path, file_names: Optional[List[str]]) -> List[Path]:
    candidates = sorted(folder.glob("*.dtsx"))
    if not file_names:
        return candidates
    targets = set(normalize_filenames(file_names))
    return [path for path in candidates if path.name.lower() in targets]


def main() -> None:
    args = parse_args()
    folder = Path(args.onedrive_folder).expanduser().resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Package folder not found: {folder}")

    output_dir = (
        Path(args.output_onedrive_folder).expanduser().resolve()
        if args.output_onedrive_folder
        else Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else DEFAULT_OUTPUT_ONEDRIVE.expanduser().resolve()
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    packages = discover_packages(folder, args.file_names)
    if not packages:
        if args.file_names:
            raise FileNotFoundError(
                f"No matching .dtsx files found in {folder} for: {', '.join(args.file_names)}"
            )
        raise FileNotFoundError(f"No .dtsx files found in folder: {folder}")

    all_rows: List[Dict[str, Optional[str]]] = []
    for package_path in packages:
        rows = extract_mappings_with_lineage(package_path)
        all_rows.extend(rows)
        output_file = output_dir / f"{package_path.stem}_lineage.csv"
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

    combined_filename = (
        Path(args.combined_excel).expanduser().resolve()
        if args.combined_excel
        else output_dir / f"{folder.name}_lineage.xlsx"
    )
    df = pd.DataFrame(all_rows)
    df.to_excel(combined_filename, index=False, sheet_name="lineage")
    print(f"[OK] Combined Excel written to {combined_filename} ({len(df)} rows)")


if __name__ == "__main__":
    main()

