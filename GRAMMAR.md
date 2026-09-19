5.1

relation ::= identifier , "(" , attribute-list , ")" , "=" , "{" , {tuple} , "}" ;

attribute-list ::= identifier, { "," , identifier } ;

tuple ::= value, { "," , value } ;

value ::= number | string ;

number ::= ["-"] , digit , {digit} , ["." , digit, {digit}] ;

//Non apostrophe char is any letter, number or symbol that is not '. I could write this out like letter or digit but no
string ::= "'" , { non-apostrophe-char | "''" } , "'" ;

identifier ::= letter , { letter | digit | "_" } ;

letter ::= "A" | "B" | ... | "Z" | "a" | ... | "z" ;

digit ::= "0" | "1" | ... | "9" ;

expr ::= join-expr , { low-operator , join-expr } ;

join-expr ::= primary-expr , { "join" , "[" , condition , "]" , primary-expr } ;

primary-expr ::=
    identifier
  | unary-expr
  | "(" , expr , ")" ;

low-operator ::=
    "union"
  | "intersect"
  | "minus"
  | "times" ;

unary-expr ::=
select-expr
| project-expr
| rename-expr ;

select-expr ::=
    "select" , "[" , condition , "]" , "(" , expr , ")" ;

project-expr ::=
    "project" , "[" , attribute-list , "]" , "(" , expr , ")" ;

rename-expr ::=
    "rename" , "[" , identifier , "]" , "(" , expr , ")" ;

condition ::= or-condition ;

or-condition ::= and-condition , { "or" , and-condition } ;

and-condition ::= not-condition , { "and" , not-condition} ;

not-condition ::= "not" , not-condition | condition-base ;

condition-base ::= comparison | "(" , condition , ")" ;

comparison ::= operand , comparison-operator, operand ;

comparison-operator ::= "=" | "<" | ">" | ">=" | "<=" | "!=" ;

operand ::= value | attribute ;

attribute ::= identifier | identifier , "." , identifier ;


5.2

In all cases ( ... ) grouping take highest precedence

Binary Operator Precedence

Operator/Grouping               Precedence              Associativity
join                            #1 (highest)            Left to Right
union, intersect, minus, times  #2                      Left to Right

This means that A union B minus C equals ( A union B ) minus C
And that A minus B minus C associates left to right resulting in ( A minus B ) minus C
Join has predence though so A minus B join C times D is ( A minus ( B join C ) ) times D

Conditional Operator    Precedence              Associativity
not                     #1                      Right to Left  
and                     #2                      Left to Right
or                      #3                      Left to Right

This means that not binds tighter than and, which binds tighter than or

5.3

Trees

Tree 1: A union ( B minus C )
   union
  /     \
 A     minus
      /     \
     B       C

Tree 2: (A union B) minus C
       minus
      /     \
   union     C
  /     \
 A       B



Different results:

If A (X, Y) = {
    (1, 1),
    (1, 0)
}

B (M, N) = {
(1, 1),
(0, 1)
}

C (Q, R) = {
(1, 1),
(0, 0)
}

Then we see that Tree 1 results in the table 
result1 (X, Y) = {
(1, 1),
(1, 0),
(0, 1)
}

And Tree 2 results in the table 
result2 (X, Y) = {
(1, 0),
(0, 1)
}

My grammar which solves this is 
expr ::= join-expr , { low-operator , join-expr } ;

low-operator ::=
    "union"
  | "intersect"
  | "minus"
  | "times" ;

  This forces left to right associativity by evaluating or in other words, Tree 2 or (A union B) minus C

5.4

This is recursive descent parser. I avoided left-recursion issues with the following expression definition
For example
expr ::= join-expr , { low-operator , join-expr } ; # Mine
expr ::= expr , operator, expr ; # Bad

Instead of having some format like the bad one above, this formatting forces the parser to consume the initial join-expr, then process an unspecified amount more of operator, join-expr. The definition of join-expr follows the same logic.

5.5

https://craftinginterpreters.com/parsing-expressions.html
https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form
https://tomassetti.me/ebnf/

For the most part, the AI was never explicitly wrong in terms of actually EBNF formatting, it just seemed to sometimes get stuck on what I actually wanted to accomplish as my end goal for grammar, as I think it tried to pull from other different existing grammar conventions instead of following mine