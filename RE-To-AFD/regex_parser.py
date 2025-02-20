from utils import is_operand, insert_concatenation_operators

def to_postfix(infix):
    precedence = {'|': 1, '.': 2, '*': 3}
    output = []
    operators = []

    infix = insert_concatenation_operators(infix)

    for c in infix:
        if is_operand(c) or c == '#':
            output.append(c)
        elif c == '(':
            operators.append(c)
        elif c == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if operators:
                operators.pop()  
        else:  
            while operators and operators[-1] != '(' and \
                  (c != '*' and precedence.get(operators[-1], 0) >= precedence.get(c, 0)):
                output.append(operators.pop())
            operators.append(c)

    while operators:
        if operators[-1] != '(':
            output.append(operators.pop())
        else:
            operators.pop()

    return output
