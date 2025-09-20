from __future__ import annotations

import itertools
import typing as _t
from dataclasses import dataclass

import docutils.nodes
import sphinx.addnodes
import sphinx.builders
import sphinx.directives
import syntax_diagrams as rr
from docutils.parsers.rst import directives
from docutils.parsers.rst.states import RSTStateMachine
from sphinx.addnodes import pending_xref
from sphinx.builders import Builder
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.environment import BuildEnvironment
from sphinx.locale import _
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import make_id, make_refnode

logger = logging.getLogger("sphinx_syntax")


def _list(value: str | None):
    if value is None:
        return []
    if "," in value:
        return [v.strip() for v in value.split(",")]
    else:
        return value.split()


def _end_class(value: str | None):
    if value:
        value = directives.choice(value.lower(), ["simple", "complex"])
        return rr.EndClass(value.upper())
    else:
        return None


def _arrow_style(value: str | None):
    if value:
        value = directives.choice(
            value.lower(),
            ["none", "triangle", "stealth", "barb", "harpoon", "harpoon_up"],
        )
        return rr.ArrowStyle(value.upper())
    else:
        return None


def _int(value: str | None):
    if value is None:
        raise ValueError("value is required")
    return int(value)


def _non_negative_int(value: str | None):
    result = _int(value)
    if result < 0:
        raise ValueError("negative value; must be positive")
    return result


def _padding(value: str | None):
    if not value:
        raise ValueError("must be a list of 4 values")
    result = directives.positive_int_list(value)
    if len(result) != 4:
        raise ValueError("must be a list of 4 values")
    return result


OPTION_SPEC_DIAGRAMS = {
    "reverse": directives.flag,
    "no-reverse": directives.flag,
    "end-class": _end_class,
    "svg-padding": _padding,
    "svg-title": _non_negative_int,
    "svg-description": _non_negative_int,
    "svg-vertical-choice-separation-outer": _non_negative_int,
    "svg-vertical-choice-separation": _non_negative_int,
    "svg-vertical-seq-separation-outer": _non_negative_int,
    "svg-vertical-seq-separation": _non_negative_int,
    "svg-horizontal-seq-separation": _non_negative_int,
    "svg-arrow-style": _arrow_style,
    "svg-arrow-length": _non_negative_int,
    "svg-arrow-cross-length": _non_negative_int,
    "svg-max-width": _non_negative_int,
    "svg-arc-radius": _non_negative_int,
    "svg-arc-margin": _non_negative_int,
    "svg-terminal-horizontal-padding": _non_negative_int,
    "svg-terminal-vertical-padding": _non_negative_int,
    "svg-terminal-radius": _non_negative_int,
    "svg-non-terminal-horizontal-padding": _non_negative_int,
    "svg-non-terminal-vertical-padding": _non_negative_int,
    "svg-non-terminal-radius": _non_negative_int,
    "svg-comment-horizontal-padding": _non_negative_int,
    "svg-comment-vertical-padding": _non_negative_int,
    "svg-comment-radius": _non_negative_int,
    "svg-group-vertical-padding": _non_negative_int,
    "svg-group-horizontal-padding": _non_negative_int,
    "svg-group-vertical-margin": _non_negative_int,
    "svg-group-horizontal-margin": _non_negative_int,
    "svg-group-radius": _non_negative_int,
    "svg-group-text-vertical-offset": _non_negative_int,
    "svg-group-text-horizontal-offset": _non_negative_int,
    "text-padding": _padding,
    "text-vertical-choice-separation-outer": _non_negative_int,
    "text-vertical-choice-separation": _non_negative_int,
    "text-vertical-seq-separation-outer": _non_negative_int,
    "text-vertical-seq-separation": _non_negative_int,
    "text-horizontal-seq-separation": _non_negative_int,
    "text-group-vertical-padding": _non_negative_int,
    "text-group-horizontal-padding": _non_negative_int,
    "text-group-vertical-margin": _non_negative_int,
    "text-group-horizontal-margin": _non_negative_int,
    "text-group-text-vertical-offset": _int,
    "text-group-text-horizontal-offset": _non_negative_int,
    "text-max-width": _non_negative_int,
}


class ContextManagerMixin(SphinxDirective):
    option_spec: _t.ClassVar[dict[str, _t.Callable[[str], _t.Any]]] = {  # type: ignore
        **{
            f"diagram-{name}": validator
            for name, validator in OPTION_SPEC_DIAGRAMS.items()
        },
    }

    @property
    def syntax_domain(self) -> SyntaxDomain:
        if not hasattr(self, "domain"):
            if ":" in self.name:
                self.domain, _ = self.name.split(":", maxsplit=1)
            else:
                self.domain = None

        domain = self.env.get_domain(self.domain or "syntax")
        assert isinstance(domain, SyntaxDomain)

        return domain

    def get_diagram_options(self, prefix="diagram-") -> _t.Dict[str, _t.Any]:
        if f"{prefix}no-reverse" in self.options:
            if f"{prefix}reverse" in self.options:
                self.state_machine.reporter.warning(
                    f":{prefix}reverse: can't be given together with :{prefix}no-reverse:",
                    line=self.lineno,
                )
            self.options[f"{prefix}reverse"] = False
            del self.options[f"{prefix}no-reverse"]
        elif f"{prefix}reverse" in self.options:
            self.options[f"{prefix}reverse"] = True

        return {
            **(self.env.ref_context.get(f"{self.syntax_domain.name}:diagram") or {}),
            **{
                name: self.options[prefix + name]
                for name in OPTION_SPEC_DIAGRAMS
                if prefix + name in self.options
            },
        }

    def push_context(self, objtype: str, fullname: str | None) -> None:
        objects = self.env.ref_context.setdefault(
            f"{self.syntax_domain.name}:{objtype}s", []
        )
        objects.append(self.env.ref_context.get(f"{self.syntax_domain.name}:{objtype}"))
        if fullname:
            self.env.ref_context[f"{self.syntax_domain.name}:{objtype}"] = fullname

        diagrams = self.env.ref_context.setdefault(
            f"{self.syntax_domain.name}:diagrams", []
        )
        diagrams.append(self.env.ref_context.get(f"{self.syntax_domain.name}:diagram"))
        self.env.ref_context[f"{self.syntax_domain.name}:diagram"] = (
            self.get_diagram_options()
        )

    def pop_context(self, objtype: str) -> None:
        objects = self.env.ref_context.setdefault(
            f"{self.syntax_domain.name}:{objtype}s", []
        )
        if objects:
            self.env.ref_context[f"{self.syntax_domain.name}:{objtype}"] = objects.pop()
        else:
            self.env.ref_context.pop(f"{self.syntax_domain.name}:{objtype}", None)

    def get_context_grammar(self) -> str | None:
        return self.env.ref_context.get(f"{self.syntax_domain.name}:grammar")


class SyntaxObjectDescription(
    ObjectDescription[tuple[str, str, str]], ContextManagerMixin
):
    option_spec: _t.ClassVar[dict[str, _t.Callable[[str], _t.Any]]] = {
        "name": directives.unchanged,
        **ContextManagerMixin.option_spec,
        **sphinx.directives.ObjectDescription.option_spec,
    }

    def get_display_prefix(self) -> list[docutils.nodes.Node]:
        return []

    def handle_signature(
        self, sig: str, signode: sphinx.addnodes.desc_signature
    ) -> tuple[str, str, str]:
        prefix = self.env.ref_context.get(f"{self.domain}:grammar", "")

        if prefix:
            fullname = f"{prefix}.{sig}"
        else:
            fullname = sig

        signode["grammar"] = prefix
        signode["fullname"] = fullname

        display_prefix = self.get_display_prefix()
        if display_prefix:
            signode += sphinx.addnodes.desc_annotation("", "", *display_prefix)

        signode += sphinx.addnodes.desc_name(
            "", "", sphinx.addnodes.desc_sig_name("", self.options.get("name") or sig)
        )

        return fullname, prefix, sig

    def _object_hierarchy_parts(
        self, sig_node: sphinx.addnodes.desc_signature
    ) -> tuple[str, ...]:
        if "fullname" not in sig_node:
            return ()
        return tuple(sig_node["fullname"].split("."))

    def add_target_and_index(
        self,
        name: tuple[str, str, str],
        sig: str,
        signode: sphinx.addnodes.desc_signature,
    ) -> None:
        fullname, _prefix, objname = name
        id_prefix = self.domain or "syntax"
        if self.objtype != "grammar":
            id_prefix += f"-{self.objtype}"
        id = make_id(self.env, self.state.document, id_prefix, fullname)

        if id not in self.state.document.ids:
            signode["names"].append(id)
            signode["ids"].append(id)
            signode["first"] = not self.names
            self.state.document.note_explicit_target(signode)

            self.syntax_domain.note_object(
                self.state_machine,
                self.lineno,
                self.env.docname,
                self.objtype,
                objname,
                fullname,
                id,
                self.options.get("name"),
                self.options.get("imports"),
            )

        if "no-index-entry" not in self.options:
            if index_text := self.get_index_text(name):
                self.indexnode["entries"].append(
                    (
                        "single",
                        index_text,
                        id,
                        "",
                        None,
                    )
                )

    def get_index_text(self, name: tuple[str, str, str]) -> str:
        _fullname, prefix, objname = name
        if prefix:
            return _("%s (%s production rule)") % (objname, prefix)
        else:
            return _("%s (%s)") % (objname, self.objtype)

    def before_content(self) -> None:
        if self.names:
            fullname, _prefix, _objname = self.names[-1]
        else:
            fullname = None
        self.push_context(self.objtype, fullname)

    def after_content(self) -> None:
        self.pop_context(self.objtype)

    def _toc_entry_name(self, sig_node: sphinx.addnodes.desc_signature) -> str:
        if not sig_node.get("_toc_parts"):
            return ""

        config = self.config
        *parents, name = sig_node["_toc_parts"]
        if config.toc_object_entries_show_parents == "domain":
            return sig_node.get("fullname", name)
        if config.toc_object_entries_show_parents == "hide":
            return name
        if config.toc_object_entries_show_parents == "all":
            return ".".join([*parents, name])
        return ""


class GrammarDescription(SyntaxObjectDescription):
    option_spec = {
        "imports": _list,
        **SyntaxObjectDescription.option_spec,
    }

    def get_signatures(self) -> list[str]:
        if self.env.ref_context.get(f"{self.domain}:grammar"):
            raise self.error(f"grammars can't be nested within other grammars")
        if self.env.ref_context.get(f"{self.domain}:rule"):
            raise self.error(f"grammars can't be nested within production rules")
        return super().get_signatures()

    def handle_signature(
        self, sig: str, signode: sphinx.addnodes.desc_signature
    ) -> tuple[str, str, str]:
        if "." in sig:
            raise self.error(f"dots are not allowed in grammar names: {sig!r}")
        return super().handle_signature(sig, signode)

    def get_display_prefix(self) -> list[docutils.nodes.Node]:
        return [
            sphinx.addnodes.desc_annotation("", "grammar"),
            sphinx.addnodes.desc_sig_space(),
        ]


class RuleDescription(SyntaxObjectDescription):
    def get_signatures(self) -> list[str]:
        if self.env.ref_context.get(f"{self.domain}:rule"):
            raise self.error(f"rules can't be nested within other production rules")
        return super().get_signatures()


class SyntaxXRefRole(XRefRole):
    def process_link(
        self,
        env: BuildEnvironment,
        refnode: docutils.nodes.Element,
        has_explicit_title: bool,
        title: str,
        target: str,
    ) -> tuple[str, str]:
        domain = self.refdomain or "syntax"
        refnode[f"{domain}:grammar"] = env.ref_context.get(f"{domain}:grammar")
        if not has_explicit_title:
            title = title.lstrip(".")
            target = target.lstrip("~")
            if title[0:1] == "~":
                title = title[1:]
                dot = title.rfind(".")
                if dot != -1:
                    title = title[dot + 1 :]
        return title, target


class SyntaxDomain(Domain):
    @dataclass
    class IndexEntry:
        docname: str
        objtype: str
        name: str
        fullname: str
        id: str | None
        display_name: str | None = None
        imports: list[str] | None = None

        def __eq__(self, value: object) -> bool:
            return (
                isinstance(value, SyntaxDomain.IndexEntry)
                and self.fullname == value.fullname
            )

        def __ne__(self, value: object) -> bool:
            return not (self == value)

        def __hash__(self) -> int:
            return hash(self.fullname)

    DEFAULT_GRAMMAR = IndexEntry(
        docname="",
        objtype="grammar",
        name="",
        fullname="",
        id=None,
        display_name=None,
        imports=[],
    )

    name = "syntax"

    label = "Syntax"

    object_types = {
        "rule": ObjType(_("production rule"), "rule", "r", "obj", "_auto"),
        "grammar": ObjType(_("grammar"), "grammar", "g", "obj", "_auto"),
    }

    directives = {
        "rule": RuleDescription,
        "grammar": GrammarDescription,
    }

    roles = {
        "rule": SyntaxXRefRole(),
        "r": SyntaxXRefRole(),
        "grammar": SyntaxXRefRole(),
        "g": SyntaxXRefRole(),
        "obj": SyntaxXRefRole(),
        "_auto": SyntaxXRefRole(),
    }

    initial_data = {
        "grammars": {},
        "rules": {},
    }

    def note_object(
        self,
        state_machine: RSTStateMachine,
        lineno: int,
        docname: str,
        objtype: str,
        name: str,
        fullname: str,
        id: str | None,
        display_name: str | None,
        imports: list[str] | None,
    ):
        if objtype == "grammar":
            index = self.grammars
        elif objtype == "rule":
            index = self.rules
        else:
            raise RuntimeError(f"unknown objtype {objtype}")

        if fullname in index and self.env.docname != index[fullname].docname:
            state_machine.reporter.warning(
                "duplicate object description of %s, " % fullname
                + "other instance in "
                + self.env.doc2path(index[fullname].docname)
                + ", use :no-index: for one of them",
                line=lineno,
            )

        index[fullname] = SyntaxDomain.IndexEntry(
            docname=docname,
            objtype=objtype,
            name=name,
            fullname=fullname,
            id=id,
            display_name=display_name,
            imports=imports,
        )

    @property
    def rules(self) -> dict[str, IndexEntry]:
        return self.data["rules"]

    @property
    def grammars(self) -> dict[str, IndexEntry]:
        return self.data["grammars"]

    def _find_grammar(self, fullname: str):
        if result := self.grammars.get(fullname):
            return result

    def _find_rule(self, fullname: str):
        if result := self.rules.get(fullname):
            return result

    def _find_obj(self, fullname: str):
        for index in [self.grammars, self.rules]:
            if result := index.get(fullname):
                return result

    def _traverse_grammars(self, roots, add_default_grammar):
        stack = list(roots)
        seen = set()
        while stack:
            grammar_name = stack.pop()
            if grammar_name in seen:
                continue
            seen.add(grammar_name)
            grammar = self._find_grammar(grammar_name)
            if grammar is not None:
                yield grammar
                stack.extend(grammar.imports or [])
        if add_default_grammar:
            yield self.DEFAULT_GRAMMAR

    def clear_doc(self, docname):
        for fullname, entry in list(self.grammars.items()):
            if entry.docname == docname:
                self.grammars.pop(fullname)
        for fullname, entry in list(self.rules.items()):
            if entry.docname == docname:
                self.rules.pop(fullname)

    def merge_domaindata(self, docnames, otherdata):
        grammars: dict[str, SyntaxDomain.IndexEntry] = otherdata["grammars"]
        grammars = {k: v for k, v in grammars.items() if v.docname in docnames}
        self._check_duplicates(self.env, grammars, self.grammars)
        self.grammars.update(grammars)

        rules: dict[str, SyntaxDomain.IndexEntry] = otherdata["rules"]
        rules = {k: v for k, v in rules.items() if v.docname in docnames}
        self._check_duplicates(self.env, grammars, self.grammars)
        self.rules.update(rules)

    @staticmethod
    def _check_duplicates(
        env: BuildEnvironment, l: dict[str, IndexEntry], r: dict[str, IndexEntry]
    ):
        for fullname, data in l.items():
            if fullname in r:
                logger.warning(
                    "duplicate description for object %s found in files %s and %s",
                    fullname,
                    env.doc2path(data.docname),
                    env.doc2path(r[fullname].docname),
                )

    def resolve_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: pending_xref,
        contnode: docutils.nodes.Element,
    ) -> docutils.nodes.reference | None:
        resolvers = []
        for objtype in self.objtypes_for_role(typ) or []:
            if objtype == "grammar":
                resolvers.append(self._resolve_grammar)
            elif objtype == "rule":
                resolvers.append(self._resolve_rule)

        results: list[docutils.nodes.reference] = []
        for resolver in resolvers:
            results.extend(resolver(env, fromdocname, builder, target, node, contnode))

        if len(results) > 1 and typ != "_auto":
            candidates = " or ".join(
                f"{result["syntax:objtype"]} {result["syntax:target"]} "
                f"from {self.env.doc2path(result["syntax:docname"])}"
                for result in results
            )
            logger.warning(
                "reference :%s:%s:`%s` resolved to multiple objects: can be %s",
                self.name,
                typ,
                target,
                candidates,
                type="lua-ls",
                location=(node.source, node.line),
            )
        if results:
            return results[0]
        else:
            return None

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: docutils.nodes.Element,
    ) -> list[tuple[str, docutils.nodes.reference]]:
        results = []

        grammars = self._resolve_grammar(
            env, fromdocname, builder, target, node, contnode
        )
        results.extend([(f"{self.name}:grammar", grammar) for grammar in grammars])

        rules = self._resolve_rule(env, fromdocname, builder, target, node, contnode)
        results.extend([(f"{self.name}:rule", grammar) for grammar in rules])

        return results

    def _resolve_grammar(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: docutils.nodes.Element,
    ) -> list[docutils.nodes.reference]:
        obj = self._find_grammar(target)
        if obj is not None:
            return [self._make_refnode(fromdocname, builder, node, contnode, obj)]
        else:
            return []

    def _resolve_rule(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: docutils.nodes.Element,
    ) -> list[docutils.nodes.reference]:
        if "." in target:
            # Got fully qualified rule reference.
            add_default_grammar = False
            grammar_name, rule_name = target.split(".", 1)
            roots = [grammar_name]
        elif f"{self.name}:grammar" in node:
            # Got rule reference made by SyntaxXRefRole.
            add_default_grammar = True
            grammar_name, rule_name = node[f"{self.name}:grammar"], target
            roots = [grammar_name] if grammar_name else []
        else:
            # Got rule reference made by AnyXRefRole.
            add_default_grammar = True
            roots = list(self.grammars.keys())
            rule_name = target

        results: list[docutils.nodes.reference] = []

        for grammar in self._traverse_grammars(roots, add_default_grammar):
            if grammar.name:
                fullname = f"{grammar.name}.{rule_name}"
            else:
                fullname = rule_name
            obj = self._find_rule(fullname)
            if obj is not None:
                refnode = self._make_refnode(fromdocname, builder, node, contnode, obj)
                results.append(refnode)

        return results

    def _make_refnode(
        self,
        fromdocname: str,
        builder: sphinx.builders.Builder,
        node: pending_xref,
        contnode: docutils.nodes.Element,
        obj: IndexEntry,
    ) -> docutils.nodes.reference:
        if not node["refexplicit"] and obj.display_name:
            contnode = contnode.deepcopy()
            contnode.clear()
            contnode += docutils.nodes.Text(obj.display_name)
        refnode = make_refnode(
            builder, fromdocname, obj.docname, obj.id, contnode, obj.fullname
        )

        # Add debug info, only used for warning messages.
        refnode["syntax:target"] = obj.fullname
        refnode["syntax:objtype"] = obj.objtype
        refnode["syntax:docname"] = obj.docname

        return refnode

    def get_objects(self):
        for fullname, entry in itertools.chain(
            self.grammars.items(), self.rules.items()
        ):
            if entry.id:
                display_name = entry.display_name or entry.name or fullname
                yield (
                    fullname,
                    display_name,
                    entry.objtype,
                    entry.docname,
                    entry.id,
                    1,
                )

    def get_full_qualified_name(self, node: docutils.nodes.Element) -> str | None:
        grammar = node.get(f"{self.name}:grammar")
        target = node.get("reftarget")
        if target is None:
            return None
        else:
            return ".".join(filter(None, [grammar, target]))
