type AFNTransitions = list[dict[str, list[AFNState]]]
type AFNState = int


def toAFN(postfix: str):

    """ 
    Se convierte la expresion regular a notacion de tipo postfix a un automata finito no determinista
    """
    stack = []
    for char in postfix:
        match char:
            case ".":  # Concatenacion de AFNs
                afn2 = stack.pop()
                afn1 = stack.pop()

                afn1OriginalLength = len(afn1["transitions"])
                newAccepted = afn2["accepted"] + afn1OriginalLength

                # Add epsilon transition to start of AFN2
                afn1Accepted = afn1["accepted"]
                initializeOrAppend(
                    afn1["transitions"][afn1Accepted], "_", afn1OriginalLength
                )

                # Ajustar los indices índices de los estados de afn2 y unir sus transiciones
                afn1["transitions"] += mappedAFN2Transitions

                # Actualizar el estado de aceptacion 
                afn1["accepted"] = newAccepted
                stack.append(afn1)

            case "+":  # Union (OR) de dos AFNs
                afn2 = stack.pop()
                afn1 = stack.pop()

                lenAfn1 = len(afn1["transitions"])
                afn = newAFN([{"_": [2, 2 + lenAfn1]}, {}], 1)
                afnLength = len(afn["transitions"])
                mappedAFN1Transitions = displaceTransitions(afn1, afnLength)

                afn1Accepted = afn1["accepted"]
                initializeOrAppend(mappedAFN1Transitions[afn1Accepted], "_", 1)

                afnLength += lenAfn1
                mappedAFN2Transitions = displaceTransitions(afn2, afnLength)

                afn2Accepted = afn2["accepted"]
                initializeOrAppend(mappedAFN2Transitions[afn2Accepted], "_", 1)

                mappedAFN1Transitions += mappedAFN2Transitions
                afn["transitions"] += mappedAFN1Transitions
                stack.append(afn)

            case "*":  # Cerradura de Kleene (0 o más repeticiones)
                received = stack.pop()

                afn = newAFN([{"_": [1, 2]}, {}], 1)
                afnLength = len(afn["transitions"])
                mappedReceivedTransitions = displaceTransitions(received, afnLength)

                receivedAccepted = received["accepted"]
                initializeOrAppend(mappedReceivedTransitions[receivedAccepted], "_", 1)
                mappedReceivedTransitions[receivedAccepted]["_"].append(2)

                afn["transitions"] += mappedReceivedTransitions
                stack.append(afn)

            case _:
                stack.append(newAFN([{char: [1]}, {}], 1))
    return stack.pop()


def initializeOrAppend(dictionary: dict, key: str, append):
    """
    Agrega un valor a una clave en un diccionario. Si la clave no existe la inicializa
    """
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(append)


def displaceTransitions(afn, delta: int):

    """
    Como su nombre lo dice desplaza los indices de los estados en un AFN para evitar las colisones al unir los automatas.
    """
    return [
        {
            word: [d + delta for d in destinations]
            for (word, destinations) in transition.items()
        }
        for transition in afn["transitions"]
    ]


def newAFN(transitions: AFNTransitions, accepted: AFNState):

    """
    Crea el AFN con la estructura basica. 
    """
    return {
        "transitions": transitions,
        "accepted": accepted,
    }


if __name__ == "__main__":
    exampleAFN = toAFN("a*b._+")
    print(exampleAFN)
