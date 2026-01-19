"""
Type normalization utilities for converting vendor-specific data types to
Spark/Delta canonical representations before seeding metadata tables.

Supported sources: ( Need to review this list , Other soruces will be added later)
    * AS400 / DB2 
    * SAP (ABAP extractors / CDS views)
    * Salesforce


Usage:
    normalize_type("AS400_DB2", "DECIMAL(15,2)") -> "decimal(15,2)"
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Pattern, Tuple


Rule = Tuple[Pattern[str], str]


def _rule(pattern: str, replacement: str) -> Rule:
    return re.compile(pattern, re.IGNORECASE), replacement


TYPE_RULES: Dict[str, List[Rule]] = {
    "DEFAULT": [
        _rule(r"^string$", "string"),
        _rule(r"^varchar(?:\(\d+\))?$", "string"),
        _rule(r"^nvarchar(?:\(\d+\))?$", "string"),
        _rule(r"^char(?:\(\d+\))?$", "string"),
        _rule(r"^nchar(?:\(\d+\))?$", "string"),
        _rule(r"^text$", "string"),
        _rule(r"^boolean$", "boolean"),
        _rule(r"^bit$", "boolean"),
        _rule(r"^tinyint$", "byte"),
        _rule(r"^smallint$", "smallint"),
        _rule(r"^int(?:eger)?$", "int"),
        _rule(r"^bigint$", "bigint"),
        _rule(r"^float$", "double"),
        _rule(r"^double$", "double"),
        _rule(r"^real$", "double"),
        _rule(r"^decimal\((\d+),\s*(\d+)\)$", r"decimal(\1,\2)"),
        _rule(r"^number\((\d+),\s*(\d+)\)$", r"decimal(\1,\2)"),
        _rule(r"^numeric\((\d+),\s*(\d+)\)$", r"decimal(\1,\2)"),
        _rule(r"^decimal$", "decimal(38,18)"),
        _rule(r"^numeric$", "decimal(38,18)"),
        _rule(r"^date$", "date"),
        _rule(r"^timestamp$", "timestamp"),
        _rule(r"^datetime$", "timestamp"),
        _rule(r"^time$", "string"),
        _rule(r"^binary$", "binary"),
    ]
}


TYPE_RULES["AS400_DB2"] = [
    _rule(r"^char\(\d+\)$", "string"),
    _rule(r"^varchar\(\d+\)$", "string"),
    _rule(r"^graphic\(\d+\)$", "string"),
    _rule(r"^vargraphic\(\d+\)$", "string"),
    _rule(r"^clob$", "string"),
    _rule(r"^blob$", "binary"),
    _rule(r"^smallint$", "smallint"),
    _rule(r"^integer$", "int"),
    _rule(r"^bigint$", "bigint"),
    _rule(r"^decimal\((\d+),\s*(\d+)\)$", r"decimal(\1,\2)"),
    _rule(r"^packed(?: decimal)?\((\d+),\s*(\d+)\)$", r"decimal(\1,\2)"),
    _rule(r"^zoned(?: decimal)?\((\d+),\s*(\d+)\)$", r"decimal(\1,\2)"),
    _rule(r"^double$", "double"),
    _rule(r"^real$", "double"),
    _rule(r"^date$", "date"),
    _rule(r"^time$", "string"),
    _rule(r"^timestamp$", "timestamp"),
]


TYPE_RULES["SAP"] = [
    _rule(r"^char\(\d+\)$", "string"),
    _rule(r"^unit$", "string"),
    _rule(r"^curr$", "decimal(18,2)"),
    _rule(r"^cuky$", "string"),
    _rule(r"^numc\(\d+\)$", "string"),
    _rule(r"^dec\((\d+),\s*(\d+)\)$", r"decimal(\1,\2)"),
    _rule(r"^dec$", "decimal(38,18)"),
    _rule(r"^int1$", "smallint"),
    _rule(r"^int2$", "int"),
    _rule(r"^int4$", "int"),
    _rule(r"^float$", "double"),
    _rule(r"^dats$", "date"),
    _rule(r"^tims$", "string"),
    _rule(r"^clnt$", "string"),
    _rule(r"^lang$", "string"),
    _rule(r"^rawstring$", "binary"),
]


TYPE_RULES["SALESFORCE"] = [
    _rule(r"^string$", "string"),
    _rule(r"^textarea$", "string"),
    _rule(r"^phone$", "string"),
    _rule(r"^url$", "string"),
    _rule(r"^email$", "string"),
    _rule(r"^picklist$", "string"),
    _rule(r"^multipicklist$", "string"),
    _rule(r"^encryptedstring$", "string"),
    _rule(r"^combobox$", "string"),
    _rule(r"^id$", "string"),
    _rule(r"^reference$", "string"),
    _rule(r"^boolean$", "boolean"),
    _rule(r"^currency$", "decimal(18,4)"),
    _rule(r"^percent$", "decimal(10,4)"),
    _rule(r"^double$", "double"),
    _rule(r"^int$", "int"),
    _rule(r"^long$", "bigint"),
    _rule(r"^date$", "date"),
    _rule(r"^datetime$", "timestamp"),
    _rule(r"^time$", "string"),
    _rule(r"^base64$", "binary"),
]


SYSTEM_ALIASES = {
    "AS400": "AS400_DB2",
    "DB2": "AS400_DB2",
    "IBM_DB2": "AS400_DB2",
    "SAP": "SAP",
    "SAP_HANA": "SAP",
    "SALESFORCE": "SALESFORCE",
    "SFDC": "SALESFORCE",
}


def normalize_type(source_system: str, raw_type: str, default: str = "string") -> str:
    """
    Convert a vendor-specific type definition into the Spark/Delta equivalent.

    Args:
        source_system: Logical source system or alias (e.g., "AS400_Db2").
        raw_type:      Type string exactly as supplied by the source metadata.
        default:       Fallback type if no rule matches.
    """
    if not raw_type:
        return default
    canonical_source = SYSTEM_ALIASES.get(source_system.upper(), source_system.upper())
    rules = TYPE_RULES.get(canonical_source, []) + TYPE_RULES["DEFAULT"]
    normalized = raw_type.strip()
    for pattern, replacement in rules:
        match = pattern.match(normalized)
        if not match:
            continue
        if pattern.groups:
            return match.expand(replacement).lower()
        return replacement.lower()
    return default


def normalize_types(source_system: str, raw_types: List[Optional[str]], default: str = "string") -> List[str]:
    """
    Apply normalize_type across a list for convenience.
    """
    return [normalize_type(source_system, raw_type or "", default=default) for raw_type in raw_types]

