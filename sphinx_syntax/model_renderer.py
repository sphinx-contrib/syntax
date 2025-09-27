from __future__ import annotations

import ast
import re
import typing as _t

import syntax_diagrams

from sphinx_syntax.model import (
    EMPTY,
    Alternative,
    CachedRuleContentVisitor,
    CharSet,
    Doc,
    HrefResolverData,
    LexerRule,
    Literal,
    Negation,
    OnePlus,
    ParserRule,
    Range,
    Reference,
    RuleBase,
    RuleContent,
    Sequence,
    Wildcard,
    ZeroPlus,
)

_TO_DASH_CASE_RE = re.compile(
    r"""
                                        # We will add a dash (bear with me here):
      _                                 # 1. instead of underscore,
      | (                               # 2. OR in the following case:
        (?<!^)                          #   - not at the beginning of the string,
        (                               #   - AND EITHER:
            (?<=[A-Z])(?=[A-Z][a-z])    #     - before case gets lower (`XMLTag` -> `XML-Tag`),
          | (?<=[a-zA-Z])(?![a-zA-Z_])  #     - between a letter and a non-letter (`HTTP20` -> `HTTP-20`),
          | (?<![A-Z_])(?=[A-Z])        #     - between non-uppercase and uppercase letter (`TagXML` -> `Tag-XML`),
        )                               #   - AND ALSO:
        (?!$)                           #     - not at the end of the string.
      )
    """,
    re.VERBOSE | re.MULTILINE,
)


def to_dash_case(s: str, /) -> str:
    """Convert ``CamelCase`` or ``snake_case`` identifier to a ``dash-case`` one.

    This function assumes ASCII input, and will not work correctly
    with non-ASCII characters.

    """

    return _TO_DASH_CASE_RE.sub("-", s).lower()


class ImportanceProvider(CachedRuleContentVisitor[int]):
    """
    Given a rule content item, calculates its importance.

    """

    def visit_literal(self, r: Literal) -> int:
        return 1

    def visit_range(self, r: Range) -> int:
        return 1

    def visit_charset(self, r: CharSet) -> int:
        return 1

    def visit_reference(self, r: Reference) -> int:
        rule = r.get_reference()
        if rule is None:
            return 1
        else:
            return rule.importance

    def visit_doc(self, r: Doc) -> int:
        return 0

    def visit_wildcard(self, r: Wildcard) -> int:
        return 1

    def visit_negation(self, r: Negation) -> int:
        return self.visit(r.child)

    def visit_zero_plus(self, r: ZeroPlus) -> int:
        return self.visit(r.child)

    def visit_one_plus(self, r: OnePlus) -> int:
        return self.visit(r.child)

    def visit_sequence(self, r: Sequence) -> int:
        if not r.children:
            return 0
        return max(self.visit(c) for c in r.children)

    def visit_alternative(self, r: Alternative) -> int:
        if not r.children:
            return 0
        return max(self.visit(c) for c in r.children)


class _Renderer(CachedRuleContentVisitor[syntax_diagrams.Element[HrefResolverData]]):
    def __init__(
        self,
        literal_rendering: _t.Literal[
            "name", "contents", "contents-unquoted"
        ] = "contents-unquoted",
        cc_to_dash: bool = False,
        importance_provider: ImportanceProvider = ImportanceProvider(),
    ):
        super().__init__()

        self.do_cc_to_dash = cc_to_dash
        self.literal_rendering = literal_rendering
        self.importance_provider = importance_provider

        self._path: set[RuleBase] = set()

    def render(self, rule: RuleBase) -> syntax_diagrams.Element[HrefResolverData]:
        self._path.add(rule)
        try:
            return self._opt_recursion(rule)
        finally:
            self._path.remove(rule)

    def _opt_recursion(
        self, rule: RuleBase
    ) -> syntax_diagrams.Element[HrefResolverData]:
        assert rule.content
        if isinstance(rule.content, Alternative) and not rule.keep_diagram_recursive:
            left_recursive_branches: set[int] = set()
            right_recursive_branches: set[int] = set()
            for i, elem in enumerate(rule.content.children):
                if isinstance(elem, Sequence) and elem.children:
                    if (
                        isinstance(elem.children[0], Reference)
                        and elem.children[0].get_reference() is rule
                    ):
                        left_recursive_branches.add(i)
                    elif (
                        isinstance(elem.children[-1], Reference)
                        and elem.children[-1].get_reference() is rule
                    ):
                        right_recursive_branches.add(i)

            if left_recursive_branches and len(left_recursive_branches) >= len(
                right_recursive_branches
            ):
                is_left_recursive = True
                recursive_branches: list[RuleContent] = []
                normal_branches: list[RuleContent] = []
                for i, elem in enumerate(rule.content.children):
                    if i in left_recursive_branches:
                        elem = _t.cast(Sequence, elem)
                        recursive_branches.append(
                            Sequence(
                                elem.children[1:],
                                elem.linebreaks[1:],
                            )
                        )
                    else:
                        normal_branches.append(elem)
            elif right_recursive_branches:
                is_left_recursive = False
                recursive_branches: list[RuleContent] = []
                normal_branches: list[RuleContent] = []
                for i, elem in enumerate(rule.content.children):
                    if i in right_recursive_branches:
                        elem = _t.cast(Sequence, elem)
                        recursive_branches.append(
                            Sequence(
                                elem.children[:-1],
                                elem.linebreaks[:-1],
                            )
                        )
                    else:
                        normal_branches.append(elem)
            else:
                return self.visit(self._opt_alternative(list(rule.content.children)))

            if is_left_recursive:
                start = self._opt_alternative(normal_branches)
                repeat = self._opt_alternative(recursive_branches)
                return self.visit(Sequence((start, ZeroPlus(repeat))))
            else:
                repeat = self._opt_alternative(recursive_branches)
                end = self._opt_alternative(normal_branches)
                return self.visit(Sequence((ZeroPlus(repeat), end)))
        else:
            return self.visit(rule.content)

    def visit_literal(self, r: Literal):
        return syntax_diagrams.terminal(
            self._unquote(r.content),
            css_class="literal",
            resolver_data=HrefResolverData(text_is_weak=False),
        )

    def visit_range(self, r: Range):
        return syntax_diagrams.terminal(
            f"{r.start}..{r.end}",
            css_class="range",
            resolver_data=HrefResolverData(text_is_weak=False),
        )

    def visit_charset(self, r: CharSet):
        return syntax_diagrams.terminal(
            r.content,
            css_class="charset",
            resolver_data=HrefResolverData(text_is_weak=False),
        )

    def visit_reference(self, r: Reference):
        rule = r.get_reference()
        if rule is None:
            if r.name and (r.name[0].isupper() or r.name.startswith("'")):
                if r.name.startswith("'") and r.name.endswith("'"):
                    name = self._unquote(r.name)
                else:
                    name = self._cc_to_dash(r.name)
                return syntax_diagrams.terminal(
                    name,
                    resolver_data=HrefResolverData(text_is_weak=True),
                )
            else:
                return syntax_diagrams.non_terminal(
                    self._cc_to_dash(r.name),
                    resolver_data=HrefResolverData(text_is_weak=True),
                )
        elif rule.is_inline and rule.content is not None and rule not in self._path:
            return self.render(rule)
        elif isinstance(rule, LexerRule):
            path = f"{rule.model.get_name()}.{rule.name}"
            if rule.is_literal and self.literal_rendering != "name":
                literal = self._unquote(str(rule.content))
                return syntax_diagrams.terminal(
                    literal,
                    href=path,
                    resolver_data=HrefResolverData(text_is_weak=False),
                    css_class=rule.css_class,
                )
            else:
                name = rule.display_name or self._cc_to_dash(rule.name)
                return syntax_diagrams.terminal(
                    name,
                    href=path,
                    resolver_data=HrefResolverData(text_is_weak=True),
                    css_class=rule.css_class,
                )
        elif isinstance(rule, ParserRule):
            return syntax_diagrams.non_terminal(
                rule.display_name or self._cc_to_dash(rule.name),
                href=f"{rule.model.get_name()}.{rule.name}",
                resolver_data=HrefResolverData(text_is_weak=True),
                css_class=rule.css_class,
            )
        else:
            assert False, "don't use RuleBase; instead, use LexerRule or ParserRule"

    def visit_doc(self, r: Doc):
        return syntax_diagrams.comment(r.value)

    def visit_wildcard(self, r: Wildcard):
        return syntax_diagrams.terminal(
            ".",
            css_class="wildcard",
            resolver_data=HrefResolverData(text_is_weak=False),
        )

    def visit_negation(self, r: Negation):
        return syntax_diagrams.terminal(
            str(r),
            css_class="negation",
            resolver_data=HrefResolverData(text_is_weak=False),
        )

    def visit_zero_plus(self, r: ZeroPlus):
        skip = not self.importance_provider.visit(r.child)
        return syntax_diagrams.zero_or_more(self.visit(r.child), skip=skip)

    def visit_one_plus(self, r: OnePlus):
        return syntax_diagrams.one_or_more(self.visit(r.child))

    def visit_sequence(self, r: Sequence):
        return self._opt_sequence(list(r.children), list(r.linebreaks))

    def _opt_sequence(
        self,
        seq: list[RuleContent | syntax_diagrams.Element[HrefResolverData]],
        lb: list[syntax_diagrams.LineBreak],
    ):
        if not seq:
            return syntax_diagrams.skip()

        assert len(seq) == len(lb) + 1

        # x y z (A B x y z)* -> OneOrMore((x y z), (A B))
        for i in range(len(seq) - 1, -1, -1):
            star = seq[i]

            if not isinstance(star, ZeroPlus):
                continue

            nested_seq: list[RuleContent | syntax_diagrams.Element[HrefResolverData]]
            if isinstance(star.child, Sequence):
                nested_seq = list(star.child.children)
                nested_seq_lb = list(star.child.linebreaks)
            else:
                nested_seq = [star.child]
                nested_seq_lb = []

            for j in range(len(nested_seq) - 1, -1, -1):
                k = i + j - len(nested_seq)
                if k < 0 or seq[k] is not nested_seq[j]:
                    seq_start = k + 1
                    nested_seq_start = j + 1
                    break
            else:
                seq_start = i - len(nested_seq)
                nested_seq_start = 0

            if seq_start == i:
                continue

            repeat = self._opt_sequence(
                nested_seq[:nested_seq_start], nested_seq_lb[: nested_seq_start - 1]
            )
            main = self._opt_sequence(
                nested_seq[nested_seq_start:], nested_seq_lb[nested_seq_start:]
            )

            item = syntax_diagrams.one_or_more(main, repeat=repeat)

            seq[seq_start : i + 1] = [item]
            lb[seq_start:i] = []

            return self._opt_sequence(seq, lb)

        # (x y z A B)* x y z -> OneOrMore((x y z), (A B))
        for i in range(len(seq)):
            star = seq[i]

            if not isinstance(star, ZeroPlus):
                continue

            nested_seq: list[RuleContent | syntax_diagrams.Element[HrefResolverData]]
            if isinstance(star.child, Sequence):
                nested_seq = list(star.child.children)
                nested_seq_lb = list(star.child.linebreaks)
            else:
                nested_seq = [star.child]
                nested_seq_lb = []

            for j in range(len(nested_seq)):
                k = i + j + 1
                if k >= len(seq) or seq[k] is not nested_seq[j]:
                    seq_end = k - 1
                    nested_seq_end = j
                    break
            else:
                seq_end = len(nested_seq)
                nested_seq_end = -1

            if seq_end == i:
                continue

            main = self._opt_sequence(
                nested_seq[:nested_seq_end], nested_seq_lb[: nested_seq_end - 1]
            )
            repeat = self._opt_sequence(
                nested_seq[nested_seq_end:], nested_seq_lb[nested_seq_end:]
            )

            item = syntax_diagrams.one_or_more(main, repeat=repeat)

            seq[i : seq_end + 1] = [item]
            lb[i:seq_end] = []

            return self._opt_sequence(seq, lb)

        return syntax_diagrams.sequence(
            *[self.visit(e) if isinstance(e, RuleContent) else e for e in seq],
            linebreaks=list(lb),
        )

    def visit_alternative(self, r: Alternative):
        default = max(
            enumerate(r.children),
            key=lambda x: self.importance_provider.visit(x[1]),
        )[0]
        return syntax_diagrams.choice(
            *[self.visit(c) for c in r.children], default=default
        )

    def _opt_alternative(self, children: list[RuleContent]):
        if len(children) <= 1:
            return Alternative(tuple(children))

        # (x A | x B) -> x (A | B)
        front_elements: dict[RuleContent, list[int]] = {}
        can_optimize = False
        for i, elem in enumerate(children):
            if isinstance(elem, Sequence) and elem.children:
                first = elem.children[0]
            else:
                first = elem
            if first in front_elements:
                can_optimize = True
                front_elements[first].append(i)
            else:
                front_elements[first] = [i]
        if can_optimize:
            new_children: list[RuleContent] = []
            for i, elem in enumerate(children):
                if isinstance(elem, Sequence) and elem.children:
                    first = elem.children[0]
                else:
                    first = elem
                if not (indices := front_elements.get(first)) or len(indices) <= 1:
                    new_children.append(elem)
                    continue
                if indices[0] != i:
                    continue
                new_sub_children: list[RuleContent] = []
                for j in indices:
                    elem = children[j]
                    if isinstance(elem, Sequence):
                        new_sub_children.append(
                            Sequence(
                                elem.children[1:],
                                elem.linebreaks[1:],
                            )
                        )
                    else:
                        new_sub_children.append(EMPTY)
                new_children.append(
                    Sequence(
                        (
                            first,
                            self._opt_alternative(new_sub_children),
                        )
                    )
                )
            children = new_children

        if len(children) <= 1:
            return Alternative(tuple(children))

        # (A x | B x) -> (A | B) x
        back_elements: dict[RuleContent, list[int]] = {}
        can_optimize = False
        for i, elem in enumerate(children):
            if isinstance(elem, Sequence) and elem.children:
                last = elem.children[-1]
            else:
                last = elem
            if last in back_elements:
                can_optimize = True
                back_elements[last].append(i)
            else:
                back_elements[last] = [i]
        if can_optimize:
            new_children: list[RuleContent] = []
            for i, elem in enumerate(children):
                if isinstance(elem, Sequence) and elem.children:
                    last = elem.children[-1]
                else:
                    last = elem
                if not (indices := back_elements.get(last)) or len(indices) <= 1:
                    new_children.append(elem)
                    continue
                if indices[0] != i:
                    continue
                new_sub_children: list[RuleContent] = []
                for j in indices:
                    elem = children[j]
                    if isinstance(elem, Sequence):
                        new_sub_children.append(
                            Sequence(
                                elem.children[:-1],
                                elem.linebreaks[:-1],
                            )
                        )
                    else:
                        new_sub_children.append(EMPTY)
                new_children.append(
                    Sequence(
                        (
                            self._opt_alternative(new_sub_children),
                            last,
                        )
                    )
                )
                continue
            children = new_children

        return Alternative(tuple(children))

    def _cc_to_dash(self, name: str) -> str:
        if self.do_cc_to_dash:
            return to_dash_case(name)
        else:
            return name

    def _unquote(self, s: str) -> str:
        if not (s.startswith("'") and s.endswith("'")):
            return s

        try:
            s = ast.literal_eval(s)
        except SyntaxError:
            return s

        if self.literal_rendering == "contents-unquoted":
            return s
        else:
            return f"'{s}'"


def render(
    rule: RuleBase,
    literal_rendering: _t.Literal[
        "name", "contents", "contents-unquoted"
    ] = "contents-unquoted",
    cc_to_dash: bool = False,
    importance_provider: ImportanceProvider = ImportanceProvider(),
):
    assert rule.content is not None
    return _Renderer(literal_rendering, cc_to_dash, importance_provider).render(rule)
