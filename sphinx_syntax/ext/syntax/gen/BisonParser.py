# Generated from BisonParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,73,183,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,1,0,5,0,36,8,0,10,0,12,0,39,9,0,1,
        0,1,0,1,0,1,0,1,1,1,1,1,1,5,1,48,8,1,10,1,12,1,51,9,1,1,1,1,1,1,
        1,1,1,3,1,57,8,1,1,2,1,2,1,3,1,3,1,4,1,4,5,4,65,8,4,10,4,12,4,68,
        9,4,1,5,1,5,5,5,72,8,5,10,5,12,5,75,9,5,1,5,1,5,1,6,1,6,5,6,81,8,
        6,10,6,12,6,84,9,6,1,6,1,6,1,7,5,7,89,8,7,10,7,12,7,92,9,7,1,8,5,
        8,95,8,8,10,8,12,8,98,9,8,1,8,5,8,101,8,8,10,8,12,8,104,9,8,1,8,
        1,8,3,8,108,8,8,1,8,3,8,111,8,8,1,8,1,8,1,8,1,8,1,9,1,9,5,9,119,
        8,9,10,9,12,9,122,9,9,1,10,1,10,1,10,1,10,1,11,1,11,1,12,1,12,1,
        12,5,12,133,8,12,10,12,12,12,136,9,12,1,13,5,13,139,8,13,10,13,12,
        13,142,9,13,1,14,1,14,3,14,146,8,14,1,14,3,14,149,8,14,1,14,1,14,
        3,14,153,8,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,
        1,14,1,14,1,14,3,14,168,8,14,1,15,1,15,3,15,172,8,15,1,16,1,16,5,
        16,176,8,16,10,16,12,16,179,9,16,1,16,1,16,1,16,0,0,17,0,2,4,6,8,
        10,12,14,16,18,20,22,24,26,28,30,32,0,0,196,0,37,1,0,0,0,2,56,1,
        0,0,0,4,58,1,0,0,0,6,60,1,0,0,0,8,62,1,0,0,0,10,69,1,0,0,0,12,78,
        1,0,0,0,14,90,1,0,0,0,16,96,1,0,0,0,18,116,1,0,0,0,20,123,1,0,0,
        0,22,127,1,0,0,0,24,129,1,0,0,0,26,140,1,0,0,0,28,167,1,0,0,0,30,
        171,1,0,0,0,32,173,1,0,0,0,34,36,3,2,1,0,35,34,1,0,0,0,36,39,1,0,
        0,0,37,35,1,0,0,0,37,38,1,0,0,0,38,40,1,0,0,0,39,37,1,0,0,0,40,41,
        5,1,0,0,41,42,3,14,7,0,42,43,5,0,0,1,43,1,1,0,0,0,44,57,5,2,0,0,
        45,49,5,6,0,0,46,48,3,10,5,0,47,46,1,0,0,0,48,51,1,0,0,0,49,47,1,
        0,0,0,49,50,1,0,0,0,50,52,1,0,0,0,51,49,1,0,0,0,52,57,5,42,0,0,53,
        57,3,8,4,0,54,57,3,4,2,0,55,57,3,6,3,0,56,44,1,0,0,0,56,45,1,0,0,
        0,56,53,1,0,0,0,56,54,1,0,0,0,56,55,1,0,0,0,57,3,1,0,0,0,58,59,5,
        7,0,0,59,5,1,0,0,0,60,61,5,8,0,0,61,7,1,0,0,0,62,66,5,3,0,0,63,65,
        5,4,0,0,64,63,1,0,0,0,65,68,1,0,0,0,66,64,1,0,0,0,66,67,1,0,0,0,
        67,9,1,0,0,0,68,66,1,0,0,0,69,73,5,16,0,0,70,72,3,10,5,0,71,70,1,
        0,0,0,72,75,1,0,0,0,73,71,1,0,0,0,73,74,1,0,0,0,74,76,1,0,0,0,75,
        73,1,0,0,0,76,77,5,52,0,0,77,11,1,0,0,0,78,82,5,17,0,0,79,81,3,10,
        5,0,80,79,1,0,0,0,81,84,1,0,0,0,82,80,1,0,0,0,82,83,1,0,0,0,83,85,
        1,0,0,0,84,82,1,0,0,0,85,86,5,52,0,0,86,13,1,0,0,0,87,89,3,16,8,
        0,88,87,1,0,0,0,89,92,1,0,0,0,90,88,1,0,0,0,90,91,1,0,0,0,91,15,
        1,0,0,0,92,90,1,0,0,0,93,95,5,8,0,0,94,93,1,0,0,0,95,98,1,0,0,0,
        96,94,1,0,0,0,96,97,1,0,0,0,97,102,1,0,0,0,98,96,1,0,0,0,99,101,
        5,7,0,0,100,99,1,0,0,0,101,104,1,0,0,0,102,100,1,0,0,0,102,103,1,
        0,0,0,103,105,1,0,0,0,104,102,1,0,0,0,105,107,5,31,0,0,106,108,3,
        20,10,0,107,106,1,0,0,0,107,108,1,0,0,0,108,110,1,0,0,0,109,111,
        3,18,9,0,110,109,1,0,0,0,110,111,1,0,0,0,111,112,1,0,0,0,112,113,
        5,25,0,0,113,114,3,22,11,0,114,115,5,26,0,0,115,17,1,0,0,0,116,120,
        5,30,0,0,117,119,3,10,5,0,118,117,1,0,0,0,119,122,1,0,0,0,120,118,
        1,0,0,0,120,121,1,0,0,0,121,19,1,0,0,0,122,120,1,0,0,0,123,124,5,
        27,0,0,124,125,5,31,0,0,125,126,5,28,0,0,126,21,1,0,0,0,127,128,
        3,24,12,0,128,23,1,0,0,0,129,134,3,26,13,0,130,131,5,29,0,0,131,
        133,3,26,13,0,132,130,1,0,0,0,133,136,1,0,0,0,134,132,1,0,0,0,134,
        135,1,0,0,0,135,25,1,0,0,0,136,134,1,0,0,0,137,139,3,28,14,0,138,
        137,1,0,0,0,139,142,1,0,0,0,140,138,1,0,0,0,140,141,1,0,0,0,141,
        27,1,0,0,0,142,140,1,0,0,0,143,145,3,30,15,0,144,146,3,20,10,0,145,
        144,1,0,0,0,145,146,1,0,0,0,146,168,1,0,0,0,147,149,3,32,16,0,148,
        147,1,0,0,0,148,149,1,0,0,0,149,150,1,0,0,0,150,152,3,10,5,0,151,
        153,3,20,10,0,152,151,1,0,0,0,152,153,1,0,0,0,153,168,1,0,0,0,154,
        168,3,12,6,0,155,168,5,19,0,0,156,157,5,20,0,0,157,168,3,30,15,0,
        158,159,5,21,0,0,159,168,5,13,0,0,160,161,5,22,0,0,161,168,3,32,
        16,0,162,163,5,23,0,0,163,168,5,13,0,0,164,165,5,24,0,0,165,168,
        5,13,0,0,166,168,5,7,0,0,167,143,1,0,0,0,167,148,1,0,0,0,167,154,
        1,0,0,0,167,155,1,0,0,0,167,156,1,0,0,0,167,158,1,0,0,0,167,160,
        1,0,0,0,167,162,1,0,0,0,167,164,1,0,0,0,167,166,1,0,0,0,168,29,1,
        0,0,0,169,172,5,31,0,0,170,172,5,14,0,0,171,169,1,0,0,0,171,170,
        1,0,0,0,172,31,1,0,0,0,173,177,5,18,0,0,174,176,3,10,5,0,175,174,
        1,0,0,0,176,179,1,0,0,0,177,175,1,0,0,0,177,178,1,0,0,0,178,180,
        1,0,0,0,179,177,1,0,0,0,180,181,5,62,0,0,181,33,1,0,0,0,20,37,49,
        56,66,73,82,90,96,102,107,110,120,134,140,145,148,152,167,171,177
    ]

class BisonParser ( Parser ):

    grammarFileName = "BisonParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'%%'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'%?{'", "'<'", "'%empty'", "'%prec'", "'%dprec'", 
                     "'%merge'", "'%expect'", "'%expect-rr'", "<INVALID>", 
                     "';'", "'['", "']'", "'|'", "'->'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'}'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'>'" ]

    symbolicNames = [ "<INVALID>", "BEGIN_RULES", "PROLOGUE", "PREQUEL_TOKEN_OPTION", 
                      "PREQUEL_TOKEN", "UNTERMINATED_PREQUEL_TOKEN", "BEGIN_PREQUEL_OPTION", 
                      "DOC_COMMENT", "HEADER", "BLOCK_COMMENT", "LINE_COMMENT", 
                      "WS", "ERRCHAR", "INT", "STRING_LITERAL", "UNTERMINATED_STRING_LITERAL", 
                      "BEGIN_ACTION", "BEGIN_PREDICATE", "BEGIN_TAG", "EMPTY", 
                      "PREC", "DPREC", "MERGE", "EXPECT", "EXPECT_RR", "COLON", 
                      "SEMI", "LBRACK", "RBRACK", "OR", "RETURN", "ID", 
                      "EPILOGUE", "MAIN_WS", "PREQUEL_OPTION_NESTED_ACTION", 
                      "PREQUEL_OPTION_ESCAPE", "PREQUEL_OPTION_STRING_LITERAL", 
                      "PREQUEL_OPTION_CHAR_LITERAL", "PREQUEL_OPTION_LIFETIME_LITERAL", 
                      "PREQUEL_OPTION_S_STRING_LITERAL", "PREQUEL_OPTION_BLOCK_COMMENT", 
                      "PREQUEL_OPTION_LINE_COMMENT", "END_PREQUEL_OPTION", 
                      "UNTERMINATED_PREQUEL_OPTION", "PREQUEL_OPTION_CONTENT", 
                      "ACTION_ESCAPE", "ACTION_STRING_LITERAL", "ACTION_CHAR_LITERAL", 
                      "ACTION_LIFETIME_LITERAL", "ACTION_S_STRING_LITERAL", 
                      "ACTION_BLOCK_COMMENT", "ACTION_LINE_COMMENT", "END_ACTION", 
                      "UNTERMINATED_ACTION", "ACTION_CONTENT", "TAG_ESCAPE", 
                      "TAG_STRING_LITERAL", "TAG_CHAR_LITERAL", "TAG_LIFETIME_LITERAL", 
                      "TAG_S_STRING_LITERAL", "TAG_BLOCK_COMMENT", "TAG_LINE_COMMENT", 
                      "END_TAG", "UNTERMINATED_TAG", "TAG_CONTENT", "RETURN_TYPE_ESCAPE", 
                      "RETURN_TYPE_STRING_LITERAL", "RETURN_TYPE_CHAR_LITERAL", 
                      "RETURN_TYPE_LIFETIME_LITERAL", "RETURN_TYPE_S_STRING_LITERAL", 
                      "RETURN_TYPE_BLOCK_COMMENT", "RETURN_TYPE_LINE_COMMENT", 
                      "UNTERMINATED_RETURN_TYPE", "RETURN_TYPE_CONTENT" ]

    RULE_grammarSpec = 0
    RULE_prequelConstruct = 1
    RULE_prequelConstructDoc = 2
    RULE_prequelConstructHeader = 3
    RULE_prequelConstructToken = 4
    RULE_actionBlock = 5
    RULE_predicateBlock = 6
    RULE_rules = 7
    RULE_ruleSpec = 8
    RULE_ruleReturn = 9
    RULE_nameRef = 10
    RULE_ruleBlock = 11
    RULE_ruleAltList = 12
    RULE_alternative = 13
    RULE_element = 14
    RULE_symbol = 15
    RULE_tag = 16

    ruleNames =  [ "grammarSpec", "prequelConstruct", "prequelConstructDoc", 
                   "prequelConstructHeader", "prequelConstructToken", "actionBlock", 
                   "predicateBlock", "rules", "ruleSpec", "ruleReturn", 
                   "nameRef", "ruleBlock", "ruleAltList", "alternative", 
                   "element", "symbol", "tag" ]

    EOF = Token.EOF
    BEGIN_RULES=1
    PROLOGUE=2
    PREQUEL_TOKEN_OPTION=3
    PREQUEL_TOKEN=4
    UNTERMINATED_PREQUEL_TOKEN=5
    BEGIN_PREQUEL_OPTION=6
    DOC_COMMENT=7
    HEADER=8
    BLOCK_COMMENT=9
    LINE_COMMENT=10
    WS=11
    ERRCHAR=12
    INT=13
    STRING_LITERAL=14
    UNTERMINATED_STRING_LITERAL=15
    BEGIN_ACTION=16
    BEGIN_PREDICATE=17
    BEGIN_TAG=18
    EMPTY=19
    PREC=20
    DPREC=21
    MERGE=22
    EXPECT=23
    EXPECT_RR=24
    COLON=25
    SEMI=26
    LBRACK=27
    RBRACK=28
    OR=29
    RETURN=30
    ID=31
    EPILOGUE=32
    MAIN_WS=33
    PREQUEL_OPTION_NESTED_ACTION=34
    PREQUEL_OPTION_ESCAPE=35
    PREQUEL_OPTION_STRING_LITERAL=36
    PREQUEL_OPTION_CHAR_LITERAL=37
    PREQUEL_OPTION_LIFETIME_LITERAL=38
    PREQUEL_OPTION_S_STRING_LITERAL=39
    PREQUEL_OPTION_BLOCK_COMMENT=40
    PREQUEL_OPTION_LINE_COMMENT=41
    END_PREQUEL_OPTION=42
    UNTERMINATED_PREQUEL_OPTION=43
    PREQUEL_OPTION_CONTENT=44
    ACTION_ESCAPE=45
    ACTION_STRING_LITERAL=46
    ACTION_CHAR_LITERAL=47
    ACTION_LIFETIME_LITERAL=48
    ACTION_S_STRING_LITERAL=49
    ACTION_BLOCK_COMMENT=50
    ACTION_LINE_COMMENT=51
    END_ACTION=52
    UNTERMINATED_ACTION=53
    ACTION_CONTENT=54
    TAG_ESCAPE=55
    TAG_STRING_LITERAL=56
    TAG_CHAR_LITERAL=57
    TAG_LIFETIME_LITERAL=58
    TAG_S_STRING_LITERAL=59
    TAG_BLOCK_COMMENT=60
    TAG_LINE_COMMENT=61
    END_TAG=62
    UNTERMINATED_TAG=63
    TAG_CONTENT=64
    RETURN_TYPE_ESCAPE=65
    RETURN_TYPE_STRING_LITERAL=66
    RETURN_TYPE_CHAR_LITERAL=67
    RETURN_TYPE_LIFETIME_LITERAL=68
    RETURN_TYPE_S_STRING_LITERAL=69
    RETURN_TYPE_BLOCK_COMMENT=70
    RETURN_TYPE_LINE_COMMENT=71
    UNTERMINATED_RETURN_TYPE=72
    RETURN_TYPE_CONTENT=73

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class GrammarSpecContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_RULES(self):
            return self.getToken(BisonParser.BEGIN_RULES, 0)

        def rules(self):
            return self.getTypedRuleContext(BisonParser.RulesContext,0)


        def EOF(self):
            return self.getToken(BisonParser.EOF, 0)

        def prequelConstruct(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BisonParser.PrequelConstructContext)
            else:
                return self.getTypedRuleContext(BisonParser.PrequelConstructContext,i)


        def getRuleIndex(self):
            return BisonParser.RULE_grammarSpec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGrammarSpec" ):
                listener.enterGrammarSpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGrammarSpec" ):
                listener.exitGrammarSpec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGrammarSpec" ):
                return visitor.visitGrammarSpec(self)
            else:
                return visitor.visitChildren(self)




    def grammarSpec(self):

        localctx = BisonParser.GrammarSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_grammarSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 460) != 0):
                self.state = 34
                self.prequelConstruct()
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 40
            self.match(BisonParser.BEGIN_RULES)
            self.state = 41
            self.rules()
            self.state = 42
            self.match(BisonParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrequelConstructContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROLOGUE(self):
            return self.getToken(BisonParser.PROLOGUE, 0)

        def BEGIN_PREQUEL_OPTION(self):
            return self.getToken(BisonParser.BEGIN_PREQUEL_OPTION, 0)

        def END_PREQUEL_OPTION(self):
            return self.getToken(BisonParser.END_PREQUEL_OPTION, 0)

        def actionBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BisonParser.ActionBlockContext)
            else:
                return self.getTypedRuleContext(BisonParser.ActionBlockContext,i)


        def prequelConstructToken(self):
            return self.getTypedRuleContext(BisonParser.PrequelConstructTokenContext,0)


        def prequelConstructDoc(self):
            return self.getTypedRuleContext(BisonParser.PrequelConstructDocContext,0)


        def prequelConstructHeader(self):
            return self.getTypedRuleContext(BisonParser.PrequelConstructHeaderContext,0)


        def getRuleIndex(self):
            return BisonParser.RULE_prequelConstruct

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrequelConstruct" ):
                listener.enterPrequelConstruct(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrequelConstruct" ):
                listener.exitPrequelConstruct(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrequelConstruct" ):
                return visitor.visitPrequelConstruct(self)
            else:
                return visitor.visitChildren(self)




    def prequelConstruct(self):

        localctx = BisonParser.PrequelConstructContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_prequelConstruct)
        self._la = 0 # Token type
        try:
            self.state = 56
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 44
                self.match(BisonParser.PROLOGUE)
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 45
                self.match(BisonParser.BEGIN_PREQUEL_OPTION)
                self.state = 49
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==16:
                    self.state = 46
                    self.actionBlock()
                    self.state = 51
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 52
                self.match(BisonParser.END_PREQUEL_OPTION)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 3)
                self.state = 53
                self.prequelConstructToken()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 4)
                self.state = 54
                self.prequelConstructDoc()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 5)
                self.state = 55
                self.prequelConstructHeader()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrequelConstructDocContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.doc = None # type: Token

        def DOC_COMMENT(self):
            return self.getToken(BisonParser.DOC_COMMENT, 0)

        def getRuleIndex(self):
            return BisonParser.RULE_prequelConstructDoc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrequelConstructDoc" ):
                listener.enterPrequelConstructDoc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrequelConstructDoc" ):
                listener.exitPrequelConstructDoc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrequelConstructDoc" ):
                return visitor.visitPrequelConstructDoc(self)
            else:
                return visitor.visitChildren(self)




    def prequelConstructDoc(self):

        localctx = BisonParser.PrequelConstructDocContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_prequelConstructDoc)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            localctx.doc = self.match(BisonParser.DOC_COMMENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrequelConstructHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.header = None # type: Token

        def HEADER(self):
            return self.getToken(BisonParser.HEADER, 0)

        def getRuleIndex(self):
            return BisonParser.RULE_prequelConstructHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrequelConstructHeader" ):
                listener.enterPrequelConstructHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrequelConstructHeader" ):
                listener.exitPrequelConstructHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrequelConstructHeader" ):
                return visitor.visitPrequelConstructHeader(self)
            else:
                return visitor.visitChildren(self)




    def prequelConstructHeader(self):

        localctx = BisonParser.PrequelConstructHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_prequelConstructHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            localctx.header = self.match(BisonParser.HEADER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrequelConstructTokenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # type: Token
            self._PREQUEL_TOKEN = None # type: Token
            self.tokens = list() # type: list[Token]

        def PREQUEL_TOKEN_OPTION(self):
            return self.getToken(BisonParser.PREQUEL_TOKEN_OPTION, 0)

        def PREQUEL_TOKEN(self, i:int=None):
            if i is None:
                return self.getTokens(BisonParser.PREQUEL_TOKEN)
            else:
                return self.getToken(BisonParser.PREQUEL_TOKEN, i)

        def getRuleIndex(self):
            return BisonParser.RULE_prequelConstructToken

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrequelConstructToken" ):
                listener.enterPrequelConstructToken(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrequelConstructToken" ):
                listener.exitPrequelConstructToken(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrequelConstructToken" ):
                return visitor.visitPrequelConstructToken(self)
            else:
                return visitor.visitChildren(self)




    def prequelConstructToken(self):

        localctx = BisonParser.PrequelConstructTokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_prequelConstructToken)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            localctx.name = self.match(BisonParser.PREQUEL_TOKEN_OPTION)
            self.state = 66
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==4:
                self.state = 63
                localctx._PREQUEL_TOKEN = self.match(BisonParser.PREQUEL_TOKEN)
                localctx.tokens.append(localctx._PREQUEL_TOKEN)
                self.state = 68
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ActionBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_ACTION(self):
            return self.getToken(BisonParser.BEGIN_ACTION, 0)

        def END_ACTION(self):
            return self.getToken(BisonParser.END_ACTION, 0)

        def actionBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BisonParser.ActionBlockContext)
            else:
                return self.getTypedRuleContext(BisonParser.ActionBlockContext,i)


        def getRuleIndex(self):
            return BisonParser.RULE_actionBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterActionBlock" ):
                listener.enterActionBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitActionBlock" ):
                listener.exitActionBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitActionBlock" ):
                return visitor.visitActionBlock(self)
            else:
                return visitor.visitChildren(self)




    def actionBlock(self):

        localctx = BisonParser.ActionBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_actionBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(BisonParser.BEGIN_ACTION)
            self.state = 73
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 70
                self.actionBlock()
                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 76
            self.match(BisonParser.END_ACTION)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PredicateBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_PREDICATE(self):
            return self.getToken(BisonParser.BEGIN_PREDICATE, 0)

        def END_ACTION(self):
            return self.getToken(BisonParser.END_ACTION, 0)

        def actionBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BisonParser.ActionBlockContext)
            else:
                return self.getTypedRuleContext(BisonParser.ActionBlockContext,i)


        def getRuleIndex(self):
            return BisonParser.RULE_predicateBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicateBlock" ):
                listener.enterPredicateBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicateBlock" ):
                listener.exitPredicateBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPredicateBlock" ):
                return visitor.visitPredicateBlock(self)
            else:
                return visitor.visitChildren(self)




    def predicateBlock(self):

        localctx = BisonParser.PredicateBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_predicateBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78
            self.match(BisonParser.BEGIN_PREDICATE)
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 79
                self.actionBlock()
                self.state = 84
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 85
            self.match(BisonParser.END_ACTION)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RulesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ruleSpec(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BisonParser.RuleSpecContext)
            else:
                return self.getTypedRuleContext(BisonParser.RuleSpecContext,i)


        def getRuleIndex(self):
            return BisonParser.RULE_rules

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRules" ):
                listener.enterRules(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRules" ):
                listener.exitRules(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRules" ):
                return visitor.visitRules(self)
            else:
                return visitor.visitChildren(self)




    def rules(self):

        localctx = BisonParser.RulesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_rules)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2147484032) != 0):
                self.state = 87
                self.ruleSpec()
                self.state = 92
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleSpecContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._HEADER = None # type: Token
            self.headers = list() # type: list[Token]
            self._DOC_COMMENT = None # type: Token
            self.docs = list() # type: list[Token]
            self.name = None # type: Token

        def COLON(self):
            return self.getToken(BisonParser.COLON, 0)

        def ruleBlock(self):
            return self.getTypedRuleContext(BisonParser.RuleBlockContext,0)


        def SEMI(self):
            return self.getToken(BisonParser.SEMI, 0)

        def ID(self):
            return self.getToken(BisonParser.ID, 0)

        def nameRef(self):
            return self.getTypedRuleContext(BisonParser.NameRefContext,0)


        def ruleReturn(self):
            return self.getTypedRuleContext(BisonParser.RuleReturnContext,0)


        def HEADER(self, i:int=None):
            if i is None:
                return self.getTokens(BisonParser.HEADER)
            else:
                return self.getToken(BisonParser.HEADER, i)

        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(BisonParser.DOC_COMMENT)
            else:
                return self.getToken(BisonParser.DOC_COMMENT, i)

        def getRuleIndex(self):
            return BisonParser.RULE_ruleSpec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleSpec" ):
                listener.enterRuleSpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleSpec" ):
                listener.exitRuleSpec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRuleSpec" ):
                return visitor.visitRuleSpec(self)
            else:
                return visitor.visitChildren(self)




    def ruleSpec(self):

        localctx = BisonParser.RuleSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_ruleSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==8:
                self.state = 93
                localctx._HEADER = self.match(BisonParser.HEADER)
                localctx.headers.append(localctx._HEADER)
                self.state = 98
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==7:
                self.state = 99
                localctx._DOC_COMMENT = self.match(BisonParser.DOC_COMMENT)
                localctx.docs.append(localctx._DOC_COMMENT)
                self.state = 104
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 105
            localctx.name = self.match(BisonParser.ID)
            self.state = 107
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==27:
                self.state = 106
                self.nameRef()


            self.state = 110
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==30:
                self.state = 109
                self.ruleReturn()


            self.state = 112
            self.match(BisonParser.COLON)
            self.state = 113
            self.ruleBlock()
            self.state = 114
            self.match(BisonParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleReturnContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(BisonParser.RETURN, 0)

        def actionBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BisonParser.ActionBlockContext)
            else:
                return self.getTypedRuleContext(BisonParser.ActionBlockContext,i)


        def getRuleIndex(self):
            return BisonParser.RULE_ruleReturn

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleReturn" ):
                listener.enterRuleReturn(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleReturn" ):
                listener.exitRuleReturn(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRuleReturn" ):
                return visitor.visitRuleReturn(self)
            else:
                return visitor.visitChildren(self)




    def ruleReturn(self):

        localctx = BisonParser.RuleReturnContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_ruleReturn)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.match(BisonParser.RETURN)
            self.state = 120
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 117
                self.actionBlock()
                self.state = 122
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NameRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACK(self):
            return self.getToken(BisonParser.LBRACK, 0)

        def ID(self):
            return self.getToken(BisonParser.ID, 0)

        def RBRACK(self):
            return self.getToken(BisonParser.RBRACK, 0)

        def getRuleIndex(self):
            return BisonParser.RULE_nameRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNameRef" ):
                listener.enterNameRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNameRef" ):
                listener.exitNameRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNameRef" ):
                return visitor.visitNameRef(self)
            else:
                return visitor.visitChildren(self)




    def nameRef(self):

        localctx = BisonParser.NameRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_nameRef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 123
            self.match(BisonParser.LBRACK)
            self.state = 124
            self.match(BisonParser.ID)
            self.state = 125
            self.match(BisonParser.RBRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ruleAltList(self):
            return self.getTypedRuleContext(BisonParser.RuleAltListContext,0)


        def getRuleIndex(self):
            return BisonParser.RULE_ruleBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleBlock" ):
                listener.enterRuleBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleBlock" ):
                listener.exitRuleBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRuleBlock" ):
                return visitor.visitRuleBlock(self)
            else:
                return visitor.visitChildren(self)




    def ruleBlock(self):

        localctx = BisonParser.RuleBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_ruleBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.ruleAltList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleAltListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._alternative = None # type: BisonParser.AlternativeContext
            self.alts = list() # type: list[BisonParser.AlternativeContext]

        def alternative(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BisonParser.AlternativeContext)
            else:
                return self.getTypedRuleContext(BisonParser.AlternativeContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(BisonParser.OR)
            else:
                return self.getToken(BisonParser.OR, i)

        def getRuleIndex(self):
            return BisonParser.RULE_ruleAltList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleAltList" ):
                listener.enterRuleAltList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleAltList" ):
                listener.exitRuleAltList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRuleAltList" ):
                return visitor.visitRuleAltList(self)
            else:
                return visitor.visitChildren(self)




    def ruleAltList(self):

        localctx = BisonParser.RuleAltListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_ruleAltList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
            localctx._alternative = self.alternative()
            localctx.alts.append(localctx._alternative)
            self.state = 134
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==29:
                self.state = 130
                self.match(BisonParser.OR)
                self.state = 131
                localctx._alternative = self.alternative()
                localctx.alts.append(localctx._alternative)
                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AlternativeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._element = None # type: BisonParser.ElementContext
            self.elements = list() # type: list[BisonParser.ElementContext]

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BisonParser.ElementContext)
            else:
                return self.getTypedRuleContext(BisonParser.ElementContext,i)


        def getRuleIndex(self):
            return BisonParser.RULE_alternative

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAlternative" ):
                listener.enterAlternative(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAlternative" ):
                listener.exitAlternative(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAlternative" ):
                return visitor.visitAlternative(self)
            else:
                return visitor.visitChildren(self)




    def alternative(self):

        localctx = BisonParser.AlternativeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_alternative)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2180989056) != 0):
                self.state = 137
                localctx._element = self.element()
                localctx.elements.append(localctx._element)
                self.state = 142
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return BisonParser.RULE_element

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ElementSymbolContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def symbol(self):
            return self.getTypedRuleContext(BisonParser.SymbolContext,0)

        def nameRef(self):
            return self.getTypedRuleContext(BisonParser.NameRefContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementSymbol" ):
                listener.enterElementSymbol(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementSymbol" ):
                listener.exitElementSymbol(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementSymbol" ):
                return visitor.visitElementSymbol(self)
            else:
                return visitor.visitChildren(self)


    class ElementDPrecContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DPREC(self):
            return self.getToken(BisonParser.DPREC, 0)
        def INT(self):
            return self.getToken(BisonParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementDPrec" ):
                listener.enterElementDPrec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementDPrec" ):
                listener.exitElementDPrec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementDPrec" ):
                return visitor.visitElementDPrec(self)
            else:
                return visitor.visitChildren(self)


    class ElementExpectContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def EXPECT(self):
            return self.getToken(BisonParser.EXPECT, 0)
        def INT(self):
            return self.getToken(BisonParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementExpect" ):
                listener.enterElementExpect(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementExpect" ):
                listener.exitElementExpect(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementExpect" ):
                return visitor.visitElementExpect(self)
            else:
                return visitor.visitChildren(self)


    class ElementPredicateBlockContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def predicateBlock(self):
            return self.getTypedRuleContext(BisonParser.PredicateBlockContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementPredicateBlock" ):
                listener.enterElementPredicateBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementPredicateBlock" ):
                listener.exitElementPredicateBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementPredicateBlock" ):
                return visitor.visitElementPredicateBlock(self)
            else:
                return visitor.visitChildren(self)


    class ElementEmptyContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def EMPTY(self):
            return self.getToken(BisonParser.EMPTY, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementEmpty" ):
                listener.enterElementEmpty(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementEmpty" ):
                listener.exitElementEmpty(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementEmpty" ):
                return visitor.visitElementEmpty(self)
            else:
                return visitor.visitChildren(self)


    class ElementPrecContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PREC(self):
            return self.getToken(BisonParser.PREC, 0)
        def symbol(self):
            return self.getTypedRuleContext(BisonParser.SymbolContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementPrec" ):
                listener.enterElementPrec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementPrec" ):
                listener.exitElementPrec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementPrec" ):
                return visitor.visitElementPrec(self)
            else:
                return visitor.visitChildren(self)


    class ElementExpectRrContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def EXPECT_RR(self):
            return self.getToken(BisonParser.EXPECT_RR, 0)
        def INT(self):
            return self.getToken(BisonParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementExpectRr" ):
                listener.enterElementExpectRr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementExpectRr" ):
                listener.exitElementExpectRr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementExpectRr" ):
                return visitor.visitElementExpectRr(self)
            else:
                return visitor.visitChildren(self)


    class ElementInlineDocContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.ElementContext
            super().__init__(parser)
            self.value = None # type: Token
            self.copyFrom(ctx)

        def DOC_COMMENT(self):
            return self.getToken(BisonParser.DOC_COMMENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementInlineDoc" ):
                listener.enterElementInlineDoc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementInlineDoc" ):
                listener.exitElementInlineDoc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementInlineDoc" ):
                return visitor.visitElementInlineDoc(self)
            else:
                return visitor.visitChildren(self)


    class ElementActionBlockContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def actionBlock(self):
            return self.getTypedRuleContext(BisonParser.ActionBlockContext,0)

        def tag(self):
            return self.getTypedRuleContext(BisonParser.TagContext,0)

        def nameRef(self):
            return self.getTypedRuleContext(BisonParser.NameRefContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementActionBlock" ):
                listener.enterElementActionBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementActionBlock" ):
                listener.exitElementActionBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementActionBlock" ):
                return visitor.visitElementActionBlock(self)
            else:
                return visitor.visitChildren(self)


    class ElementMergeContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def MERGE(self):
            return self.getToken(BisonParser.MERGE, 0)
        def tag(self):
            return self.getTypedRuleContext(BisonParser.TagContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementMerge" ):
                listener.enterElementMerge(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementMerge" ):
                listener.exitElementMerge(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementMerge" ):
                return visitor.visitElementMerge(self)
            else:
                return visitor.visitChildren(self)



    def element(self):

        localctx = BisonParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_element)
        self._la = 0 # Token type
        try:
            self.state = 167
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [14, 31]:
                localctx = BisonParser.ElementSymbolContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 143
                self.symbol()
                self.state = 145
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==27:
                    self.state = 144
                    self.nameRef()


                pass
            elif token in [16, 18]:
                localctx = BisonParser.ElementActionBlockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 148
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==18:
                    self.state = 147
                    self.tag()


                self.state = 150
                self.actionBlock()
                self.state = 152
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==27:
                    self.state = 151
                    self.nameRef()


                pass
            elif token in [17]:
                localctx = BisonParser.ElementPredicateBlockContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 154
                self.predicateBlock()
                pass
            elif token in [19]:
                localctx = BisonParser.ElementEmptyContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 155
                self.match(BisonParser.EMPTY)
                pass
            elif token in [20]:
                localctx = BisonParser.ElementPrecContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 156
                self.match(BisonParser.PREC)
                self.state = 157
                self.symbol()
                pass
            elif token in [21]:
                localctx = BisonParser.ElementDPrecContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 158
                self.match(BisonParser.DPREC)
                self.state = 159
                self.match(BisonParser.INT)
                pass
            elif token in [22]:
                localctx = BisonParser.ElementMergeContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 160
                self.match(BisonParser.MERGE)
                self.state = 161
                self.tag()
                pass
            elif token in [23]:
                localctx = BisonParser.ElementExpectContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 162
                self.match(BisonParser.EXPECT)
                self.state = 163
                self.match(BisonParser.INT)
                pass
            elif token in [24]:
                localctx = BisonParser.ElementExpectRrContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 164
                self.match(BisonParser.EXPECT_RR)
                self.state = 165
                self.match(BisonParser.INT)
                pass
            elif token in [7]:
                localctx = BisonParser.ElementInlineDocContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 166
                localctx.value = self.match(BisonParser.DOC_COMMENT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SymbolContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return BisonParser.RULE_symbol

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SymbolIdContext(SymbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.SymbolContext
            super().__init__(parser)
            self.name = None # type: Token
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(BisonParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSymbolId" ):
                listener.enterSymbolId(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSymbolId" ):
                listener.exitSymbolId(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSymbolId" ):
                return visitor.visitSymbolId(self)
            else:
                return visitor.visitChildren(self)


    class SymbolLiteralContext(SymbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BisonParser.SymbolContext
            super().__init__(parser)
            self.content = None # type: Token
            self.copyFrom(ctx)

        def STRING_LITERAL(self):
            return self.getToken(BisonParser.STRING_LITERAL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSymbolLiteral" ):
                listener.enterSymbolLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSymbolLiteral" ):
                listener.exitSymbolLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSymbolLiteral" ):
                return visitor.visitSymbolLiteral(self)
            else:
                return visitor.visitChildren(self)



    def symbol(self):

        localctx = BisonParser.SymbolContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_symbol)
        try:
            self.state = 171
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [31]:
                localctx = BisonParser.SymbolIdContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 169
                localctx.name = self.match(BisonParser.ID)
                pass
            elif token in [14]:
                localctx = BisonParser.SymbolLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 170
                localctx.content = self.match(BisonParser.STRING_LITERAL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TagContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_TAG(self):
            return self.getToken(BisonParser.BEGIN_TAG, 0)

        def END_TAG(self):
            return self.getToken(BisonParser.END_TAG, 0)

        def actionBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BisonParser.ActionBlockContext)
            else:
                return self.getTypedRuleContext(BisonParser.ActionBlockContext,i)


        def getRuleIndex(self):
            return BisonParser.RULE_tag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTag" ):
                listener.enterTag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTag" ):
                listener.exitTag(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTag" ):
                return visitor.visitTag(self)
            else:
                return visitor.visitChildren(self)




    def tag(self):

        localctx = BisonParser.TagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_tag)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 173
            self.match(BisonParser.BEGIN_TAG)
            self.state = 177
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 174
                self.actionBlock()
                self.state = 179
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 180
            self.match(BisonParser.END_TAG)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





