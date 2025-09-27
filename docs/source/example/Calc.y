/** Infix notation calculator. */

/**
 *  A single integer number.
 */
//@ doc:content [1-9][0-9]* | '0'
%token NUMBER

%%

/** Grammar input. */
input
    : input line
    | %empty
    ;

//@ doc:inline
line
    : expression '\n'
    | '\n'
    ;

/** A single expression. */
expression
    : expression '+' exp1
    | expression '-' exp1
    | exp1
    ;

//@ doc:inline
exp1
    : exp1 '*' exp2
    | exp1 '/' exp2
    | exp2
    ;

//@ doc:inline
exp2
    : '-' exp3
    | exp3
    ;

//@ doc:inline
exp3
    : exp4 /** right-assoc */ '^' exp3
    | exp4
    ;

//@ doc:inline
exp4
    : NUMBER
    | '(' expression ')'
    ;

%%
