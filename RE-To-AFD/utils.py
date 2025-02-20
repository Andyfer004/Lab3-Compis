def is_operator(c):
    return c in {'|', '.', '*', '(', ')', '#'}

def is_operand(c):
    return c.isalnum() and c not in {'|', '.', '*', '#', '(', ')'}


def insert_concatenation_operators(infix):
    output = []
    i = 0
    while i < len(infix):
        output.append(infix[i])
        if i < len(infix) - 1:
            current = infix[i]
            next_char = infix[i + 1]
            if (is_operand(current) or current == '*' or current == ')') and \
               (is_operand(next_char) or next_char == '(' or next_char == '#'):
                output.append('.')
        i += 1
    return ''.join(output)
