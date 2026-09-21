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
    for row in R[2:]:
        evaluation = evaluate_condition(condition, R[1], row)
        if evaluation is None:
            return None
        if evaluation:
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
    if R1[1] != R2[1]:
        print(
            f"Syntax error: Cannot union relations with different schemas: "
            f"{R1[1]} and {R2[1]}"
        )
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
    if R1[1] != R2[1]:
        print(
            f"Syntax error: Cannot intersect relations with different schemas: "
            f"{R1[1]} and {R2[1]}"
        )
        return None
    intersect = [R1[0]]
    intersect.append(R1[1])
    for row1 in R1[2:]:
        for row2 in R2[2:]:
            if row1 == row2:
                intersect.append(row1)
    return intersect

def minus(R1: list[tuple[str]], R2: list[tuple[str]]):
    if R1[1] != R2[1]:
        print(
            f"Syntax error: Cannot minus relations with different schemas: "
            f"{R1[1]} and {R2[1]}"
        )
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

def rename(R1: list[tuple[str]], name: str):
    new_relation = R1.copy()
    new_relation[0] = name
    relations[name] = new_relation
    return relations[name]

def print_table(R: list[tuple[str]]):
    print(R[0] + "\n")
    widths = [
        max(len(str(row[i])) for row in R[1:])
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

def print_tree(tree, indent="", last=True):
    if not tree:
        print("<empty tree>")
        return

    connector = "└── " if last else "├── "

    if tree[0] == "RELATION":
        print(indent + connector + tree[0] + ": " + tree[1])
        return

    print(indent + connector + tree[0])

    # Unary operations: SELECT, PROJECT, RENAME
    if tree[0] in ["SELECT", "PROJECT", "RENAME"]:
        print_tree(tree[1], indent + ("    " if last else "│   "), False)
        print_tree(tree[2], indent + ("    " if last else "│   "), True)

    # Binary operations: UNION, INTERSECT, MINUS, TIMES
    elif tree[0] in ["UNION", "INTERSECT", "MINUS", "TIMES"]:
        print_tree(tree[1], indent + ("    " if last else "│   "), False)
        print_tree(tree[2], indent + ("    " if last else "│   "), True)

    # JOIN has three children: left, right, condition
    elif tree[0] == "JOIN":
        print_tree(tree[1], indent + ("    " if last else "│   "), False)
        print_tree(tree[2], indent + ("    " if last else "│   "), False)
        print_tree(tree[3], indent + ("    " if last else "│   "), True)

    # Condition trees
    elif tree[0] in ["OR", "AND"]:
        print_tree(tree[1], indent + ("    " if last else "│   "), False)
        print_tree(tree[2], indent + ("    " if last else "│   "), True)

    elif tree[0] == "NOT":
        print_tree(tree[1], indent + ("    " if last else "│   "), True)

    elif tree[0] == "COMPARISON":
        operator, left, right = tree[1]
        print(indent + ("    " if last else "│   ") + "├── " + operator)
        print(indent + ("    " if last else "│   ") + "├── " + str(left))
        print(indent + ("    " if last else "│   ") + "└── " + str(right))


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
    
        # Check if boolean operator
        if c in ["a", "o", "n"]:
            if c == "a":
                if query[position:position + 3] == "and":
                    next_pos = position + 3
                    if next_pos == len(query) or not (query[next_pos].isalnum() or query[next_pos] == "_"):
                        tokens.append("AND:and")
                        position += 3
                        continue

            if c == "o":
                if query[position:position + 2] == "or":
                    next_pos = position + 2
                    if next_pos == len(query) or not (query[next_pos].isalnum() or query[next_pos] == "_"):
                        tokens.append("OR:or")
                        position += 2
                        continue

            if c == "n":
                if query[position:position + 3] == "not":
                    next_pos = position + 3
                    if next_pos == len(query) or not (query[next_pos].isalnum() or query[next_pos] == "_"):
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

        # Check if binary op except join
        if c in ["t", "u", "i", "m"]:
            if c == "t": #Needs to recognize trailing binary op as binary op despite no following space to give correct failure error
                if query[position - 1:position + 6] == " times " or (query[position - 1:position + 5] == " times" and len(query) == position + 5):
                    tokens.append("TIMES:times")
                    position += 5
                    continue

            if c == "u":
                if query[position - 1:position + 6] == " union " or (query[position - 1:position + 5] == " union" and len(query) == position + 5):
                    tokens.append("UNION:union")
                    position += 5
                    continue

            if c == "i":
                if query[position - 1:position + 10] == " intersect " or (query[position - 1:position + 9] == " intersect" and len(query) == position + 9):
                    tokens.append("INTERSECT:intersect")
                    position += 9
                    continue

            if c == "m":
                if query[position - 1:position + 6] == " minus " or (query[position - 1:position + 5] == " minus" and len(query) == position + 5):
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
    print(tokens)
    result = parse_join_expr(tokens)
    if not result:
        return None
    leftJoinExpr, num_consumed = result
    total_num_consumed = num_consumed
    if num_consumed == len(tokens):
        return leftJoinExpr, total_num_consumed
    tokens = tokens[num_consumed:]
    while tokens[0] in ["UNION:union", "INTERSECT:intersect", "MINUS:minus", "TIMES:times"]:
        operator = tokens[0]
        if len(tokens) == 1:
            print(f"Syntax error: binary operator {operator} must be followed by a join-expr, cannot be empty.")
            return None
        result = parse_join_expr(tokens[1:])
        if not result:
            return None
        rightJoinExpr, num_consumed = result
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
    result = parse_primary_expr(tokens)
    if not result:
        return None
    leftPrimaryExpr, num_consumed = result
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
        result = parse_condition(condition_tokens)
        if not result:
            return None
        condition, condition_num_consumed = result
        if condition_num_consumed != len(condition_tokens):
            print("Syntax error: Join condition consumption did not match expected value.")
            return None
        result = parse_primary_expr(tokens[rConIndex + 1:])
        if not result:
            return None
        rightPrimaryExpr, right_num_consumed = result
        total_num_consumed += condition_num_consumed + right_num_consumed + 3 # +3 is for join, [ and ]
        expr = ("JOIN", leftPrimaryExpr, rightPrimaryExpr, condition)
        if right_num_consumed == len(tokens[rConIndex + 1:]):
            return expr, total_num_consumed
        tokens = tokens[rConIndex + 1 + right_num_consumed:]
        leftPrimaryExpr = expr
    return leftPrimaryExpr, total_num_consumed

def parse_primary_expr(tokens: list[str]):
    if len(tokens) == 0:
        print("Syntax error: expected primary expr")
        return None

    if tokens[0] == "LEFTP:(":
        result = parse_expr(tokens[1:])
        if not result:
            return None
        expr, num_consumed = result
        if num_consumed == len(tokens[1:]) or tokens[num_consumed + 1] != "RIGHTP:)":
            print(f"Syntax error: Never closed ( for nested expression {tokens[1:]}")
            return None
        
        return expr, num_consumed + 2
    elif tokens[0] in ["SELECT:select", "PROJECT:project", "RENAME:rename"]:
        if "LEFTS:[" not in tokens or tokens[1] != "LEFTS:[":
            print("Syntax error: unary operator must be followed by [.")
            return None
        if "RIGHTS:]" not in tokens:
            print("Syntax error: Condition for unary statement must be closed with ].")
            return None
        lConIndex = tokens.index("LEFTS:[")
        rConIndex = tokens.index("RIGHTS:]")
        if rConIndex == 2:
            print("Syntax error: unary condition cannot be empty")
            return None
        if rConIndex == len(tokens) - 1:
            print("Syntax error: Must have expression after unary condition")
            return None
        condition_tokens = tokens[lConIndex + 1:rConIndex]
        match tokens[0]:
            case "SELECT:select":
                result = parse_condition(condition_tokens)
            case "PROJECT:project":
                result = parse_attribute_list(condition_tokens)
            case "RENAME:rename":
                result = parse_new_name(condition_tokens) 
        if not result:
            return None
        condition, condition_num_consumed = result
        if condition_num_consumed != len(condition_tokens):
            print("Syntax error: Unary condition consumption did not match expected value.")
            return None 
        if "LEFTP:(" not in tokens or tokens[rConIndex + 1] != "LEFTP:(":
            print(f"Syntax error: Require nested ( expression ) after condition for unary expression {tokens[0]}")
            return None
        result = parse_expr(tokens[rConIndex + 2:])
        if not result:
            return None
        base_expr, num_consumed = result
        if num_consumed == len(tokens[rConIndex + 2:]) or tokens[rConIndex + num_consumed + 2] != "RIGHTP:)":
            print(f"Syntax error: Never closed ( for nested expression {tokens[rConIndex+1:]}")
            return None
        total_num_consumed = condition_num_consumed + num_consumed + 5 # +5 is for unary, [, ], (, and )
        match tokens[0]:
            case "SELECT:select":
                expr = ("SELECT", base_expr, condition)
            case "PROJECT:project":
                expr = ("PROJECT", base_expr, condition)
            case "RENAME:rename":
                expr = ("RENAME", base_expr, condition)
        return expr, total_num_consumed
    else:  # Relation
        if not tokens[0].startswith("RELATION:") or len(tokens[0]) == len("RELATION:"):
            print("Syntax error: Expected a non-empty relation name")
            return None

        relation_name = tokens[0][len("RELATION:"):]
        return ("RELATION", relation_name), 1
    
def parse_attribute_list(tokens: list[str]):
    if not tokens:
        print("Must provide at least one column name for projection")
        return None
    if len(tokens) % 2 == 0:
        print("Projection attribute list must have odd number of tokens")
        return None
    names = []
    for i in range(len(tokens)):
        if i % 2 == 0: #All even elements must be RELATION, all odds must be COMMA
            if not tokens[i].startswith("RELATION:"):
                print("Each element in attribute list must be of type RELATION")
                return None
            names.append(tokens[i][tokens[i].index(":")+1:])
        else:
            if not tokens[i] == "COMMA:,":
                print("Each element in attribute list must be seperated by comma")
                return None
        
    return ("ATTRIBUTE_LIST", names), len(tokens)

def parse_new_name(tokens: list[str]):
    if not tokens:
        print("Must provide argument for new name for RENAME")
        return None
    if len(tokens) > 1:
        print("Only provide one argument for new name for RENAME")
        return None
    new_name = tokens[0]
    if not new_name.startswith("RELATION:"):
        print("New name arg for rename must of type RELATION")
        return None
    new_name = new_name[9:]
    if not new_name or not new_name[0].isalpha() or not all(c.isalnum() or c == "_" for c in new_name):
        print("Relation name must being with alpha character and contain only alphanumeric characters or '_'")
        return None

    return ("STR", new_name), 1

def parse_condition(tokens: list[str]):
    result = parse_and_condition(tokens)
    if not result:
        return None
    leftAndCondition, num_consumed = result
    total_num_consumed = num_consumed
    if num_consumed == len(tokens):
        return leftAndCondition, total_num_consumed
    tokens = tokens[num_consumed:]
    while tokens[0] == "OR:or":
        if len(tokens) == 1:
            print(f"Syntax error: or operator must be followed by comparison or nested condition")
            return None
        result = parse_and_condition(tokens[1:])
        if not result:
            return None
        rightAndCondition, num_consumed = result
        total_num_consumed += num_consumed + 1
        condition = ("OR", leftAndCondition, rightAndCondition)
        if num_consumed == len(tokens[1:]):
            return condition, total_num_consumed
        tokens = tokens[num_consumed + 1:]
        leftAndCondition = condition
    return leftAndCondition, total_num_consumed



def parse_and_condition(tokens: list[str]):
    result = parse_not_condition(tokens)
    if not result:
        return None
    leftNotCondition, num_consumed = result
    total_num_consumed = num_consumed
    if num_consumed == len(tokens):
        return leftNotCondition, total_num_consumed
    tokens = tokens[num_consumed:]
    while tokens[0] == "AND:and":
        if len(tokens) == 1:
            print(f"Syntax error: and operator must be followed by comparison or nested condition")
            return None
        result = parse_not_condition(tokens[1:])
        if not result:
            return None
        rightNotCondition, num_consumed = result
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

        result = parse_not_condition(tokens[1:])

        if not result:
            return None
        condition, num_consumed = result

        return ("NOT", condition), num_consumed + 1

    return parse_condition_base(tokens)

def parse_condition_base(tokens: list[str]):

    if len(tokens) == 0:
        print("Syntax error: expected condition")
        return None

    if tokens[0] == "LEFTP:(":
        result = parse_condition(tokens[1:])
        if not result:
            return None
        condition, num_consumed = result
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
    if operand.startswith("RELATION:"):
        return ("ATTRIBUTE", operand[operand.index(":")+1:])
    if operand.startswith("INT:"):
        return ("INT", int(operand[operand.index(":")+1:]))
    if operand.startswith("STR:"):
        return ("STR", operand[operand.index(":")+1:])
    print(f"Operand must be of type RELATION, INT, or STR: {operand}")
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

def evaluate_expr(parse_tree):
    if not (parse_tree):
        print("Empty tree")
        return None
    match parse_tree[0]:
        case "RELATION":
            name = parse_tree[1]
            if name not in relations:
                print(f"Name Error: Relation {name} does not exist")
                return None
            return relations[name]

        case "SELECT":
            expr = evaluate_expr(parse_tree[1])
            if expr is None:
                return None
            return select(expr, parse_tree[2])

        case "PROJECT":
            expr = evaluate_expr(parse_tree[1])
            if expr is None:
                return None
            return project(expr, parse_tree[2][1])

        case "RENAME":
            expr = evaluate_expr(parse_tree[1])
            if expr is None:
                return None
            return rename(expr, parse_tree[2][1])

        case "UNION":
            expr1 = evaluate_expr(parse_tree[1])
            expr2 = evaluate_expr(parse_tree[2])
            if expr1 is None or expr2 is None:
                return None
            return union(expr1, expr2)

        case "INTERSECT":
            expr1 = evaluate_expr(parse_tree[1])
            expr2 = evaluate_expr(parse_tree[2])
            if expr1 is None or expr2 is None:
                return None
            return intersect(expr1, expr2)

        case "MINUS":
            expr1 = evaluate_expr(parse_tree[1])
            expr2 = evaluate_expr(parse_tree[2])
            if expr1 is None or expr2 is None:
                return None
            return minus(expr1, expr2)

        case "TIMES":
            expr1 = evaluate_expr(parse_tree[1])
            expr2 = evaluate_expr(parse_tree[2])
            if expr1 is None or expr2 is None:
                return None
            return times(expr1, expr2)

        case "JOIN":
            expr1 = evaluate_expr(parse_tree[1])
            expr2 = evaluate_expr(parse_tree[2])
            if expr1 is None or expr2 is None:
                return None
            return join(expr1, expr2, parse_tree[3])


def main():

    if "--tree" in sys.argv:
        query = sys.argv[-1]
        tokens = tokenize(query)
        if tokens is None:
            return
        parse_tree = parse_expr(tokens)
        if parse_tree is None:
            return
        print_tree(parse_tree[0])
        return

    while(True):
        query = input(">")
        if query in ["quit", "exit"]:
            return
        tokens = tokenize(query)
        if tokens is None:
            continue
        if len(tokens) >= 2 and tokens[0].startswith("RELATION:") and tokens[1] == "LEFTP:(":
            while "}" not in query:
                query += "\n" + input()
            create_relation(query)
        else:
            parse_tree = parse_expr(tokens)
            if parse_tree is None:
                continue
            evaluation = evaluate_expr(parse_tree[0])
            if evaluation is None:
                continue
            print_table(evaluation)



if __name__ == "__main__":
    main()