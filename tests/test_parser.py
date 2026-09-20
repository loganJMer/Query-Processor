from source import tokenize, parse_condition, evaluate_condition


# =========================
# Condition Parser Tests
# =========================

parserTests = [

    # 1
    [
        "Age > 30",
        ("COMPARISON", ("GT", ("ATTRIBUTE", "Age"), ("INT", 30)))
    ],

    # 2
    [
        "Age > 30 and Age < 40",
        (
            "AND",
            ("COMPARISON", ("GT", ("ATTRIBUTE", "Age"), ("INT", 30))),
            ("COMPARISON", ("LT", ("ATTRIBUTE", "Age"), ("INT", 40)))
        )
    ],

    # 3
    [
        "Age > 30 or Age < 20",
        (
            "OR",
            ("COMPARISON", ("GT", ("ATTRIBUTE", "Age"), ("INT", 30))),
            ("COMPARISON", ("LT", ("ATTRIBUTE", "Age"), ("INT", 20)))
        )
    ],

    # 4 - AND has higher precedence than OR
    [
        "Age > 30 or Age < 20 and Name = 'John'",
        (
            "OR",
            ("COMPARISON", ("GT", ("ATTRIBUTE", "Age"), ("INT", 30))),
            (
                "AND",
                ("COMPARISON", ("LT", ("ATTRIBUTE", "Age"), ("INT", 20))),
                ("COMPARISON", ("EQ", ("ATTRIBUTE", "Name"), ("STR", "John")))
            )
        )
    ],

    # 5 - NOT is right-associative
    [
        "not not Age > 30",
        (
            "NOT",
            ("NOT",
                ("COMPARISON", ("GT", ("ATTRIBUTE", "Age"), ("INT", 30)))
            )
        )
    ],

    # 6 - Parentheses
    [
        "(Age > 30 or Age < 20) and Name = 'John'",
        (
            "AND",
            (
                "OR",
                ("COMPARISON", ("GT", ("ATTRIBUTE", "Age"), ("INT", 30))),
                ("COMPARISON", ("LT", ("ATTRIBUTE", "Age"), ("INT", 20)))
            ),
            ("COMPARISON", ("EQ", ("ATTRIBUTE", "Name"), ("STR", "John")))
        )
    ]
]


# =========================
# Condition Evaluation Tests
# =========================

evalTests = [

    # 1
    [
        "Age > 30",
        ("Name", "Age"),
        ("John", "32"),
        True
    ],

    # 2
    [
        "Age < 30",
        ("Name", "Age"),
        ("John", "32"),
        False
    ],

    # 3
    [
        "Age > 30 and Age < 40",
        ("Name", "Age"),
        ("John", "32"),
        True
    ],

    # 4
    [
        "Age > 30 or Age < 20",
        ("Name", "Age"),
        ("John", "32"),
        True
    ],

    # 5
    [
        "not Age > 30",
        ("Name", "Age"),
        ("John", "32"),
        False
    ],

    # 6
    [
        "not not Age > 30",
        ("Name", "Age"),
        ("John", "32"),
        True
    ],

    # 7
    [
        "Name = 'John'",
        ("Name", "Age"),
        ("John", "32"),
        True
    ],

    # 8
    [
        "Name != 'John'",
        ("Name", "Age"),
        ("John", "32"),
        False
    ],

    # 9
    [
        "Age = OtherAge",
        ("Name", "Age", "OtherAge"),
        ("John", "32", "32"),
        True
    ],

    # 10 - Parentheses change evaluation
    [
        "(Age > 30 or Age < 20) and Name = 'John'",
        ("Name", "Age"),
        ("John", "32"),
        True
    ]
]


def main():
    failCount = 0

    print("Condition parser tests\n")
    failCount += runParserTests(parserTests)

    print("Condition evaluation tests\n")
    failCount += runEvalTests(evalTests)

    print(f"Fail count: {failCount}")


def runParserTests(tests: list[list]):
    failCount = 0

    for test in tests:
        condition = test[0]
        expectedOutput = test[1]

        tokens = tokenize(condition)
        parsed = parse_condition(tokens)

        if parsed is None:
            failCount += 1
            print(f"Condition: {condition}\nParser returned None\nFailure!\n")
            continue

        output = parsed[0]

        if output != expectedOutput:
            failCount += 1
            print(
                f"Condition: {condition}\n"
                f"Output:          {output}\n"
                f"Expected Output: {expectedOutput}\n"
                f"Failure!\n"
            )
        else:
            print(f"Condition: {condition}\nOutput: {output}\nSuccess!\n")

    return failCount


def runEvalTests(tests: list[list]):
    failCount = 0

    for test in tests:
        condition = test[0]
        col_names = test[1]
        row = test[2]
        expectedOutput = test[3]

        tokens = tokenize(condition)
        parsed = parse_condition(tokens)

        if parsed is None:
            failCount += 1
            print(f"Condition: {condition}\nParser returned None\nFailure!\n")
            continue

        output = evaluate_condition(parsed[0], col_names, row)

        if output != expectedOutput:
            failCount += 1
            print(
                f"Condition: {condition}\n"
                f"Output:          {output}\n"
                f"Expected Output: {expectedOutput}\n"
                f"Failure!\n"
            )
        else:
            print(f"Condition: {condition}\nOutput: {output}\nSuccess!\n")

    return failCount


if __name__ == "__main__":
    main()