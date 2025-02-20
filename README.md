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
