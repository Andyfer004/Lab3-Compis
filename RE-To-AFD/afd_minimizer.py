import graphviz

def minimize_afd(afd_dict):
    """
    Minimiza un AFD representado como un diccionario.
    Devuelve el AFD minimizado en formato Graphviz.
    """
    accepted_states = set(afd_dict['accepted'])
    state_groups = {}

    # Agrupar estados según sus transiciones y si son de aceptación
    for state, transitions in afd_dict['transitions'].items():
        is_accepted = state in accepted_states
        key = (frozenset(transitions.items()), is_accepted)
        if key not in state_groups:
            state_groups[key] = []
        state_groups[key].append(state)

    minimized_transitions = {}
    minimized_accepted = set()
    minimized_states = {}

    state_counter = 0

    # Crear un nuevo conjunto de estados minimizados
    for group in state_groups.values():
        representative = frozenset(group)
        minimized_states[representative] = f"M{state_counter}"
        state_counter += 1

    minimized_afd = graphviz.Digraph('Minimized_AFD')
    minimized_afd.attr(rankdir='LR')

    # Agregar nodo de inicio visible
    minimized_afd.node("", shape="none")
    minimized_afd.edge("", minimized_states[frozenset([afd_dict['initial']])], label="")

    for group, representative in minimized_states.items():
        minimized_transitions[representative] = {}

        for input_char, next_state in afd_dict['transitions'][next(iter(group))].items():
            for next_group, next_rep in minimized_states.items():
                if next_state in next_group:
                    minimized_transitions[representative][input_char] = next_rep
                    break

        if any(state in accepted_states for state in group):
            minimized_accepted.add(representative)

    for state, transitions in minimized_transitions.items():
        minimized_afd.node(state, shape='doublecircle' if state in minimized_accepted else 'circle')

        for symbol, next_state in transitions.items():
            minimized_afd.edge(state, next_state, symbol)

    return minimized_afd