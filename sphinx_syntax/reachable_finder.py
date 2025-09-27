from __future__ import annotations

from sphinx_syntax.model import (
    Alternative,
    Doc,
    Negation,
    OnePlus,
    Reference,
    RuleBase,
    RuleContentVisitor,
    Sequence,
    Wildcard,
    ZeroPlus,
)


class _ReachableFiner(RuleContentVisitor[set[RuleBase]]):
    def __init__(self):
        super().__init__()

        self._seen = set()

    def visit_literal(self, r) -> set[RuleBase]:
        return set()

    def visit_range(self, r) -> set[RuleBase]:
        return set()

    def visit_charset(self, r) -> set[RuleBase]:
        return set()

    def visit_reference(self, r: Reference) -> set[RuleBase]:
        ref = r.get_reference()
        if ref is None:
            return set()
        elif ref in self._seen:
            return set()
        else:
            self._seen.add(ref)
            if ref.content:
                return {ref} | self.visit(ref.content)
            else:
                return {ref}

    def visit_doc(self, r: Doc) -> set[RuleBase]:
        return set()

    def visit_wildcard(self, r: Wildcard) -> set[RuleBase]:
        return set()

    def visit_negation(self, r: Negation) -> set[RuleBase]:
        return self.visit(r.child)

    def visit_zero_plus(self, r: ZeroPlus) -> set[RuleBase]:
        return self.visit(r.child)

    def visit_one_plus(self, r: OnePlus) -> set[RuleBase]:
        return self.visit(r.child)

    def visit_sequence(self, r: Sequence) -> set[RuleBase]:
        return set().union(*[self.visit(c) for c in r.children])

    def visit_alternative(self, r: Alternative) -> set[RuleBase]:
        return set().union(*[self.visit(c) for c in r.children])


def find_reachable_rules(r: RuleBase) -> set[RuleBase]:
    """
    Calculates a set of rules that are reachable from the root rule.

    """

    if r.content:
        return {r} | _ReachableFiner().visit(r.content)
    else:
        return {r}
