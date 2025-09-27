/**
 * JSON (JavaScript Object Notation) is a lightweight data-interchange format.
 */
grammar Json;


/// **Top level**

/**
 * On top level, JSON consists of a single value. That value can be either
 * a complex structure (such as an `object` or an `array`) or a primitive
 * type (a :syntax:r:`STRING` in double quotes, a :syntax:r:`NUMBER`,
 * or ``true`` or ``false`` or ``null``).
 */
value
    : object
    | array
    | NUMBER
    | STRING
    | TRUE
    | FALSE
    | NULL
    ;


/// **Complex objects**

/**
 * Object is a collection of name/value pairs. In various languages,
 * this is realized as an object, record, struct, dictionary,
 * hash table, keyed list, or associative array.
 */
object
    : '(' (STRING ':' value (',' STRING ':' value)*)? ')'
    ;

/**
 * Array is an ordered list of values. In most languages, this is realized as
 * vector, list, array or sequence.
 */
array
    : '[' (value (',' value)*)? ']'
    ;


/// **Primitive types**

/**
 * A number is very much like a C or Java number,
 * except that the octal and hexadecimal formats are not used.
 */
NUMBER
    : NEG? ('0' | [1-9] [0-9]*) ('.' [0-9]+)? EXPONENT?
    ;

//@ doc:inline
//@ doc:importance 0
fragment NEG
    : '-'
    ;

//@ doc:inline
//@ doc:importance 0
fragment EXPONENT
    : ('e' | 'E') ('+' | '-')? [0-9]+
    ;

/**
 * A string is a sequence of zero or more Unicode characters,
 * wrapped in double quotes, using backslash escapes.
 * A character is represented as a single character string.
 * A string is very much like a C or Java string.
 */
STRING
   : '"' (SAFECODEPOINT | ESC)* '"'
   ;

//@ doc:inline
fragment ESC
   : '\\' ESC_CONTENTS
   ;

//@ doc:inline
fragment ESC_CONTENTS
    : '"' /** quotation mark */
    | '\\' /** reverse solidus */
    | '/' /** solidus */
    | 'b' /** backspace */
    | 'f' /** formfeed */
    | 'n' /** newline */
    | 'r' /** carriage return */
    | 't' /** horizontal tab */
    | 'u' UNICODE
    ;

//@ doc:name 4 hexadecimal digits
fragment UNICODE
   : 'u' HEX HEX HEX HEX
   ;

fragment HEX
   : [0-9a-fA-F]
   ;

//@ doc:name Any unicode character except " and \
fragment SAFECODEPOINT
   : ~ ["\\\u0000-\u001F]
   ;

TRUE
    : 'true'
    ;

FALSE
    : 'false'
    ;

NULL
    : 'null'
    ;
