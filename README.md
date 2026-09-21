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