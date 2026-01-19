"""
Config loader + helpers for compute selection and path templates.
"""

from __future__ import annotations

import yaml
from typing import Dict, Optional


class ConfigLoader:
    """Loads YAML config and exposes helper getters."""

    def __init__(self, path: str):
        with open(path, "r", encoding="utf-8") as handle:
            self._cfg = yaml.safe_load(handle)

    def fabric(self) -> Dict:
        return self._cfg.get("fabric", {})

    def metadata_store(self) -> Dict:
        return self._cfg.get("metadata_store", {})

    def storage_paths(self) -> Dict:
        return self._cfg.get("storage_paths", {})

    def sources(self) -> Dict:
        return self._cfg.get("sources", {})

    def notifications(self) -> Dict:
        return self._cfg.get("notifications", {})

    def observability(self) -> Dict:
        return self._cfg.get("observability", {})


class ComputeResolver:
    """Allows devs to pick the Fabric compute engine at runtime."""

    def __init__(self, config: Dict):
        self.config = config

    def resolve(self, override: Optional[str]) -> Dict:
        profiles = self.config.get("compute_profiles", {})
        default_choice = self.config.get("default_compute")
        choice = override or default_choice
        if not choice:
            raise ValueError("No compute choice supplied and no default configured.")
        if choice not in profiles:
            raise ValueError(f"Compute profile '{choice}' is not defined in config.")
        profile = profiles[choice]
        return {"name": choice, "profile": profile}


class PathBuilder:
    """Central place for parameterised file/table names."""

    def __init__(self, config: Dict):
        self.config = config

    def _normalise(self, value: str) -> str:
        return value.lower().replace(".", "_")

    def landing_path(self, source_cfg, run_ctx: Dict) -> str:
        return self.config["landing_template"].format(
            root=self.config["root"],
            source_system=self._normalise(source_cfg.source_system),
            source_object=self._normalise(source_cfg.source_object_name),
            ingest_dt=run_ctx["ingest_dt"],
            run_id=run_ctx["run_id"],
        )

    def bronze_table(self, source_cfg, run_ctx: Dict) -> str:
        return self.config["bronze_table_template"].format(
            catalog=run_ctx.get("catalog", "lakehouse"),
            database=run_ctx.get("database", "bronze"),
            source_system=self._normalise(source_cfg.source_system),
            source_object=self._normalise(source_cfg.source_object_name),
        )

    def quarantine_path(self, source_cfg, run_ctx: Dict) -> str:
        template = source_cfg.quarantine_path or self.config["quarantine_template"]
        return template.format(
            root=self.config["root"],
            source_system=self._normalise(source_cfg.source_system),
            source_object=self._normalise(source_cfg.source_object_name),
            run_id=run_ctx["run_id"],
        )








