from __future__ import annotations

from typing import Any, Mapping

import tomlkit

from pdm.project.toml_file import TOMLBase

GENERATED_COMMENTS = [
    "This file is @generated by PDM.",
    "It is not intended for manual editing.",
]


class Lockfile(TOMLBase):
    spec_version = "4.2"

    @property
    def hash(self) -> str:
        return self._data.get("metadata", {}).get("content_hash", "")

    @property
    def file_version(self) -> str:
        return self._data.get("metadata", {}).get("lock_version", "")

    @property
    def groups(self) -> list[str] | None:
        return self._data.get("metadata", {}).get("groups")

    def set_data(self, data: Mapping[str, Any]) -> None:
        self._data = tomlkit.document()
        for line in GENERATED_COMMENTS:
            self._data.append(None, tomlkit.comment(line))
        self._data.update(data)

    def write(self, show_message: bool = True) -> None:
        super().write()
        if show_message:
            self.ui.echo(f"Changes are written to [success]{self._path.name}[/].")

    def __getitem__(self, key: str) -> dict:
        return self._data[key]