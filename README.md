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

