# Generated from BisonParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .BisonParser import BisonParser
else:
    from BisonParser import BisonParser

# This class defines a complete generic visitor for a parse tree produced by BisonParser.

class BisonParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BisonParser#grammarSpec.
    def visitGrammarSpec(self, ctx:BisonParser.GrammarSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#prequelConstruct.
    def visitPrequelConstruct(self, ctx:BisonParser.PrequelConstructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#prequelConstructDoc.
    def visitPrequelConstructDoc(self, ctx:BisonParser.PrequelConstructDocContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#prequelConstructHeader.
    def visitPrequelConstructHeader(self, ctx:BisonParser.PrequelConstructHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#prequelConstructToken.
    def visitPrequelConstructToken(self, ctx:BisonParser.PrequelConstructTokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#actionBlock.
    def visitActionBlock(self, ctx:BisonParser.ActionBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#predicateBlock.
    def visitPredicateBlock(self, ctx:BisonParser.PredicateBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#rules.
    def visitRules(self, ctx:BisonParser.RulesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#ruleSpec.
    def visitRuleSpec(self, ctx:BisonParser.RuleSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#ruleReturn.
    def visitRuleReturn(self, ctx:BisonParser.RuleReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#nameRef.
    def visitNameRef(self, ctx:BisonParser.NameRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#ruleBlock.
    def visitRuleBlock(self, ctx:BisonParser.RuleBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#ruleAltList.
    def visitRuleAltList(self, ctx:BisonParser.RuleAltListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#alternative.
    def visitAlternative(self, ctx:BisonParser.AlternativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#elementSymbol.
    def visitElementSymbol(self, ctx:BisonParser.ElementSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#elementActionBlock.
    def visitElementActionBlock(self, ctx:BisonParser.ElementActionBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#elementPredicateBlock.
    def visitElementPredicateBlock(self, ctx:BisonParser.ElementPredicateBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#elementEmpty.
    def visitElementEmpty(self, ctx:BisonParser.ElementEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#elementPrec.
    def visitElementPrec(self, ctx:BisonParser.ElementPrecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#elementDPrec.
    def visitElementDPrec(self, ctx:BisonParser.ElementDPrecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#elementMerge.
    def visitElementMerge(self, ctx:BisonParser.ElementMergeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#elementExpect.
    def visitElementExpect(self, ctx:BisonParser.ElementExpectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#elementExpectRr.
    def visitElementExpectRr(self, ctx:BisonParser.ElementExpectRrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#elementInlineDoc.
    def visitElementInlineDoc(self, ctx:BisonParser.ElementInlineDocContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#symbolId.
    def visitSymbolId(self, ctx:BisonParser.SymbolIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#symbolLiteral.
    def visitSymbolLiteral(self, ctx:BisonParser.SymbolLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BisonParser#tag.
    def visitTag(self, ctx:BisonParser.TagContext):
        return self.visitChildren(ctx)



del BisonParser