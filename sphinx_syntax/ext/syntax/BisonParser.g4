parser grammar BisonParser;

options {
    tokenVocab = BisonLexer;
}

grammarSpec
   : prequelConstruct* BEGIN_RULES rules EOF
   ;

prequelConstruct
   : PROLOGUE
   | BEGIN_PREQUEL_OPTION actionBlock* END_PREQUEL_OPTION
   | prequelConstructToken
   | prequelConstructDoc
   | prequelConstructHeader
   ;

prequelConstructDoc
    : doc=DOC_COMMENT
    ;


prequelConstructHeader
    : header=HEADER
    ;

prequelConstructToken
   : name=PREQUEL_TOKEN_OPTION tokens+=PREQUEL_TOKEN*
   ;

actionBlock
   : BEGIN_ACTION actionBlock* END_ACTION
   ;

predicateBlock
   : BEGIN_PREDICATE actionBlock* END_ACTION
   ;

rules
   : ruleSpec*
   ;

ruleSpec
   : headers+=HEADER* docs+=DOC_COMMENT* name=ID nameRef? ruleReturn? COLON ruleBlock SEMI
   ;

ruleReturn
   : RETURN actionBlock*
   ;

nameRef
   : LBRACK ID RBRACK
   ;

ruleBlock
   : ruleAltList
   ;

ruleAltList
   : alts+=alternative (OR alts+=alternative)*
   ;

alternative
   : elements+=element*
   ;

element
   : symbol nameRef? # elementSymbol
   | tag? actionBlock nameRef? # elementActionBlock
   | predicateBlock # elementPredicateBlock
   | EMPTY # elementEmpty
   | PREC symbol # elementPrec
   | DPREC INT # elementDPrec
   | MERGE tag # elementMerge
   | EXPECT INT # elementExpect
   | EXPECT_RR INT # elementExpectRr
   | value=DOC_COMMENT # elementInlineDoc
   ;

symbol
   : name=ID #symbolId
   | content=STRING_LITERAL #symbolLiteral
   ;

tag
   : BEGIN_TAG actionBlock* END_TAG
   ;
