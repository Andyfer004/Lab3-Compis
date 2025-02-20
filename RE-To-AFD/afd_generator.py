import graphviz

def compute_followpos(root, positions):
    """
    Calcula el followpos de cada posición en el árbol de sintaxis.
    """
    followpos = {pos: set() for pos in positions}

    def compute(node):
        if node:
            if node.value == '.':  # Concatenación
                for i in node.left.lastpos:
                    followpos[i] |= node.right.firstpos
            elif node.value == '*':  # Cerradura de Kleene
                for i in node.lastpos:
                    followpos[i] |= node.firstpos
            compute(node.left)
            compute(node.right)

    compute(root)
    return followpos

def generate_afd(root, positions, followpos):
    """
    Genera un AFD a partir del árbol de sintaxis y los followpos.
    Devuelve tanto el grafo de Graphviz como un diccionario con la estructura del AFD.
    """
    afd = graphviz.Digraph('AFD')
    afd.attr(rankdir='LR')

    initial_state = frozenset(root.firstpos)
    states = {initial_state: 'A'}
    unmarked_states = [initial_state]
    state_counter = 0

    final_position = next((pos for pos, node in positions.items() if node.value == '#'), None)

    afd_dict = {
        'transitions': {},
        'accepted': [],
        'initial': 'A'
    }

    # Añadir nodo vacío para indicar el estado inicial
    afd.node("", shape="none")
    afd.edge("", "A", label="")

    while unmarked_states:
        current_state = unmarked_states.pop(0)
        current_name = states[current_state]

        if final_position in current_state:
            afd_dict['accepted'].append(current_name)

        transitions = {}
        for pos in current_state:
            symbol = positions[pos].value
            if symbol != '#':  # No considerar el símbolo final
                transitions.setdefault(symbol, set()).update(followpos[pos])

        afd_dict['transitions'][current_name] = {}

        for symbol, next_positions in transitions.items():
            next_state = frozenset(next_positions)
            if next_state not in states:
                state_counter += 1
                state_name = chr(ord('A') + state_counter)
                states[next_state] = state_name
                unmarked_states.append(next_state)
            afd.edge(current_name, states[next_state], symbol)
            afd_dict['transitions'][current_name][symbol] = states[next_state]

    for state, name in states.items():
        afd.node(name, shape='doublecircle' if name in afd_dict['accepted'] else 'circle')

    return afd, afd_dict