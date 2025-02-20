# syntax_tree.py

from utils import is_operand
import graphviz

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.firstpos = set()
        self.lastpos = set()
        self.nullable = False
        self.position = None

def build_syntax_tree(postfix):
    stack = []
    position = 1
    positions = {}

    for token in postfix:
        if is_operand(token) or token == '#':
            node = Node(token)
            node.position = position
            node.firstpos = {position}
            node.lastpos = {position}
            node.nullable = False
            positions[position] = node
            stack.append(node)
            position += 1
        elif token == '*':
            operand = stack.pop()
            node = Node(token, operand)
            node.nullable = True
            node.firstpos = operand.firstpos
            node.lastpos = operand.lastpos
            stack.append(node)
        elif token in {'|', '.'}:
            right = stack.pop()
            left = stack.pop()
            node = Node(token, left, right)

            if token == '|':
                node.nullable = left.nullable or right.nullable
                node.firstpos = left.firstpos | right.firstpos
                node.lastpos = left.lastpos | right.lastpos
            else:
                node.nullable = left.nullable and right.nullable
                node.firstpos = left.firstpos | (right.firstpos if left.nullable else set())
                node.lastpos = right.lastpos | (left.lastpos if right.nullable else set())

            stack.append(node)

    return stack[0], positions

def generate_ast_graph(root):
    dot = graphviz.Digraph('AST')

    def add_nodes(node, parent_id=None):
        if node:
            node_id = str(id(node))
            label = f"{node.value}"
            if node.position:
                label += f" ({node.position})"
            dot.node(node_id, label)

            if parent_id:
                dot.edge(parent_id, node_id)

            add_nodes(node.left, node_id)
            add_nodes(node.right, node_id)

    add_nodes(root)
    return dot