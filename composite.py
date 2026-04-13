from abc import ABC, abstractmethod
from typing import Tuple, List

# ── Componente base (Component) ──────────────────────────────────────────────
class ExpresionAritmetica(ABC):
    @abstractmethod
    def evaluar(self) -> float:
        pass

    @abstractmethod
    def mostrar(self, nivel: int = 0) -> str:
        pass

    @abstractmethod
    def altura(self) -> int:
        pass


# ── Hoja (Leaf) ───────────────────────────────────────────────────────────────
class Numero(ExpresionAritmetica):
    def __init__(self, valor: float):
        self.valor = valor

    def evaluar(self) -> float:
        return self.valor

    def altura(self) -> int:
        return 1

    def mostrar(self, nivel: int = 0) -> str:
        v = int(self.valor) if self.valor == int(self.valor) else self.valor
        return str(v)


# ── Compuesto (Composite) ─────────────────────────────────────────────────────
class Operacion(ExpresionAritmetica):
    SIMBOLOS = {"+": "+", "-": "-", "*": "×", "/": "÷"}

    def __init__(self, operador: str, izquierdo: ExpresionAritmetica, derecho: ExpresionAritmetica):
        self.operador = operador
        self.izquierdo = izquierdo
        self.derecho = derecho

    def evaluar(self) -> float:
        izq = self.izquierdo.evaluar()
        der = self.derecho.evaluar()
        if self.operador == "+": return izq + der
        if self.operador == "-": return izq - der
        if self.operador == "*": return izq * der
        if self.operador == "/":
            if der == 0:
                raise ZeroDivisionError("División entre cero.")
            return izq / der

    def altura(self) -> int:
        return 1 + max(self.izquierdo.altura(), self.derecho.altura())

    def mostrar(self, nivel: int = 0) -> str:
        return self.SIMBOLOS[self.operador]


# ── Visualización vertical centrada ──────────────────────────────────────────

def obtener_lineas(nodo: ExpresionAritmetica) -> Tuple[List[str], int, int, int]:
    """
    Retorna (lineas, ancho, pos_izq_borde, pos_der_borde).
    - lineas:         lista de strings, cada uno es una fila del árbol
    - ancho:          ancho total del bloque
    - pos_izq_borde:  posición x del borde izquierdo del nodo raíz
    - pos_der_borde:  posición x del borde derecho del nodo raíz
    """
    etiqueta = nodo.mostrar()
    largo = len(etiqueta)

    if isinstance(nodo, Numero):
        # Nodo hoja: se encierra en ( )
        caja = f"({etiqueta})"
        return [caja], len(caja), 0, len(caja) - 1

    # Nodo compuesto: obtener bloques de hijos
    lineas_izq, ancho_izq, _, borde_der_izq = obtener_lineas(nodo.izquierdo)
    lineas_der, ancho_der, borde_izq_der, _ = obtener_lineas(nodo.derecho)

    GAP = 2  # espacio entre subárboles

    # Caja del operador
    caja_op = f"({etiqueta})"
    largo_op = len(caja_op)

    # Centro de cada subárbol (donde se conecta la línea)
    centro_izq = (borde_der_izq) // 2 + (ancho_izq - borde_der_izq - 1) // 2 + borde_der_izq // 2
    # Más preciso: centro del nodo raíz del hijo izquierdo
    centro_izq = (0 + borde_der_izq) // 2
    centro_der = ancho_izq + GAP + (borde_izq_der + ancho_der) // 2

    ancho_hijos = ancho_izq + GAP + ancho_der

    # Posición x del operador: centrado entre los dos hijos
    pos_op = (centro_izq + centro_der - largo_op + 1) // 2
    pos_op = max(pos_op, 0)

    ancho_total = max(ancho_hijos, pos_op + largo_op)

    # ── Fila del operador ─────────────────────────────────────────────────────
    fila_op = " " * pos_op + caja_op
    fila_op = fila_op.ljust(ancho_total)

    centro_op = pos_op + largo_op // 2

    # ── Fila de conectores (/ \) ──────────────────────────────────────────────
    fila_conex = [" "] * ancho_total
    # Barra izquierda: desde centro_op-1 hasta centro_izq+1
    for x in range(centro_izq + 1, centro_op):
        fila_conex[x] = "─"
    fila_conex[centro_izq] = "┌" if centro_izq < centro_op else "│"
    fila_conex[centro_op]  = "┴" if centro_izq < centro_op < centro_der else "│"
    # Barra derecha: desde centro_op+1 hasta centro_der-1
    for x in range(centro_op + 1, centro_der):
        fila_conex[x] = "─"
    if centro_der < ancho_total:
        fila_conex[centro_der] = "┐"
    fila_conex = "".join(fila_conex)

    # ── Filas de los hijos (alineadas lado a lado) ────────────────────────────
    max_filas = max(len(lineas_izq), len(lineas_der))
    lineas_izq  += [" " * ancho_izq]  * (max_filas - len(lineas_izq))
    lineas_der  += [" " * ancho_der]  * (max_filas - len(lineas_der))

    filas_hijos = []
    for li, ld in zip(lineas_izq, lineas_der):
        fila = li.ljust(ancho_izq) + " " * GAP + ld.ljust(ancho_der)
        filas_hijos.append(fila.ljust(ancho_total))

    lineas = [fila_op, fila_conex] + filas_hijos

    return lineas, ancho_total, pos_op, pos_op + largo_op - 1


def visualizar_arbol(nodo: ExpresionAritmetica, expresion: str):
    lineas, _, _, _ = obtener_lineas(nodo)
    resultado = nodo.evaluar()
    resultado_fmt = int(resultado) if resultado == int(resultado) else resultado

    ancho_total = max(len(l) for l in lineas)
    borde = "═" * (ancho_total + 4)

    print(f"\n  ╔{borde}╗")
    print(f"  ║  Expresión: {expresion.ljust(ancho_total - 9)}  ║")
    print(f"  ╠{borde}╣")
    for linea in lineas:
        print(f"  ║  {linea.ljust(ancho_total)}  ║")
    print(f"  ╠{borde}╣")
    print(f"  ║  Resultado = {str(resultado_fmt).ljust(ancho_total - 11)}  ║")
    print(f"  ╚{borde}╝\n")


# ── Parser ────────────────────────────────────────────────────────────────────
def tokenizar(expr: str) -> list:
    tokens = []
    i = 0
    expr = expr.replace(" ", "")
    while i < len(expr):
        if expr[i].isdigit() or (expr[i] == '.' and i+1 < len(expr) and expr[i+1].isdigit()):
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
        elif expr[i] in "+-*/()":
            tokens.append(expr[i])
            i += 1
        else:
            raise ValueError(f"Carácter no reconocido: '{expr[i]}'")
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self, esperado=None):
        tok = self.actual()
        if esperado and tok != esperado:
            raise SyntaxError(f"Se esperaba '{esperado}', se encontró '{tok}'")
        self.pos += 1
        return tok

    def parsear(self):
        nodo = self.expr()
        if self.actual() is not None:
            raise SyntaxError(f"Token inesperado: '{self.actual()}'")
        return nodo

    def expr(self):
        nodo = self.termino()
        while self.actual() in ("+", "-"):
            op = self.consumir()
            nodo = Operacion(op, nodo, self.termino())
        return nodo

    def termino(self):
        nodo = self.factor()
        while self.actual() in ("*", "/"):
            op = self.consumir()
            nodo = Operacion(op, nodo, self.factor())
        return nodo

    def factor(self):
        tok = self.actual()
        if tok == "(":
            self.consumir("(")
            nodo = self.expr()
            self.consumir(")")
            return nodo
        try:
            self.consumir()
            return Numero(float(tok))
        except (TypeError, ValueError):
            raise SyntaxError(f"Se esperaba un número, se encontró: '{tok}'")


def construir_arbol(expresion: str) -> ExpresionAritmetica:
    return Parser(tokenizar(expresion)).parsear()


# ── Interfaz de consola ───────────────────────────────────────────────────────
def main():
    print("\n  ╔══════════════════════════════════════════════╗")
    print("  ║   Árbol Binario de Expresiones — Composite  ║")
    print("  ╚══════════════════════════════════════════════╝")
    print("  Operadores : + - * /     Agrupación: ( )")
    print("  Ejemplos   : (4+5) + (2*5)  |  (4*3-5) + (2/2+1)")
    print("  Salir      : escribir 'salir'\n")

    while True:
        entrada = input("  Expresión: ").strip()
        if entrada.lower() in ("salir", "exit", "q"):
            print("\n  ¡Hasta luego!\n")
            break
        if not entrada:
            continue
        try:
            arbol = construir_arbol(entrada)
            visualizar_arbol(arbol, entrada)
        except ZeroDivisionError as e:
            print(f"\n  ⚠  {e}\n")
        except (SyntaxError, ValueError) as e:
            print(f"\n  ⚠  Expresión inválida: {e}\n")


if __name__ == "__main__":
    main()
