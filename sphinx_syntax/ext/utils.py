import pathlib
import re
import textwrap
import typing as _t
from dataclasses import dataclass

import antlr4
import sphinx.util.logging
from antlr4.error.ErrorListener import ErrorListener

from sphinx_syntax.model import Model, Position, RuleContent

__all__ = [
    "DocInfo",
    "load_docs",
]

_logger = sphinx.util.logging.getLogger(__name__)


_CMD_RE = re.compile(
    r"""
    //@\s*doc\s*:\s*(?P<cmd>[a-zA-Z0-9_-]+)\s*(?P<ctx>.*)
    """,
    re.UNICODE | re.VERBOSE,
)


class LoggingErrorListener(ErrorListener):
    def __init__(self, path: pathlib.Path | None, offset: int):
        self._path = path
        self._offset = offset

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        _logger.error(
            msg,
            location=f"{self._path or "<in-memory>"}:{line + self._offset}",
            type="sphinx_syntax",
        )


@dataclass
class DocInfo:
    importance: int
    is_inline: bool
    is_nodoc: bool
    is_no_diagram: bool
    keep_diagram_recursive: bool
    css_class: str | None
    name: str | None
    documentation: list[tuple[int, str]]
    content: RuleContent | None


def load_docs(
    model: Model,
    offset: int,
    tokens: _t.Iterable[antlr4.Token],
    allow_cmd: bool = True,
):
    is_nodoc = False
    is_inline = False
    is_no_diagram = False
    keep_diagram_recursive = False
    css_class = None
    importance = 1
    name = None
    docs: list[tuple[int, str]] = []
    content = None

    for token in tokens:
        text: str = token.text
        position = Position(model.get_path(), token.line + offset)
        if text.startswith("//@"):
            match = _CMD_RE.match(text)

            if match is None:
                _logger.error(
                    f"invalid command {text!r}",
                    location=str(position),
                    type="sphinx_syntax",
                )
                continue

            if not allow_cmd:
                _logger.error(
                    f"commands not allowed here",
                    location=str(position),
                    type="sphinx_syntax",
                )
                continue

            cmd = match["cmd"]

            if cmd in ["nodoc", "no-doc"]:
                is_nodoc = True
            elif cmd == "inline":
                is_inline = True
            elif cmd in ["nodiagram", "no-diagram"]:
                is_no_diagram = True
            elif cmd == "keep-diagram-recursive":
                keep_diagram_recursive = True
            elif cmd == "unimportant":
                importance = 0
            elif cmd == "importance":
                try:
                    val = int(match["ctx"].strip())
                except ValueError:
                    _logger.error(
                        f"importance requires an integer argument",
                        location=str(position),
                        type="sphinx_syntax",
                    )
                    continue
                if val < 0:
                    _logger.error(
                        f"importance should not be negative",
                        location=str(position),
                        type="sphinx_syntax",
                    )
                importance = val
            elif cmd == "name":
                name = match["ctx"].strip()
                if not name:
                    _logger.error(
                        f"name command requires an argument",
                        location=str(position),
                        type="sphinx_syntax",
                    )
                    continue
            elif cmd == "content":
                content = _parse_content(match["ctx"].strip(), position)
            elif cmd == "css-class":
                css_class = match["ctx"].strip()
                if not name:
                    _logger.error(
                        f"css-class command requires an argument",
                        location=str(position),
                        type="sphinx_syntax",
                    )
                    continue
            else:
                _logger.error(
                    f"unknown command {cmd!r}",
                    location=str(position),
                    type="sphinx_syntax",
                )

            if (
                cmd not in ["name", "css-class", "importance", "content"]
                and match["ctx"]
            ):
                _logger.warning(
                    f"argument for {cmd!r} command is ignored",
                    location=str(position),
                    type="sphinx_syntax",
                )
        else:
            documentation_lines: list[str] = []

            lines = text.splitlines()

            if len(lines) == 1:
                documentation_lines.append(lines[0][3:-2].strip())
            else:
                first_line = lines[0]
                lines = lines[1:]

                first_line = first_line[3:].strip()
                documentation_lines.append(first_line)

                lines[-1] = lines[-1][:-2].rstrip()

                if not lines[-1].lstrip():
                    lines.pop()

                if all(line.lstrip().startswith("*") for line in lines):
                    lines = [line.lstrip()[1:] for line in lines]

                text = textwrap.dedent("\n".join(lines))

                documentation_lines.extend(text.splitlines())

            docs.extend(
                (position.line + i, line) for i, line in enumerate(documentation_lines)
            )

    return DocInfo(
        importance=importance,
        is_inline=is_inline,
        is_nodoc=is_nodoc,
        is_no_diagram=is_no_diagram,
        keep_diagram_recursive=keep_diagram_recursive,
        css_class=css_class,
        name=name,
        documentation=docs,
        content=content,
    )


def _parse_content(content_str: str, position: Position) -> RuleContent | None:
    from sphinx_syntax.ext.antlr4 import PROVIDER

    model = PROVIDER.from_text(
        f"grammar X; ROOT : {content_str} ;",
        position.file,
        offset=position.line - 1,
    )
    tree = model.lookup("ROOT")
    if tree is not None:
        return tree.content
    else:
        return None
