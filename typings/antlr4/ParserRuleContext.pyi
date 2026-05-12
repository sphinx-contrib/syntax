from collections.abc import Callable, Generator
from typing import TypeVar

from antlr4.error.Errors import RecognitionException
from antlr4.RuleContext import RuleContext as RuleContext
from antlr4.Token import Token as Token
from antlr4.tree.Tree import (
    INVALID_INTERVAL as INVALID_INTERVAL,
)
from antlr4.tree.Tree import (
    ErrorNodeImpl as ErrorNodeImpl,
)
from antlr4.tree.Tree import (
    ParseTree as ParseTree,
)
from antlr4.tree.Tree import (
    ParseTreeListener as ParseTreeListener,
)
from antlr4.tree.Tree import (
    TerminalNode as TerminalNode,
)
from antlr4.tree.Tree import (
    TerminalNodeImpl as TerminalNodeImpl,
)

class ParserRuleContext(RuleContext):
    __slots__ = ("children", "start", "stop", "exception")
    children: list[ParseTree | TerminalNode]
    start: Token
    stop: Token
    exception: RecognitionException | None
    def __init__(
        self,
        parent: ParserRuleContext | None = None,
        invokingStateNumber: int | None = None,
    ) -> None: ...
    parentCtx: RuleContext | None
    invokingState: int
    def copyFrom(self, ctx: ParserRuleContext) -> None: ...
    def enterRule(self, listener: ParseTreeListener) -> None: ...
    def exitRule(self, listener: ParseTreeListener) -> None: ...
    def addChild(self, child: _ParseTreeT) -> _ParseTreeT: ...
    def removeLastChild(self) -> None: ...
    def addTokenNode(self, token: Token) -> TerminalNodeImpl: ...
    def addErrorNode(self, badToken: Token) -> ErrorNodeImpl: ...
    def getChild(
        self, i: int, ttype: type[_GenericType] | None = None
    ) -> _GenericType: ...
    def getChildren(
        self, predicate: Callable[[ParseTree | TerminalNode], bool] | None = None
    ) -> Generator[ParseTree | TerminalNode]: ...
    def getToken(self, ttype: int, i: int) -> TerminalNode: ...
    def getTokens(self, ttype: int) -> list[TerminalNode]: ...
    def getTypedRuleContext(
        self, ctxType: type[_ParserRuleContextT], i: int
    ) -> _ParserRuleContextT: ...
    def getTypedRuleContexts(
        self, ctxType: type[_ParserRuleContextT]
    ) -> list[_ParserRuleContextT]: ...
    def getChildCount(self) -> int: ...
    def getSourceInterval(self) -> tuple[int | None, int | None]: ...

_GenericType = TypeVar("_GenericType", bound=type)
_ParseTreeT = TypeVar("_ParseTreeT", bound=ParseTree)
_ParserRuleContextT = TypeVar("_ParserRuleContextT", bound=ParserRuleContext)

class InterpreterRuleContext(ParserRuleContext):
    ruleIndex: int
    def __init__(
        self, parent: ParserRuleContext, invokingStateNumber: int, ruleIndex: int
    ) -> None: ...
