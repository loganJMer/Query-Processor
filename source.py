import sys

relations = {}

def create_relation(input: str):
    relation_name = input[:input.find(" ")]
    col_names = input[input.find("(") + 1:input.find(")")].split(", ")
    relation = [relation_name, tuple(col_names)]
    info = input[input.find("{") + 1:input.find("}") - 1].split("\n")
    for row in info:
        row = row.strip()
        if row:
            split_row = row.split(", ")
            relation.append(tuple(split_row))
    relations[relation_name] = relation

def evaluate_condition(condition, col_names: tuple[str], row: tuple[str]):
    if not (condition):
        print("Syntax error: Select requires non empty condition.")
        return None
    match condition[0]:
        case "OR":
            return evaluate_condition(condition[1], col_names, row) or evaluate_condition(condition[2], col_names, row)
        case "AND":
            return evaluate_condition(condition[1], col_names, row) and evaluate_condition(condition[2], col_names, row)
        case "NOT":
            return not evaluate_condition(condition[1], col_names, row)
        case "COMPARISON":
            comparison = condition[1]
            operator = comparison[0]
            val1 = comparison[1]
            val2 = comparison[2]
            vals = []
            for val in [val1, val2]:
                if val[0] == "ATTRIBUTE":
                    if val[1] not in col_names:
                        print(f"Syntax error: Attribute {val[1]} not present in relation attributes {col_names}")
                        return None
                    index = col_names.index(val[1])
                    row_value = row[index]
                    if is_number(row_value):
                        row_value = float(row_value)
                    vals.append(row_value)
                elif val[0] == "INT":
                    vals.append(float(val[1]))
                else:
                    vals.append(val[1])
            compatible = check_compatability(vals, operator)
            if not compatible:
                return None
            match operator:
                case "EQ":
                    return vals[0] == vals[1]
                case "NEQ":
                    return vals[0] != vals[1]
                case "GT":
                    return vals[0] > vals[1]
                case "GTE":
                    return vals[0] >= vals[1]
                case "LT":
                    return vals[0] < vals[1]
                case "LTE":
                    return vals[0] <= vals[1]
            print(f"Unknown operator type {operator}")
            return None

def check_compatability(vals, operator):
    nums = [False, False]
    if isinstance(vals[0], float):
        nums[0] = True
    if isinstance(vals[1], float):
        nums[1] = True
    #Don't need to be same type for these. MAYBE NEED TO CHANGE
    if operator in ["EQ", "NEQ"] or nums[0] == nums[1]:
        return True
    print(f"Syntax error: Cannot compare string to int with operator {operator}. Val1: {vals[0]}  Val2: {vals[1]}")
    return False

def is_number(n):
  try:
    float(n)
    return True
  except ValueError:
    return False

def select(R: list[tuple[str]], condition: list[str]):
    selection = [R[0], R[1]]
    parsed_condition = parse_condition(condition)
    for row in R[2:]:
        if evaluate_condition(parsed_condition, R[1], row):
            selection.append(row)
    return selection

def project(R: list[tuple[str]], cols: list[str]):
    indices = []
    projection = [R[0]]
    for col in cols:
        index = R[1].index(col)
        if index in indices:
            print(f"Syntax error: No duplicates attributes in project. Error in project{cols}({R[0]})")
        indices.append(index)
        if indices[-1] == -1:
            print(f"Name error: Column {col} does not exist in relation {R}")
            return None
    for row in R[1:]:
        new_row = tuple([row[i] for i in indices])
        if new_row not in projection:
            projection.append(new_row)

    return projection
    

#Cartesian product
def times(R1: list[tuple[str]], R2: list[tuple[str]]):
    product = [R1[0]]
    titles = []
    for col in R1[1]:
        titles.append(f"{R1[0]}.{col}")
    for col in R2[1]:
        titles.append(f"{R2[0]}.{col}")
    product.append(tuple(titles))
    rows1, rows2 = R1[2:], R2[2:]
    for row1 in rows1:
        for row2 in rows2:
            product.append(row1+row2)
    return product


#Theta inner join
def join(R1: list[tuple[str]], R2: list[tuple[str]], condition: str):
    return select(times(R1, R2), condition)

def union(R1: list[tuple[str]], R2: list[tuple[str]]):
    if len(R1[1]) != len(R2[1]):
        print("Schema Error: Relations must have same number of columns for union\n")
        return None
    R2_copy = R2.copy()
    union = [R1[0]]
    union.append(R1[1])
    for row1 in R1[2:]:
        union.append(row1)
        for row2 in R2_copy[2:]:
            if row1 == row2:
                R2_copy.remove(row2)
    for row in R2_copy[2:]:
        union.append(row)
    return union

def intersect(R1: list[tuple[str]], R2: list[tuple[str]]):
    if len(R1[1]) != len(R2[1]):
        print("Schema Error: Relations must have same number of columns for intersect\n")
        return None
    intersect = [R1[0]]
    intersect.append(R1[1])
    for row1 in R1[2:]:
        for row2 in R2[2:]:
            if row1 == row2:
                intersect.append(row1)
    return intersect

def minus(R1: list[tuple[str]], R2: list[tuple[str]]):
    if len(R1[1]) != len(R2[1]):
        print("Schema Error: Relations must have same number of columns for minus\n")
        return None
    minus = [R1[0]]
    minus.append(R1[1])
    for row1 in R1[2:]:
        skip = False
        for row2 in R2[2:]:
            if row1 == row2:
                skip = True
                break
        if skip:
            continue
        minus.append(row1)
    return minus

def rename(R1: str, name: str):
    if not relations.get(R1):
        print(f"Name Error: Relation {R1} does not exist")
        return None
    relations[name] = relations[R1]

def print_table(R: list[tuple[str]]):
    print(R[0] + "\n")
    widths = [
        max(len(str(row[i])) for row in R)
        for i in range(len(R[1]))
    ]

    for row in R[1:]:
        print(" | ".join(
            str(value).ljust(widths[i])
            for i, value in enumerate(row)
        ))

        if row == R[1]:
            print("-+-".join("-" * width for width in widths))
    print("\n")




def tokenize(query: str):
    tokens = []
    position = 0
    fail_message = ""

    while(position < len(query)):
        c = query[position]
        c2 = query[position + 1] if position + 1 < len(query) else None

        #Skip whitespace
        if c == ' ':
            position += 1
            continue

        #Check if comma
        if c == ',':
            tokens.append("COMMA:,")
            position += 1
            continue

        #Check if string
        if c == "'":
            token, position = tokenize_str(query, position + 1)
            if position == -1:
                fail_message = token
                break
            tokens.append(f"STR:{token}")
            continue

        #Check if comparison operator
        if c in ["!", "=", "<", ">"]:
            if c == "!":
                if not c2 or c2 != "=":
                    fail_message = "Name error: Invalid != operator. ! must be followed by ="
                    break
                tokens.append("NEQ:!=")
                position += 2
                continue
            if c == "<":
                if c2 and c2 == "=":
                    tokens.append("LTE:<=")
                    position += 2
                    continue
                else:
                    tokens.append("LT:<")
                    position += 1
                    continue
            if c == ">":
                if c2 and c2 == "=":
                    tokens.append("GTE:>=")
                    position += 2
                    continue
                else:
                    tokens.append("GT:>")
                    position += 1
                    continue
            if c == "=":
                tokens.append("EQ:=")
                position += 1
                continue
    
        #Check if boolean operator
        if c in ["a", "o", "n"]:
            if c == "a":
                if position + 2 < len(query):
                    if query[position:position + 3] == "and":
                        tokens.append("AND:and")
                        position += 3
                        continue
            if c == "o":
                if c2 and c2 == "r":
                    tokens.append("OR:or")
                    position += 2
                    continue
            if c == "n":
                if position + 2 < len(query):
                    if query[position:position + 3] == "not":
                        tokens.append("NOT:not")
                        position += 3
                        continue

        brackets = {"(":"LEFTP:(", ")":"RIGHTP:)", "[":"LEFTS:[", "]":"RIGHTS:]", "{":"LEFTC:{", "}":"RIGHTC:}"}
        #Check if bracket
        if c in ["(", ")", "[", "]", "{", "}"]:
            tokens.append(brackets.get(c))
            position += 1
            continue

        #Check if unary op/join
        if c in ["s", "r", "p", "j"]:
            if c == "s":
                if position + 6 < len(query):
                    if query[position:position + 7] == "select[":
                        tokens.append("SELECT:select")
                        position += 6
                        continue
            if c == "r":
                if position + 6 < len(query):
                    if query[position:position + 7] == "rename[":
                        tokens.append("RENAME:rename")
                        position += 6
                        continue
            if c == "p":
                if position + 7 < len(query):
                    if query[position:position + 8] == "project[":
                        tokens.append("PROJECT:project")
                        position += 7
                        continue
            if c == "j":
                if position + 4 < len(query):
                    if query[position:position + 5] == "join[":
                        tokens.append("JOIN:join")
                        position += 4
                        continue

        #Check if binary op except join
        if c in ["t", "u", "i", "m"]:
            if c == "t":
                if position + 5 < len(query):
                    if query[position - 1:position + 6] == " times ":
                        tokens.append("TIMES:times")
                        position += 5
                        continue
            if c == "u":
                if position + 5 < len(query):
                    if query[position - 1:position + 6] == " union ":
                        tokens.append("UNION:union")
                        position += 5
                        continue
            if c == "i":
                if position + 9 < len(query):
                    if query[position - 1:position + 10] == " intersect ":
                        tokens.append("INTERSECT:intersect")
                        position += 9
                        continue
            if c == "m":
                if position + 5 < len(query):
                    if query[position - 1:position + 6] == " minus ":
                        tokens.append("MINUS:minus")
                        position += 5
                        continue



        if c.isnumeric() or c == "-":
            token, position = tokenize_int(query, position)
            tokens.append(f"INT:{token}")
            continue

        if c.isalpha():
            token, position = tokenize_relation(query, position)
            if token.count(".") > 1:
                fail_message = f"Lexical Error: Cannot have relation reference with more than one '.'. Error in relation: {token}"
                break
            if token.count(".") == 1:
                tokens.append(f"RELATION_COLUMN:{token}")
            else:
                tokens.append(f"RELATION:{token}")
            continue

        fail_message = f"Lexical Error: Unknown formatting at character {c} in position {position}"
        break
    if fail_message:
        return fail_message
    return tokens


def tokenize_str(query: str, position: int):
    string = ""
    orig_pos = position - 1
    finished = False
    while(position < len(query)):
        c = query[position]
        if c != "'":
            string += c
            position += 1
            continue
        if position + 1 != len(query) and query[position + 1] == "'":
            string += c
            position += 2
            continue
        finished = True
        break
    if not finished:
        fail_message = f"Lexical Error: String '{string} was never closed. Starts at position {orig_pos}"
        return fail_message, -1
    return string, position + 1

def tokenize_int(query: str, position: int):
    string = ""
    while(position < len(query)):
        c = query[position]
        if c.isnumeric() or (c == "-" and string == ""):
            string += c
            position += 1
            continue
        break
    return string, position

def tokenize_relation(query: str, position: int):
    relation = ""
    while(position < len(query)):
        c = query[position]
        if c.isalnum() or c in ["_", "."]:
            relation += c
            position += 1
            continue
        break
    return relation, position

def parse_expr(tokens: list[str]):
    leftJoinExpr, num_consumed = parse_join_expr(tokens)
    if not leftJoinExpr:
        return None
    total_num_consumed = num_consumed
    if num_consumed == len(tokens):
        return leftJoinExpr, total_num_consumed
    tokens = tokens[num_consumed:]
    while tokens[0] in ["UNION:union", "INTERSECT:intersect", "MINUS:minus", "TIMES:times"]:
        operator = tokens[0]
        if len(tokens) == 1:
            print(f"Syntax error: binary operator {operator} must be followed by a join-expr, cannot be empty.")
            return None
        rightJoinExpr, num_consumed = parse_join_expr(tokens[1:])
        if not rightJoinExpr:
            return None
        total_num_consumed += num_consumed + 1
        match operator:
            case "UNION:union":
                expr = ("UNION", leftJoinExpr, rightJoinExpr)
            case "INTERSECT:intersect":
                expr = ("INTERSECT", leftJoinExpr, rightJoinExpr)
            case "MINUS:minus":
                expr = ("MINUS", leftJoinExpr, rightJoinExpr)
            case "TIMES:times":
                expr = ("TIMES", leftJoinExpr, rightJoinExpr)
        if num_consumed == len(tokens[1:]):
            return expr, total_num_consumed
        tokens = tokens[num_consumed + 1:]
        leftJoinExpr = expr
    return leftJoinExpr, total_num_consumed


def parse_join_expr(tokens: list[str]):
    leftPrimaryExpr, num_consumed = parse_primary_expr(tokens)
    if not leftPrimaryExpr:
        return None
    total_num_consumed = num_consumed
    if num_consumed == len(tokens):
        return leftPrimaryExpr, total_num_consumed
    tokens = tokens[num_consumed:]
    while tokens[0] == "JOIN:join":
        if "LEFTS:[" not in tokens or tokens[1] != "LEFTS:[":
            print("Syntax error: join operator must be followed by [.")
            return None
        if "RIGHTS:]" not in tokens:
            print("Syntax error: Condition for join statement must be closed with ].")
            return None
        lConIndex = tokens.index("LEFTS:[")
        rConIndex = tokens.index("RIGHTS:]")
        if rConIndex == 2:
            print("Syntax error: join condition cannot be empty")
            return None
        if rConIndex == len(tokens) - 1:
            print("Syntax error: Must have primary expression after join condition")
            return None
        
        condition_tokens = tokens[lConIndex + 1:rConIndex]
        condition, condition_num_consumed = parse_condition(condition_tokens)
        if not condition:
            return None
        if condition_num_consumed != len(condition_tokens):
            print("Syntax error: Join condition consumption did not match expected value.")
            return None
        rightPrimaryExpr, right_num_consumed = parse_primary_expr(tokens[rConIndex + 1:])
        if not rightPrimaryExpr:
            return None
        total_num_consumed += condition_num_consumed + right_num_consumed + 3 # +3 is for join, [ and ]
        expr = ("JOIN", leftPrimaryExpr, rightPrimaryExpr, condition)
        if right_num_consumed == len(tokens[rConIndex + 1:]):
            return expr, total_num_consumed
        tokens = tokens[rConIndex + 1:]
        leftPrimaryExpr = expr
    return leftPrimaryExpr, total_num_consumed

def parse_primary_expr(tokens: list[str]):
    pass


def parse_condition(tokens: list[str]):
    leftAndCondition, num_consumed = parse_and_condition(tokens)
    if not leftAndCondition:
        return None
    total_num_consumed = num_consumed
    if num_consumed == len(tokens):
        return leftAndCondition, total_num_consumed
    tokens = tokens[num_consumed:]
    while tokens[0] == "OR:or":
        if len(tokens) == 1:
            print(f"Syntax error: or operator must be followed by comparison or nested condition")
            return None
        rightAndCondition, num_consumed = parse_and_condition(tokens[1:])
        if not rightAndCondition:
            return None
        total_num_consumed += num_consumed + 1
        condition = ("OR", leftAndCondition, rightAndCondition)
        if num_consumed == len(tokens[1:]):
            return condition, total_num_consumed
        tokens = tokens[num_consumed + 1:]
        leftAndCondition = condition
    return leftAndCondition, total_num_consumed



def parse_and_condition(tokens: list[str]):
    leftNotCondition, num_consumed = parse_not_condition(tokens)
    if not leftNotCondition:
        return None
    total_num_consumed = num_consumed
    if num_consumed == len(tokens):
        return leftNotCondition, total_num_consumed
    tokens = tokens[num_consumed:]
    while tokens[0] == "AND:and":
        if len(tokens) == 1:
            print(f"Syntax error: and operator must be followed by comparison or nested condition")
            return None
        rightNotCondition, num_consumed = parse_not_condition(tokens[1:])
        if not rightNotCondition:
            return None
        total_num_consumed += num_consumed + 1
        condition = ("AND", leftNotCondition, rightNotCondition)
        if num_consumed == len(tokens[1:]):
            return condition, total_num_consumed
        tokens = tokens[num_consumed + 1:]
        leftNotCondition = condition
    return leftNotCondition, total_num_consumed

def parse_not_condition(tokens: list[str]):

    if len(tokens) == 0:
        print("Syntax error: expected not-condition, but received no tokens")
        return None

    if tokens[0] == "NOT:not":

        if len(tokens) == 1:
            print("Syntax error: not operator must be followed by a condition")
            return None

        condition, num_consumed = parse_not_condition(tokens[1:])

        if not condition:
            return None

        return ("NOT", condition), num_consumed + 1

    return parse_condition_base(tokens)

def parse_condition_base(tokens: list[str]):

    if len(tokens) == 0:
        print("Syntax error: expected condition")
        return None

    if tokens[0] == "LEFTP:(":
        condition, num_consumed = parse_condition(tokens[1:])
        if not condition:
            return None
        if num_consumed == len(tokens[1:]) or tokens[num_consumed + 1] != "RIGHTP:)":
            print(f"Syntax error: Never closed ( for nested condition {tokens[1:]}")
            return None
        
        return condition, num_consumed + 2
    return parse_comparison(tokens)

def parse_comparison(tokens: list[str]):
    if len(tokens) < 3:
        print(f"Syntax error: comparison must consist of three elements: {tokens}")
        return None
    leftOp = parse_operand(tokens[0])
    rightOp = parse_operand(tokens[2])
    compOp = parse_comparison_operator(tokens[1])
    if not (leftOp and rightOp and compOp):
        return None
    return ("COMPARISON", (compOp, leftOp, rightOp)), 3

def parse_operand(token: str):
    if not token:
        print(f"Syntax error: operand must consist of one element: {token}")
        return None
    operand = token
    if operand.startswith("RELATION:") or operand.startswith("RELATION_COLUMN:"):
        return ("ATTRIBUTE", operand[operand.index(":")+1:])
    if operand.startswith("INT:"):
        return ("INT", int(operand[operand.index(":")+1:]))
    if operand.startswith("STR:"):
        return ("STR", operand[operand.index(":")+1:])
    print(f"Operand must be of type RELATION, RELATION_COLUMN, INT, or STR: {operand}")
    return None

def parse_comparison_operator(token: str):
    if not token:
        print(f"Syntax error: comparison operator must consist of one element: {token}")
        return None
    compOp = token
    if compOp in ["EQ:=", "NEQ:!=", "GT:>", "GTE:>=", "LT:<", "LTE:<="]:
        return compOp[:compOp.index(":")]
    print(f"Comparison operator must be of type EQ, NE, GT, GTE, LT, LTE: {compOp}")
    return None

def main():


    # rel1 = """Employees (EID, Name, Age, DID) = {
    # E1, John, 32, D1
    # E2, Alice, 28, D2
    # E3, Bob, 29, D3
    # E4, Janice, 30, D2
    # }"""
    # rel2 = """Departments (DID, Name, Budget) = {
    # D1, Finance, 20000
    # D2, Sales, 30000
    # D3, HR, 25000
    # D4, IT, 15000
    # }"""
    # rel3 = """Employees2 (EID, Name, Age, DID) = {
    # E2, Alice, 28, D2
    # E4, Janice, 30, D2
    # E5, John, 32, D1
    # E6, David, 47, D4
    # }"""
    # create_relation(rel1)
    # create_relation(rel2)
    # create_relation(rel3)
    # print_table(relations["Employees"])
    # print_table(relations["Departments"])
    # print_table(relations["Employees2"])
    # print_table(project(relations["Departments"], ["DID"]))
    # print_table(project(relations["Employees"], ["EID", "Age"]))
    # print_table(times(relations["Employees"], relations["Departments"]))
    # print_table(union(relations["Employees"], relations["Employees2"]))
    # print_table(intersect(relations["Employees"], relations["Employees2"]))
    # print_table(minus(relations["Employees"], relations["Employees2"]))
    # print_table(minus(relations["Employees2"], relations["Employees"]))
    rel1 = """A (X) = {
    1
    2
    3
    }"""

    rel2 = """B (X) = {
    2
    3
    4
    }"""

    rel3 = """C (X) = {
    3
    4
    5
    }"""

    rel4 = """D (Y) = {
    10
    20
    }"""

    create_relation(rel1)
    create_relation(rel2)
    create_relation(rel3)
    create_relation(rel4)

    print("Testing: A")
    query, num = parse_expr(tokenize("A"))
    print_table(query)

    print("Testing: A union B")
    query, num = parse_expr(tokenize("A union B"))
    print_table(query)

    print("Testing: A intersect B")
    query, num = parse_expr(tokenize("A intersect B"))
    print_table(query)

    print("Testing: A minus B")
    query, num = parse_expr(tokenize("A minus B"))
    print_table(query)

    print("Testing: A times D")
    query, num = parse_expr(tokenize("A times D"))
    print_table(query)

    print("Testing: A union B minus C")
    query, num = parse_expr(tokenize("A union B minus C"))
    print_table(query)

    print("Testing: A minus B minus C")
    query, num = parse_expr(tokenize("A minus B minus C"))
    print_table(query)

    print("Testing: A union B intersect C")
    query, num = parse_expr(tokenize("A union B intersect C"))
    print_table(query)

    print("Testing: A times D union B")
    query, num = parse_expr(tokenize("A times D union B"))
    print_table(query)


if __name__ == "__main__":
    main()