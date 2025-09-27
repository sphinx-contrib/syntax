/**
 * Docs for grammar.
 */
lexer grammar Lexer;

tokens {
    /// Prologue 1.

    /** Docs for token A. */
    TOKEN_A,

    /** Docs for token B. */
    //@ doc:name token-b
    //@ doc:content 'token_b'
    TOKEN_B
}

/// Prologue 2.

/** Docs for token C. */
TOKEN_C: 'token_c';

/** Docs for token D. */
TOKEN_D: Fragment;

fragment Fragment: 'token_d';
