/*
 * [The "BSD license"]
 *  Copyright (c) 2012-2014 Terence Parr
 *  Copyright (c) 2012-2014 Sam Harwell
 *  Copyright (c) 2015 Gerald Rosenberg
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *  3. The name of the author may not be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 *  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 *  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 *  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 *  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

lexer grammar ANTLRv4Lexer;

options {
    superClass = ANTLRv4LexerBase ;
}

import LexBasic;

tokens {
    TOKEN_REF,
    RULE_REF,
    LEXER_CHAR_SET,
    LBRACE
}


// ======================================================
// Lexer specification
//

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
// Integer
//

INT
    : DecimalNumeral
    ;


// -------------------------
// Literal string
//
// ANTLR makes no distinction between a single character literal and a
// multi-character string. All literals are single quote delimited and
// may contain unicode escape sequences of the form \uxxxx, where x
// is a valid hexadecimal number (per Unicode standard).

STRING_LITERAL
    : SQuoteLiteral
    ;

UNTERMINATED_STRING_LITERAL
    : USQuoteLiteral
    ;


// -------------------------
// Arguments
//
// Certain argument lists, such as those specifying call parameters
// to a rule invocation, or input parameters to a rule specification
// are contained within square brackets.

BEGIN_ARGUMENT
    : '['                           { self.handleBeginArgument() }
    ;


// -------------------------
// Actions

BEGIN_ACTION
    : '{'                           -> pushMode(Action)
    ;


// -------------------------
// Keywords
//
// Keywords may not be used as labels for rules or in any other context where
// they would be ambiguous with the keyword vs some other identifier.  OPTIONS,
// TOKENS, & CHANNELS blocks are handled idiomatically in dedicated lexical modes.

OPTIONS
    : 'options' [ \t\f\n\r]* '{'    -> pushMode(Options)
    ;
TOKENS
    : 'tokens' [ \t\f\n\r]* '{'     -> pushMode(Tokens)
    ;
CHANNELS
    : 'channels' [ \t\f\n\r]* '{'   -> pushMode(Channels)
    ;
IMPORT
    : 'import'
    ;
FRAGMENT
    : 'fragment'
    ;
LEXER
    : 'lexer'
    ;
PARSER
    : 'parser'
    ;
GRAMMAR
    : 'grammar'
    ;
PROTECTED
    : 'protected'
    ;
PUBLIC
    : 'public'
    ;
PRIVATE
    : 'private'
    ;
RETURNS
    : 'returns'
    ;
LOCALS
    : 'locals'
    ;
THROWS
    : 'throws'
    ;
CATCH
    : 'catch'
    ;
FINALLY
    : 'finally'
    ;
MODE
    : 'mode'
    ;


// -------------------------
// Punctuation

COLON
    : ':'
    ;
COLONCOLON
    : '::'
    ;
COMMA
    : ','
    ;
SEMI
    : ';'
    ;
LPAREN
    : '('
    ;
RPAREN
    : ')'
    ;
RBRACE
    : '}'
    ;
RARROW
    : '->'
    ;
LT
    : '<'
    ;
GT
    : '>'
    ;
ASSIGN
    : '='
    ;
QUESTION
    : '?'
    ;
STAR
    : '*'
    ;
PLUS_ASSIGN
    : '+='
    ;
PLUS
    : '+'
    ;
OR
    : '|'
    ;
DOLLAR
    : '$'
    ;
RANGE
    : '..'
    ;
DOT
    : '.'
    ;
AT
    : '@'
    ;
POUND
    : '#'
    ;
NOT
    : '~'
    ;


// -------------------------
// Identifiers - allows unicode rule/token names

ID
    : Id
    ;


// -------------------------
// Whitespace

WS
    : Ws+                           -> channel(HIDDEN)
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
// Lexer modes

// -------------------------
// Arguments

mode Argument;

NESTED_ARGUMENT
    : '['                           -> type(BEGIN_ARGUMENT), pushMode(Argument)
    ;
ARGUMENT_ESCAPE
    : EscAny                        -> skip
    ;
ARGUMENT_STRING_LITERAL
    : DQuoteLiteral                 -> skip
    ;
ARGUMENT_CHAR_LITERAL
    : SQuoteLiteral                 -> skip
    ;
END_ARGUMENT
    : ']'                           -> popMode
    ;
UNTERMINATED_ARGUMENT
    : EOF                           -> popMode
    ;
ARGUMENT_CONTENT
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
    : EscAny                        -> skip
    ;
ACTION_STRING_LITERAL
    : DQuoteLiteral                 -> skip
    ;
ACTION_CHAR_LITERAL
    : SQuoteLiteral                 -> skip
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
    : EOF                           -> popMode
    ;
ACTION_CONTENT
    : .                             -> skip
    ;


// -------------------------
// Options

mode Options;

OPT_BLOCK_COMMENT
    : BlockComment                  -> skip
    ;
OPT_LINE_COMMENT
    : LineComment                   -> skip
    ;
OPT_LBRACE
    : '{'                           -> type(LBRACE)
    ;
OPT_RBRACE
    : '}'                           -> type(RBRACE), popMode
    ;
OPT_ID
    : Id                            -> type(ID)
    ;
OPT_DOT
    : '.'                           -> type(DOT)
    ;
OPT_ASSIGN
    : '='                           -> type(ASSIGN)
    ;
OPT_STRING_LITERAL
    : SQuoteLiteral                 -> type(STRING_LITERAL)
    ;
OPT_INT
    : DecimalNumeral                -> type(INT)
    ;
OPT_STAR
    : '*'                           -> type(STAR)
    ;
OPT_SEMI
    : ';'                           -> type(SEMI)
    ;
OPT_WS
    : Ws+                           -> skip
    ;


// -------------------------
// Tokens

mode Tokens;

TOK_DOC_COMMENT
    : DocComment                    -> type(DOC_COMMENT)
    ;
TOK_HEADER
    : HeaderComment                 -> type(HEADER)
    ;
TOK_BLOCK_COMMENT
    : BlockComment                  -> skip
    ;
TOK_LINE_COMMENT
    : LineComment                   -> skip
    ;
TOK_LBRACE
    : '{'                           -> type(LBRACE)
    ;
TOK_RBRACE
    : '}'                           -> type(RBRACE), popMode
    ;
TOK_ID
    : Id                            -> type(ID)
    ;
TOK_DOT
    : '.'                           -> type(DOT)
    ;
TOK_COMMA
    : ','                           -> type(COMMA)
    ;
TOK_WS
    : Ws+                           -> type(WS), channel(HIDDEN)
    ;


// -------------------------
// Channels

mode Channels;

CHN_BLOCK_COMMENT
    : BlockComment                  -> skip
    ;
CHN_LINE_COMMENT
    : LineComment                   -> skip
    ;
CHN_LBRACE
    : '{'                           -> type(LBRACE)
    ;
CHN_RBRACE
    : '}'                           -> type(RBRACE), popMode
    ;
CHN_ID
    : Id                            -> type(ID)
    ;
CHN_DOT
    : '.'                           -> type(DOT)
    ;
CHN_COMMA
    : ','                           -> type(COMMA)
    ;
CHN_WS
    : Ws+                           -> type(WS), channel(HIDDEN)
    ;


// -------------------------
// Lexer CharSet

mode LexerCharSet;

LEXER_CHAR_SET_BODY
    : (~[\]\\]|EscAny)+             -> more
    ;
LEXER_CHAR_SET
    : ']'                           -> popMode
    ;
UNTERMINATED_CHAR_SET
    : EOF                           -> popMode
    ;
