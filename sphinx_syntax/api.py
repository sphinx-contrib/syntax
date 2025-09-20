import pathlib
import threading
import typing as _t
from dataclasses import dataclass


@dataclass
class Object:
    """
    Description of an object (grammar or rule) extracted from a grammar source file.

    """

    name: str
    """
    Unique name for this object, used for cross-referencing. Can contain any string,
    but its preferable for names to be alphanumeric identifiers. Grammar names
    can't contain dots.

    """

    human_readable_name: str | None = None
    """
    Human-readable name, overrides :attr:`Object.name` when rendering.

    """

    description: str | list[tuple[str, int]] | None = None
    """
    Docstring that will be rendered as object's description. Can be either a string
    or a list of pairs containing line numbers and line contents.

    """

    file: pathlib.Path | None = None
    """
    Where this object was declared. Used for sorting objects by source.

    """

    line: int | None = None
    """
    Where this object was declared. Used for sorting objects by source.

    """


@dataclass
class Section:
    """
    Section comment.

    """

    description: str | list[tuple[str, int]] | None = None
    """
    Docstring that will be rendered as section's description. Can be either a string
    or a list of pairs containing line numbers and line contents.

    """

    file: pathlib.Path | None = None
    """
    Where this section was declared. Used for sorting objects by source.

    """

    line: int | None = None
    """
    Where this section was declared. Used for sorting objects by source.

    """


@dataclass
class Grammar(Object):
    """
    Description of a grammar.

    """

    rules: list["Rule | Section"] | None = None
    """
    List of rules found in this grammar.

    """

    imports: list[str] | None = None
    """
    List of names of imported grammars.

    """

    dependencies: set[pathlib.Path] | None = None
    """
    List of files that affect definition of this object. Used to rebuild
    documentation on changes.

    """


@dataclass
class Rule(Object):
    """
    Description of a production rule.

    """

    is_root: bool = False
    """
    Indicates that this is the starting production in a grammar.

    """

    diagram: _t.Any | None = None
    """
    Data for rendering rule's diagram.

    """

    render_diagram: bool | None = None
    """
    Whether to render a diagram for this rule. If ``None``, a project-wide setting
    will be used.

    """


class AutodocProvider:
    """
    Base interface for extracting data from a grammar source files.

    """

    supported_extensions: set[str]
    """
    Set of file extensions that correspond to this provider's syntax.

    """

    def can_handle(self, path: pathlib.Path) -> bool:
        """
        Check whether this provider can parse the given diagram file.

        By default, checks file extension against
        :attr:`AutodocProvider.supported_extensions`.

        """

        return path.suffix in self.supported_extensions

    def handle(self, path: pathlib.Path) -> Grammar:
        """
        Main customization point: handle the given file and return a grammar
        defined within.

        """

        raise NotImplementedError()


_KNOWN_PROVIDERS = []
_KNOWN_PROVIDERS_LOCK = threading.Lock()


def register_provider(provider: AutodocProvider):
    with _KNOWN_PROVIDERS_LOCK:
        _KNOWN_PROVIDERS.append(provider)
