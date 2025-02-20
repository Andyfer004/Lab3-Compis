import os
from regex_parser import to_postfix
from syntax_tree import build_syntax_tree, generate_ast_graph
from afd_generator import compute_followpos, generate_afd
from afd_minimizer import minimize_afd
from validator import validate_string

print("¡Bienvenido al generador de AFD desde una expresión regular! 🎭")

while True:
    regex = input("\nIngrese la expresión regular (o 'salir' para terminar): ")
    if regex.lower() == 'salir':
        print("¡Gracias por usar el generador de AFD! 🚀")
        break

    # Convertir regex a postfix y construir árbol sintáctico
    postfix = to_postfix(regex + "#")
    root, positions = build_syntax_tree(postfix)
    followpos = compute_followpos(root, positions)

    # Crear carpeta específica para la regex
    regex_folder = f"regex-images-afddirect/{regex}"
    os.makedirs(regex_folder, exist_ok=True)

    # Generar AST y guardarlo
    generate_ast_graph(root).render(f"{regex_folder}/ast", format="png", cleanup=True)

    # Generar AFD y guardarlo
    afd, afd_dict = generate_afd(root, positions, followpos)
    afd.render(f"{regex_folder}/afd", format="png", cleanup=True)

    # Minimizar el AFD y guardarlo
    minimized_afd = minimize_afd(afd_dict)
    minimized_afd.render(f"{regex_folder}/afd_minimized", format="png", cleanup=True)

    print(f"\n🔹 Diagramas generados en: {regex_folder}")
    
    # Comenzar a validar cadenas hasta que el usuario quiera salir
    while True:
        string = input("\nIngrese una cadena para verificar (o 'salir' para cambiar de regex): ")
        if string.lower() == 'salir':
            break
        
        if validate_string(afd_dict, string):
            print(f"✅ La cadena '{string}' ES ACEPTADA por la expresión regular.")
        else:
            print(f"❌ La cadena '{string}' NO ES ACEPTADA por la expresión regular.")

print("\nFin del programa. 😊")
