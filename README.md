# Construcción de un DFA directamente desde una Expresión Regular (r.e)

## Expresión Regular

Dada la expresión regular **r = (a|b)*abb**, el objetivo es construir un DFA directamente a partir del árbol sintáctico generado.

---

## Pasos de Construcción

### **1. Aumentar la expresión regular**

- Se añade un símbolo especial `#` al final para marcar el fin de la cadena:

  ```markdown
  r = (a|b)*abb#
  ```

Este proceso se realiza en `main.py`, donde el usuario ingresa la expresión regular y se concatena `#` antes de su procesamiento.

---

### **2. Conversión a Notación Postfix**

- Se utiliza el algoritmo *Shunting Yard* para convertir la expresión infija a notación postfix.
- Se emplea la función `to_postfix` en `regex_parser.py`.

Ejemplo:

  ```python
  from regex_parser import to_postfix
  postfix = to_postfix("(a|b)*abb#")
  print(postfix)  # ['a', 'b', '|', '*', 'a', 'b', 'b', '.', '.', '#', '.']
  ```

---

### **3. Construcción del Árbol Sintáctico**

- Se crea un árbol sintáctico a partir de la notación postfix con `build_syntax_tree` en `syntax_tree.py`.
- Se asignan posiciones a las hojas y se calculan `nullable`, `firstpos`, y `lastpos`.

Ejemplo:

  ```python
  from syntax_tree import build_syntax_tree
  root, positions = build_syntax_tree(postfix)
  ```

---

### **4. Cálculo de `followpos`**

- Se computan los `followpos` recorriendo el árbol y aplicando las reglas en `compute_followpos` de `afd_generator.py`.

Ejemplo:

  ```python
  from afd_generator import compute_followpos
  followpos = compute_followpos(root, positions)
  ```

**Tabla de `Followpos` generada:**

  ```markdown
  | Posición | Siguiente Pos |
  |----------|---------------|
  |    1     | {1, 2}        |
  |    2     | {1, 2}        |
  |    3     | {4}           |
  |    4     | {5}           |
  |    5     | {6}           |
  |    6     | ∅             |
  ```

---

### **5. Generación del AFD**

- Se crean los estados del AFD utilizando `generate_afd` en `afd_generator.py`.
- Se define un estado inicial a partir de `firstpos` de la raíz.
- Se iteran las transiciones según `followpos`.

Ejemplo:

  ```python
  from afd_generator import generate_afd
  afd, afd_dict = generate_afd(root, positions, followpos)
  ```

**Estados del AFD generados:**

  ```markdown
  A = {1, 2, 3}
  B = {1, 2, 4}
  C = {5}
  D = {6} (Estado de aceptación)
  ```

El AFD se guarda como una imagen en `regex-images-afddirect/` usando Graphviz.

---

### **6. Minimización del AFD**

- Se usa `minimize_afd` en `afd_minimizer.py` para reducir el número de estados.

Ejemplo:

  ```python
  from afd_minimizer import minimize_afd
  minimized_afd = minimize_afd(afd_dict)
  ```

El AFD minimizado también se almacena en `regex-images-afddirect/`.

---

### **7. Simulación del AFD**

- La función `validate_string` en `validator.py` verifica si una cadena es aceptada por el AFD.

Ejemplo:

  ```python
  from validator import validate_string
  resultado = validate_string(afd_dict, "abb")
  print(resultado)  # True (Cadena aceptada)
  ```

---

### **8. Generación Visual de los Autómatas**

- Se usan funciones de Graphviz en `syntax_tree.py`, `afd_generator.py` y `afd_minimizer.py` para graficar:
  - `generate_ast_graph(root)`: Genera el árbol sintáctico.
  - `generate_afd(root, positions, followpos)`: Genera el AFD.
  - `minimize_afd(afd_dict)`: Genera el AFD minimizado.

Los diagramas se almacenan en `regex-images-afddirect/`.

---

## **Resumen**

1. Se ingresa una expresión regular en `main.py`.
2. `to_postfix` en `regex_parser.py` la convierte a notación postfix.
3. `build_syntax_tree` en `syntax_tree.py` genera el árbol sintáctico.
4. `compute_followpos` en `afd_generator.py` calcula los `followpos`.
5. `generate_afd` en `afd_generator.py` construye el AFD.
6. `minimize_afd` en `afd_minimizer.py` minimiza el AFD.
7. `validate_string` en `validator.py` permite simular la validación de cadenas.
8. Se crean representaciones visuales con Graphviz.

Este procedimiento ilustra cómo derivar un DFA directamente desde una expresión regular utilizando el árbol sintáctico y la construcción directa del AFD.




# Simulación de un Autómata desde una Expresión Regular

## Expresión Regular

Dada una expresión regular, el objetivo es convertirla en un autómata finito no determinista (AFN), transformarlo en un autómata finito determinista (AFD), minimizarlo y simular su comportamiento con cadenas de entrada.

---

## Pasos de Construcción

### **1. Convertir Expresión Regular de Infija a Postfija**

- Se utiliza el algoritmo *Shunting Yard* para convertir la expresión infija a notación postfix.
- Se emplea la función `toPostFix` en `shunYard.py`.

Ejemplo:

  ```python
  from shunYard import toPostFix
  postfix = toPostFix("(a|b)*abb")
  print(postfix)  # ['a', 'b', '|', '*', 'a', 'b', 'b', '.','.']
  ```

---

### **2. Construcción del Autómata Finito No Determinista (AFN)**

- Se construye un AFN a partir de la notación postfix usando `toAFN` en `regexToAFN.py`.
- Se utiliza una pila para evaluar los operadores de concatenación (`.`), unión (`+`) y cierre de Kleene (`*`).

Ejemplo:

  ```python
  from regexToAFN import toAFN
  afn = toAFN(postfix)
  print(afn)  # Representación del AFN en diccionario
  ```

---

### **3. Conversión del AFN a AFD**

- Se emplea `fromAFNToAFD` en `AFNToAFD.py`.
- Se calcula el cierre-ε y se generan los estados del AFD a partir del AFN.

Ejemplo:

  ```python
  from AFNToAFD import fromAFNToAFD
  afd = fromAFNToAFD(afn)
  print(afd)  # Transiciones y estados del AFD
  ```

---

### **4. Minimizar el AFD**

- Se minimiza el AFD usando `minimize_afd` en `minimizeAFD.py`.
- Se agrupan estados equivalentes y se redefinen las transiciones.

Ejemplo:

  ```python
  from minimizeAFD import minimize_afd
  minimized_afd = minimize_afd(afd)
  print(minimized_afd)  # Representación minimizada del AFD
  ```

---

### **5. Generación Visual de los Autómatas**

- Se generan diagramas de los autómatas usando `generate_graph` en `simulate.py`.
- Los autómatas se almacenan en `automaton_graphs/`.

Ejemplo:

  ```python
  from simulate import generate_graph
  generate_graph(afn, "AFN", "./output")
  generate_graph(afd, "AFD", "./output")
  generate_graph(minimized_afd, "Minimized_AFD", "./output")
  ```

---

### **6. Simulación de Cadenas en el AFD Minimizado**

- Se utiliza `simulate_regexp_process` en `simulate.py`.
- Se verifica si una cadena es aceptada por el autómata minimizado.

Ejemplo:

  ```python
  from simulate import simulate_regexp_process
  simulate_regexp_process("(a|b)*abb", "abb")
  ```

---

## **Resumen**

1. Se convierte la expresión regular de infija a postfija en `shunYard.py`.
2. Se genera un AFN en `regexToAFN.py`.
3. Se transforma el AFN en AFD en `AFNToAFD.py`.
4. Se minimiza el AFD en `minimizeAFD.py`.
5. Se generan representaciones visuales en `simulate.py`.
6. Se simula la validación de cadenas en `simulate.py`.

Este procedimiento ilustra la construcción y simulación de autómatas finitos desde una expresión regular utilizando distintos algoritmos.


