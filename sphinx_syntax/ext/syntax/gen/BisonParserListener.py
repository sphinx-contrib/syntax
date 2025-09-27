# Generated from BisonParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .BisonParser import BisonParser
else:
    from BisonParser import BisonParser

# This class defines a complete listener for a parse tree produced by BisonParser.
class BisonParserListener(ParseTreeListener):

    # Enter a parse tree produced by BisonParser#grammarSpec.
    def enterGrammarSpec(self, ctx:BisonParser.GrammarSpecContext):
        pass

    # Exit a parse tree produced by BisonParser#grammarSpec.
    def exitGrammarSpec(self, ctx:BisonParser.GrammarSpecContext):
        pass


    # Enter a parse tree produced by BisonParser#prequelConstruct.
    def enterPrequelConstruct(self, ctx:BisonParser.PrequelConstructContext):
        pass

    # Exit a parse tree produced by BisonParser#prequelConstruct.
    def exitPrequelConstruct(self, ctx:BisonParser.PrequelConstructContext):
        pass


    # Enter a parse tree produced by BisonParser#prequelConstructDoc.
    def enterPrequelConstructDoc(self, ctx:BisonParser.PrequelConstructDocContext):
        pass

    # Exit a parse tree produced by BisonParser#prequelConstructDoc.
    def exitPrequelConstructDoc(self, ctx:BisonParser.PrequelConstructDocContext):
        pass


    # Enter a parse tree produced by BisonParser#prequelConstructHeader.
    def enterPrequelConstructHeader(self, ctx:BisonParser.PrequelConstructHeaderContext):
        pass

    # Exit a parse tree produced by BisonParser#prequelConstructHeader.
    def exitPrequelConstructHeader(self, ctx:BisonParser.PrequelConstructHeaderContext):
        pass


    # Enter a parse tree produced by BisonParser#prequelConstructToken.
    def enterPrequelConstructToken(self, ctx:BisonParser.PrequelConstructTokenContext):
        pass

    # Exit a parse tree produced by BisonParser#prequelConstructToken.
    def exitPrequelConstructToken(self, ctx:BisonParser.PrequelConstructTokenContext):
        pass


    # Enter a parse tree produced by BisonParser#actionBlock.
    def enterActionBlock(self, ctx:BisonParser.ActionBlockContext):
        pass

    # Exit a parse tree produced by BisonParser#actionBlock.
    def exitActionBlock(self, ctx:BisonParser.ActionBlockContext):
        pass


    # Enter a parse tree produced by BisonParser#predicateBlock.
    def enterPredicateBlock(self, ctx:BisonParser.PredicateBlockContext):
        pass

    # Exit a parse tree produced by BisonParser#predicateBlock.
    def exitPredicateBlock(self, ctx:BisonParser.PredicateBlockContext):
        pass


    # Enter a parse tree produced by BisonParser#rules.
    def enterRules(self, ctx:BisonParser.RulesContext):
        pass

    # Exit a parse tree produced by BisonParser#rules.
    def exitRules(self, ctx:BisonParser.RulesContext):
        pass


    # Enter a parse tree produced by BisonParser#ruleSpec.
    def enterRuleSpec(self, ctx:BisonParser.RuleSpecContext):
        pass

    # Exit a parse tree produced by BisonParser#ruleSpec.
    def exitRuleSpec(self, ctx:BisonParser.RuleSpecContext):
        pass


    # Enter a parse tree produced by BisonParser#ruleReturn.
    def enterRuleReturn(self, ctx:BisonParser.RuleReturnContext):
        pass

    # Exit a parse tree produced by BisonParser#ruleReturn.
    def exitRuleReturn(self, ctx:BisonParser.RuleReturnContext):
        pass


    # Enter a parse tree produced by BisonParser#nameRef.
    def enterNameRef(self, ctx:BisonParser.NameRefContext):
        pass

    # Exit a parse tree produced by BisonParser#nameRef.
    def exitNameRef(self, ctx:BisonParser.NameRefContext):
        pass


    # Enter a parse tree produced by BisonParser#ruleBlock.
    def enterRuleBlock(self, ctx:BisonParser.RuleBlockContext):
        pass

    # Exit a parse tree produced by BisonParser#ruleBlock.
    def exitRuleBlock(self, ctx:BisonParser.RuleBlockContext):
        pass


    # Enter a parse tree produced by BisonParser#ruleAltList.
    def enterRuleAltList(self, ctx:BisonParser.RuleAltListContext):
        pass

    # Exit a parse tree produced by BisonParser#ruleAltList.
    def exitRuleAltList(self, ctx:BisonParser.RuleAltListContext):
        pass


    # Enter a parse tree produced by BisonParser#alternative.
    def enterAlternative(self, ctx:BisonParser.AlternativeContext):
        pass

    # Exit a parse tree produced by BisonParser#alternative.
    def exitAlternative(self, ctx:BisonParser.AlternativeContext):
        pass


    # Enter a parse tree produced by BisonParser#elementSymbol.
    def enterElementSymbol(self, ctx:BisonParser.ElementSymbolContext):
        pass

    # Exit a parse tree produced by BisonParser#elementSymbol.
    def exitElementSymbol(self, ctx:BisonParser.ElementSymbolContext):
        pass


    # Enter a parse tree produced by BisonParser#elementActionBlock.
    def enterElementActionBlock(self, ctx:BisonParser.ElementActionBlockContext):
        pass

    # Exit a parse tree produced by BisonParser#elementActionBlock.
    def exitElementActionBlock(self, ctx:BisonParser.ElementActionBlockContext):
        pass


    # Enter a parse tree produced by BisonParser#elementPredicateBlock.
    def enterElementPredicateBlock(self, ctx:BisonParser.ElementPredicateBlockContext):
        pass

    # Exit a parse tree produced by BisonParser#elementPredicateBlock.
    def exitElementPredicateBlock(self, ctx:BisonParser.ElementPredicateBlockContext):
        pass


    # Enter a parse tree produced by BisonParser#elementEmpty.
    def enterElementEmpty(self, ctx:BisonParser.ElementEmptyContext):
        pass

    # Exit a parse tree produced by BisonParser#elementEmpty.
    def exitElementEmpty(self, ctx:BisonParser.ElementEmptyContext):
        pass


    # Enter a parse tree produced by BisonParser#elementPrec.
    def enterElementPrec(self, ctx:BisonParser.ElementPrecContext):
        pass

    # Exit a parse tree produced by BisonParser#elementPrec.
    def exitElementPrec(self, ctx:BisonParser.ElementPrecContext):
        pass


    # Enter a parse tree produced by BisonParser#elementDPrec.
    def enterElementDPrec(self, ctx:BisonParser.ElementDPrecContext):
        pass

    # Exit a parse tree produced by BisonParser#elementDPrec.
    def exitElementDPrec(self, ctx:BisonParser.ElementDPrecContext):
        pass


    # Enter a parse tree produced by BisonParser#elementMerge.
    def enterElementMerge(self, ctx:BisonParser.ElementMergeContext):
        pass

    # Exit a parse tree produced by BisonParser#elementMerge.
    def exitElementMerge(self, ctx:BisonParser.ElementMergeContext):
        pass


    # Enter a parse tree produced by BisonParser#elementExpect.
    def enterElementExpect(self, ctx:BisonParser.ElementExpectContext):
        pass

    # Exit a parse tree produced by BisonParser#elementExpect.
    def exitElementExpect(self, ctx:BisonParser.ElementExpectContext):
        pass


    # Enter a parse tree produced by BisonParser#elementExpectRr.
    def enterElementExpectRr(self, ctx:BisonParser.ElementExpectRrContext):
        pass

    # Exit a parse tree produced by BisonParser#elementExpectRr.
    def exitElementExpectRr(self, ctx:BisonParser.ElementExpectRrContext):
        pass


    # Enter a parse tree produced by BisonParser#elementInlineDoc.
    def enterElementInlineDoc(self, ctx:BisonParser.ElementInlineDocContext):
        pass

    # Exit a parse tree produced by BisonParser#elementInlineDoc.
    def exitElementInlineDoc(self, ctx:BisonParser.ElementInlineDocContext):
        pass


    # Enter a parse tree produced by BisonParser#symbolId.
    def enterSymbolId(self, ctx:BisonParser.SymbolIdContext):
        pass

    # Exit a parse tree produced by BisonParser#symbolId.
    def exitSymbolId(self, ctx:BisonParser.SymbolIdContext):
        pass


    # Enter a parse tree produced by BisonParser#symbolLiteral.
    def enterSymbolLiteral(self, ctx:BisonParser.SymbolLiteralContext):
        pass

    # Exit a parse tree produced by BisonParser#symbolLiteral.
    def exitSymbolLiteral(self, ctx:BisonParser.SymbolLiteralContext):
        pass


    # Enter a parse tree produced by BisonParser#tag.
    def enterTag(self, ctx:BisonParser.TagContext):
        pass

    # Exit a parse tree produced by BisonParser#tag.
    def exitTag(self, ctx:BisonParser.TagContext):
        pass



del BisonParser