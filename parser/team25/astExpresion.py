from enum import Enum

# Enumeraciones para identificar expresiones que comparten clase


class OPERACION_ARITMETICA(Enum):
    MAS = 1
    MENOS = 2
    POR = 3
    DIVIDO = 4


class OPERACION_RELACIONAL(Enum):
    MAYORIGUAL  = 1
    MENORIGUAL  = 2
    MAYOR       = 3
    MENOR       = 4
    IGUAL       = 5
    DESIGUAL    = 6


class OPERACION_LOGICA(Enum):
    AND = 1
    OR = 2

# ------------------------ EXPRESIONES ----------------------------
# ------EXPRESIONES NUMERICAS

# Clase de expresion númerica (Abstracta)
class Expresion:
    def dibujar(self):
        pass

    def ejecutar(self, ts):
        pass

# Clase de expresión aritmética


class ExpresionAritmetica(Expresion):
    def __init__(self, exp1, exp2, operador):
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador + "[ label =\"" + self.operador + "\" ];"
        nodo += "\n" + identificador + " -> " + str(hash(self.exp1)) + ";"
        nodo += "\n" + identificador + " -> " + str(hash(self.exp2)) + ";\n"

        nodo += self.exp1.dibujar()
        nodo += self.exp2.dibujar()

        return nodo

    def valor(self, ts):
        if self.operador == '+':
            # count(*) as a; a + 5
            return self.exp1.valor(ts) + self.exp2.valor(ts)

# Clase de expresión negativa


class ExpresionNegativa(Expresion):
    def __init__(self, exp):
        self.exp = exp

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador + "[ label =\"-\" ];"
        nodo += "\n" + identificador + " -> " + str(hash(self.exp)) + ";\n"

        nodo += self.exp.dibujar()

        return nodo


class ExpresionPositiva(Expresion):
    def __init__(self, exp):
        self.exp = exp

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador + "[ label =\"+\" ];"
        nodo += "\n" + identificador + " -> " + str(hash(self.exp)) + ";\n"

        nodo += self.exp.dibujar()

        return nodo

# Clase de expresión numero


class ExpresionNumero(Expresion):
    def __init__(self, val):
        self.val = val

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador + "[ label =\"" + str(self.val) + "\" ];\n"

        return nodo

# ------FUNCIONES NUMERICAS (EXPRESIONES NUMERICAS)


class FuncionNumerica(Expresion):
    def __init__(self, funcion, parametro1=None, parametro2=None):
        self.parametro1 = parametro1
        self.parametro2 = parametro2
        self.funcion = funcion

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador + "[ label =\"" + self.funcion + "\" ];"

        # Retorno
        if self.parametro1:
            nodo += "\n" + identificador + " -> " + \
                str(hash(self.parametro1)) + ";"
            nodo += self.parametro1.dibujar()
        if self.parametro2:
            nodo += "\n" + identificador + " -> " + \
                str(hash(self.parametro2)) + ";"
            nodo += self.parametro2.dibujar()

        return nodo

# ------EXPRESIONES LOGICAS
# Expresión binaria de comparacion
class ExpresionComparacion(Expresion):
    def __init__(self, exp1, exp2, operador):
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador + "[ label =\"" + self.operador + "\" ];"
        nodo += "\n" + identificador + " -> " + str(hash(self.exp1)) + ";"
        nodo += "\n" + identificador + " -> " + str(hash(self.exp2)) + ";\n"

        nodo += self.exp1.dibujar()
        nodo += self.exp2.dibujar()

        return nodo

class ExpresionLogica(Expresion):
    def __init__(self, exp1, exp2, operador):
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador + "[ label =\"" + self.operador + "\" ];"
        nodo += "\n" + identificador + " -> " + str(hash(self.exp1)) + ";"
        nodo += "\n" + identificador + " -> " + str(hash(self.exp2)) + ";\n"

        nodo += self.exp1.dibujar()
        nodo += self.exp2.dibujar()

        return nodo

# Expresion negada
class ExpresionNegada(Expresion):
    def __init__(self, exp):
        self.exp = exp

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador + "[ label =\"NOT\" ];"
        nodo += "\n" + identificador + " -> " + str(hash(self.exp)) + ";\n"

        nodo += self.exp.dibujar()

        return nodo

# Expresión booleana (Valor puro)
class ExpresionBooleano(Expresion):
    def __init__(self, val):
        self.val = val

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador + "[ label =\"" + str(self.val) + "\" ];\n"

        return nodo

# Expresión Between: Contempla tanto al Between como al Between Symmetric, asi como las versiones negadas


class ExpresionBetween(Expresion):
    def __init__(self, evaluado, limiteInferior, limiteSuperior, invertido=False, simetria=False):
        self.evaluado = evaluado
        self.limiteInferior = limiteInferior
        self.limiteSuperior = limiteSuperior
        self.invertido = invertido
        self.simetria = simetria

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador

        if self.simetria:
            if self.invertido:
                nodo += "[ label = \"NOT BETWEEN SYMMETRIC\" ];"
            else:
                nodo += "[ label = \"BETWEEN SYMMETRIC\" ];"
        else:
            if self.invertido:
                nodo += "[ label = \"NOT BETWEEN\" ];"
            else:
                nodo += "[ label = \"BETWEEN\" ];"

        nodo += "\nAND" + identificador + "[ label = \"AND\" ];"
        nodo += "\n" + identificador + " -> AND" + identificador + ";"

        nodo += "\n" + identificador + " -> " + str(hash(self.evaluado)) + ";"
        nodo += self.evaluado.dibujar()

        nodo += "\nAND" + identificador + " -> " + \
            str(hash(self.limiteInferior)) + ";"
        nodo += self.limiteInferior.dibujar()

        nodo += "\nAND" + identificador + " -> " + \
            str(hash(self.limiteSuperior)) + ";"
        nodo += self.limiteSuperior.dibujar()

        return nodo

# Expresión is: Contempla todas su variaciones
class ExpresionIs(Expresion):
    def __init__(self, condicion, tipo, invertido=False, subcondicion=None):
        self.condicion = condicion
        self.invertido = invertido
        self.subcondicion = subcondicion

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador

        return nodo

# ------EXPRESIONES DE CADENAS
class ExpresionCadena(Expresion):
    def __init__(self, valor):
        self.val = valor

    def dibujar(self):
        identificador = str(hash(self))
        temp = str(self.val)

        temp = temp.replace("\"", "")
        temp = temp.replace("\'", "")

        nodo = "\n" + identificador + "[ label =\"" + temp + "\" ];\n"

        return nodo


class FuncionCadena(Expresion):
    def __init__(self, funcion, parametro1, parametro2=None, parametro3=None):
        self.funcion = funcion
        self.parametro1 = parametro1
        self.parametro2 = parametro2
        self.parametro3 = parametro3

    def dibujar(self):
        identificador = str(hash(self))

        nodo = "\n" + identificador + "[ label = \"" + self.funcion + "\" ];"
        nodo += "\n" + identificador + " -> " + \
            str(hash(self.parametro1)) + ";"
        nodo += "\n" + str(hash(self.parametro1)) + \
            "[label = \"" + self.parametro1 + "\"];"

        if self.parametro2:
            if isinstance(self.parametro2, str):
                nodo += "\n" + identificador + " -> " + \
                    str(hash(self.parametro2)) + ";"
                nodo += "\n" + str(hash(self.parametro2)) + \
                    "[label = \"" + self.parametro2 + "\"];"
            else:
                nodo += "\n" + identificador + " -> " + \
                    str(hash(self.parametro2)) + ";"
                nodo += "\n" + str(hash(self.parametro2)) + \
                    "[label = \"" + str(self.parametro2) + "\"];"

        return nodo