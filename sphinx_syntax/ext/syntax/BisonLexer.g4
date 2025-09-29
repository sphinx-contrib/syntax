lexer grammar BisonLexer;

options {
    superClass = BisonLexerBase ;
}

import LexBasic;

// ======================================================
// Prequel mode
//


// -------------------------
// Mode marker

BEGIN_RULES
    : '%%'                          -> mode(Main)
    ;


// -------------------------
// Prequel contents

PROLOGUE
    : '%{' .*? '%}'
    ;
PREQUEL_TOKEN_OPTION
    : '%left'
    | '%right'
    | '%nonassoc'
    | '%precedence'
    | '%token'
    | '//@' Hws* '%token' ~[\r\n\f]*
    | '%epp'
    ;
PREQUEL_TOKEN
    : Id
    | SQuoteLiteral
    | DQuoteLiteral
    ;
UNTERMINATED_PREQUEL_TOKEN
    : USQuoteLiteral
    | UDQuoteLiteral
    ;
BEGIN_PREQUEL_OPTION
    : '%' IdDash                    -> pushMode(PrequelOption)
    ;


// -------------------------
// Comments

DOC_COMMENT
    : DocComment
    ;
HEADER
    : HeaderComment
    ;
BLOCK_COMMENT
    : BlockComment                  -> channel(HIDDEN)
    ;
LINE_COMMENT
    : LineComment                   -> channel(HIDDEN)
    ;


// -------------------------
// Whitespace

WS
    : Ws+                           -> skip
    ;


// -------------------------
// Illegal Characters
//
// This is an illegal character trap which is always the last rule in the
// lexer specification. It matches a single character of any value and being
// the last rule in the file will match when no other rule knows what to do
// about the character. It is reported as an error but is not passed on to the
// parser. This means that the parser to deal with the gramamr file anyway
// but we will not try to analyse or code generate from a file with lexical
// errors.
//
// Comment this rule out to allow the error to be propagated to the parser

ERRCHAR
    : .                             -> channel(HIDDEN)
    ;


// ======================================================
// Main mode
//

mode Main;


// -------------------------
// Comments

MAIN_DOC_COMMENT
    : DocComment                    -> type(DOC_COMMENT)
    ;
MAIN_HEADER
    : HeaderComment                 -> type(HEADER)
    ;
MAIN_BLOCK_COMMENT
    : BlockComment                  -> type(BLOCK_COMMENT), channel(HIDDEN)
    ;
MAIN_LINE_COMMENT
    : LineComment                   -> type(LINE_COMMENT), channel(HIDDEN)
    ;


// -------------------------
// Integer
//

INT
    : DecimalNumeral
    ;


// -------------------------
// Literal string

STRING_LITERAL
    : SQuoteLiteral
    | DQuoteLiteral
    ;
UNTERMINATED_STRING_LITERAL
    : USQuoteLiteral
    | UDQuoteLiteral
    ;


// -------------------------
// Actions and annotations

BEGIN_ACTION
    : '{'                           -> pushMode(Action)
    ;
BEGIN_PREDICATE
    : '%?{'                         -> pushMode(Action)
    ;
BEGIN_TAG
    : '<'                           -> pushMode(Tag)
    ;


// -------------------------
// Keywords

EMPTY
    : '%empty'
    ;
PREC
    : '%prec'
    ;
DPREC
    : '%dprec'
    ;
MERGE
    : '%merge'
    ;
EXPECT
    : '%expect'
    ;
EXPECT_RR
    : '%expect-rr'
    ;

// -------------------------
// Punctuation

COLON
    : ':'
    ;
SEMI
    : ';'
    ;
LBRACK
    : '['
    ;
RBRACK
    : ']'
    ;
OR
    : '|'
    ;
RETURN
    : '->'                          -> pushMode(ReturnType)
    ;


// -------------------------
// Identifiers - allows unicode rule/token names

ID
    : Id
    ;


EPILOGUE
    : '%%' .*?                      -> skip
    ;


// -------------------------
// Whitespace

MAIN_WS
    : Ws+                           -> skip
    ;


// -------------------------
// Illegal Characters
//
// This is an illegal character trap which is always the last rule in the
// lexer specification. It matches a single character of any value and being
// the last rule in the file will match when no other rule knows what to do
// about the character. It is reported as an error but is not passed on to the
// parser. This means that the parser to deal with the gramamr file anyway
// but we will not try to analyse or code generate from a file with lexical
// errors.
//
// Comment this rule out to allow the error to be propagated to the parser

MAIN_ERRCHAR
    : .                             -> type(ERRCHAR), channel(HIDDEN)
    ;


// ======================================================
// Lexer modes

// -------------------------
// Prequel option
//
// Consumes content after %option. Content ends at the nearest newline,
// unless it contains action code or escapes.

mode PrequelOption;

PREQUEL_OPTION_NESTED_ACTION
    : '{'                           -> skip, pushMode(Action)
    ;
PREQUEL_OPTION_ESCAPE
    : '\\' .                        -> skip
    ;
PREQUEL_OPTION_STRING_LITERAL
    : DQuoteLiteral                 -> skip
    ;
PREQUEL_OPTION_CHAR_LITERAL
    : { self.isLikeC() }?
      CharLiteral                   -> skip
    ;
PREQUEL_OPTION_LIFETIME_LITERAL
    : { self.isLikeC() }?
      LifetimeLiteral               -> skip
    ;
PREQUEL_OPTION_S_STRING_LITERAL
    : { self.isLikePy() }?
      SQuoteLiteral                 -> skip
    ;
PREQUEL_OPTION_BLOCK_COMMENT
    : BlockComment                  -> skip
    ;
PREQUEL_OPTION_LINE_COMMENT
    : LineComment                   -> skip
    ;
END_PREQUEL_OPTION
    : Vws                           -> popMode
    ;
UNTERMINATED_PREQUEL_OPTION
    : EOF                           -> skip
    ;
PREQUEL_OPTION_CONTENT
    : .                             -> skip
    ;


// -------------------------
// Actions
//
// Many language targets use {} as block delimiters and so we
// must recursively match {} delimited blocks to balance the
// braces. Additionally, we must make some assumptions about
// literal string representation in the target language. We assume
// that they are delimited by ' or " and so consume these
// in their own alts so as not to inadvertantly match {}.

mode Action;

NESTED_ACTION
    : '{'                           -> type(BEGIN_ACTION), pushMode(Action)
    ;
ACTION_ESCAPE
    : '\\' .                        -> skip
    ;
ACTION_STRING_LITERAL
    : DQuoteLiteral                 -> skip
    ;
ACTION_CHAR_LITERAL
    : { self.isLikeC() }?
      CharLiteral                   -> skip
    ;
ACTION_LIFETIME_LITERAL
    : { self.isLikeC() }?
      LifetimeLiteral               -> skip
    ;
ACTION_S_STRING_LITERAL
    : { self.isLikePy() }?
      SQuoteLiteral                 -> skip
    ;
ACTION_BLOCK_COMMENT
    : BlockComment                  -> skip
    ;
ACTION_LINE_COMMENT
    : LineComment                   -> skip
    ;
END_ACTION
    : '}'                           -> popMode
    ;
UNTERMINATED_ACTION
    : EOF                           -> skip
    ;
ACTION_CONTENT
    : .                             -> skip
    ;



// -------------------------
// Tag
//
// Parses type tag.

mode Tag;

TAG_NESTED_ACTION
    : '{'                           -> type(BEGIN_ACTION), pushMode(Action)
    ;
TAG_ESCAPE
    : '\\' .                        -> skip
    ;
TAG_STRING_LITERAL
    : DQuoteLiteral                 -> skip
    ;
TAG_CHAR_LITERAL
    : { self.isLikeC() }?
      CharLiteral                   -> skip
    ;
TAG_LIFETIME_LITERAL
    : { self.isLikeC() }?
      LifetimeLiteral               -> skip
    ;
TAG_S_STRING_LITERAL
    : { self.isLikePy() }?
      SQuoteLiteral                 -> skip
    ;
TAG_BLOCK_COMMENT
    : BlockComment                  -> skip
    ;
TAG_LINE_COMMENT
    : LineComment                   -> skip
    ;
END_TAG
    : '>'                           -> popMode
    ;
UNTERMINATED_TAG
    : EOF                           -> skip
    ;
TAG_CONTENT
    : .                             -> skip
    ;


// -------------------------
// Return type
//
// Parses return type after -> in some of bison dialects.

mode ReturnType;

RETURN_TYPE_NESTED_ACTION
    : '{'                           -> type(BEGIN_ACTION), pushMode(Action)
    ;
RETURN_TYPE_ESCAPE
    : '\\' .                        -> skip
    ;
RETURN_TYPE_STRING_LITERAL
    : DQuoteLiteral                 -> skip
    ;
RETURN_TYPE_CHAR_LITERAL
    : { self.isLikeC() }?
      CharLiteral                   -> skip
    ;
RETURN_TYPE_LIFETIME_LITERAL
    : { self.isLikeC() }?
      LifetimeLiteral               -> skip
    ;
RETURN_TYPE_S_STRING_LITERAL
    : { self.isLikePy() }?
      SQuoteLiteral                 -> skip
    ;
RETURN_TYPE_BLOCK_COMMENT
    : BlockComment                  -> skip
    ;
RETURN_TYPE_LINE_COMMENT
    : LineComment                   -> skip
    ;
END_RETURN_TYPE
    : ':'                           -> type(COLON), popMode
    ;
UNTERMINATED_RETURN_TYPE
    : EOF                           -> skip
    ;
RETURN_TYPE_CONTENT
    : .                             -> skip
    ;
