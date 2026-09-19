Session 1: 12pm to 3pm, September 18
Began working on the project. Created all the necessary files and started by simply implementing most of the relational algebra operator functionalities including projection, times, union, etc. Did not implement selection and join as those need parser for condition. Will just implement join as times + select though. Also implemented method to convert a relation in provided string format into list of tuples. Used AI for occasional small troubleshooting and for the relation print method for debugging. Also began working on tokenizer.

Session 2: 5pm - 7:30pm
Finished tokenizer, adding functionality for all possibilities as for all that I'm currently aware of. Swapped relations to store table name at index 0, which allows creation of a new table name after operation. This is necessary when having many nested functions like multiple cartesian products to have accurate attribute names. Also implemented required tests for the tokenizer, will probably add some custom ones for edges cases later.
**AI issue**: Used it to automatically translate the required tests into my list format of [query, expected]. Two issues arose. Firstly, it tried using different token names like LEFTBRACKET, RIGHTCURLY instead of the ones I had and provided it. Secondly, it was unable to recognize what should be a tokenizer error vs parser error. For example, it set the expected output for cases 16 and 17 to SYNTAX ERROR, when they should just be tokenized and the tokenizer will parse them correctly. *note: I know tests beyond 7.1 are not to test tokenizer but I figured it was good to add and it heplped me remember some cases I'd forgotten like commas*
Planning to begin work on grammar


Session 3: 2pm - 
Worked on


**AI issue**: When trying to use AI to help confirm if there were issues with my grammar declarations for section 5.1, it continually tried to make me changed my definitions so that the base definition of an expr was exclusively a binary operator, essentially making it so every query would have to have at least one binary operator