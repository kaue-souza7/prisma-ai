"""Utilitário de formatação dos textos editoriais versionados.

Os corpos de conteúdo usam Markdown e são escritos em blocos indentados nos
seed files. `md()` remove a indentação comum, junta linhas de continuação e
preserva a estrutura de parágrafos, listas e títulos.
"""
import re
from textwrap import dedent

_LIST_ITEM = re.compile(r"^(?:[-*]|\d+\.)\s+")


def md(text: str) -> str:
    normalized = dedent(text).strip()
    lines: list[str] = []

    for raw_line in normalized.splitlines():
        line = raw_line.strip()
        is_continuation = bool(raw_line[:1].isspace())
        is_block_start = line.startswith("#") or bool(_LIST_ITEM.match(line))

        if (
            line
            and is_continuation
            and not is_block_start
            and lines
            and lines[-1]
        ):
            lines[-1] = f"{lines[-1]} {line}"
        else:
            lines.append(line)

    return "\n".join(lines)
