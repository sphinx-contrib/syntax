Diagrams
========

.. container:: regression

   .. syntax:parser-diagram:: x y z (A B y z)*
      :force-text:

   .. syntax:parser-diagram:: (x y A B)* x y z
      :force-text:

   .. syntax:parser-diagram::
      :force-text:

        x y A
      | x y B
      | y x C

   .. syntax:parser-diagram::
      :force-text:

        A x y
      | B x y
      | C y x

   .. syntax:parser-diagram::
      :force-text:

        root X
      |

   .. syntax:parser-diagram::
      :force-text:

        root X
      | X

   .. syntax:parser-diagram::
      :force-text:

        root ',' X
      | root ',' Y
      | X
      | Y

   .. syntax:parser-diagram::
      :force-text:

      exp;

      //@ doc:inline
      exp
         : exp '+' exp1
         | exp '-' exp1
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
         : exp4 '^' exp3
         | exp4
         ;
      //@ doc:inline
      exp4
         : NUMBER
         | '(' exp ')'

   .. syntax:parser-diagram::
      :force-text:

         exp;

         //@ doc:inline
         //@ doc:keep-diagram-recursive
         exp
            : NUMBER
            | exp '+' exp
            | exp '-' exp
            | exp '*' exp
            | exp '/' exp
            | '-' exp
            | exp '^' exp
            | '(' exp ')'
