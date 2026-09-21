HOW TO CALL SOURCE

base command: python source.py

The program will run with an input loop, allowing the user to enter relations and queries into the terminal
Relations will accept multi line input and can be pasted in or entered in the follow format:

RELATION_NAME (col1, col2, col3) = {
    A1, A2, A3
    B1, B2, B3
    C1, C2, C3
    D1, D2, D3
}

tree command: python source.py --tree "**QUERY**"

The program will print the parse tree for the given query.

HOW TO RUN TESTS

Run following command from root directory containing source.py and tests/*.py

python -m tests.test_*insert*

example:

python -m tests.test_tokenizer


Known limitations:
Cannot store strings of numbers in relations. If a relation has a value resembling a number (5, -2, 3.4), it will automatically be considered a number. You cannot theoretically have "3" as a relation value, however it is possible as a operand
Due to how times and join modify column names, it can be difficult for a user to correctly access column names after multiple joins. For example, they could end up having do do something like select[R2.R1.Age = 30](R2) after multiple, not necesarily a limitation but definitely annoying





join rename necessity:
    Essentially, join uses the format of table_name.attribute to differentiate between attributes for either table in the joined table. If a self join is called without using rename, it results in a table like
    R.a, R.b, R.c, R.a, R.b
    Where the program has no clue which attribute is from which table, making comparison impossible


projection clarification:
    Cannot have duplicate col names in projection condition, will cause error