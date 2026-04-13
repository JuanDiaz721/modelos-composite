# Visualizador de Árboles de Expresiones Aritméticas 🌳🧮

Este proyecto es una implementación interactiva en Python que analiza expresiones matemáticas en texto, construye un Árbol de Sintaxis Abstracta (AST) y lo resuelve. 

El núcleo arquitectónico del proyecto está basado en el **Patrón de Diseño Composite**, lo que permite evaluar recursivamente estructuras jerárquicas complejas de manera limpia, uniforme y orientada a objetos.

## 🚀 Características

* **Parser de Descenso Recursivo:** Tokeniza y analiza sintácticamente (parsing) expresiones matemáticas ingresadas por el usuario teniendo en cuenta la precedencia de operadores y agrupación por paréntesis.
* **Patrón Composite:** Arquitectura robusta que trata los valores numéricos (Hojas) y las operaciones matemáticas (Compuestos) bajo una misma interfaz polimórfica.
* **Visualización ASCII:** Renderizado dinámico del árbol binario en consola, calculando de manera automática el espaciado, los conectores y el centrado de los nodos.
* **Manejo de Excepciones:** Detección de errores de sintaxis y divisiones por cero en tiempo de evaluación.

## 🏗️ Arquitectura (Patrón Composite)

El proyecto estructura la lógica matemática en tres niveles:
1.  **`ExpresionAritmetica` (Component):** La clase abstracta base que define los métodos `evaluar()`, `mostrar()` y `altura()`.
2.  **`Numero` (Leaf):** Nodos terminales del árbol. Contienen los valores numéricos y representan el caso base de la recursividad.
3.  **`Operacion` (Composite):** Nodos intermedios que contienen un operador matemático (`+`, `-`, `*`, `/`) y referencias a un nodo izquierdo y uno derecho. Delegan la evaluación a sus hijos antes de ejecutar su propia operación.

## 🛠️ Requisitos e Instalación

El proyecto está escrito en **Python puro**, aprovechando únicamente librerías estándar. No requiere instalaciones adicionales ni entornos virtuales complejos.

* Python 3.6 o superior.

Clona el repositorio y ejecuta el script principal:

```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO
python composite.py
