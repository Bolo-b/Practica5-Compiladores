noterminales = ["S'","S","P","LS","I","E","C","T"]
terminales = ["(", ")", "defun", "id", "if", "+", "first", "rest", "null", "'", "num", "nil", "t"]
#Clase para almacenar el AST
class Nodo:
    def __init__(self, simbolo, hijos=None):
        self.simbolo = simbolo
        self.hijos = hijos or []


def imprimir_ast(nodo, prefijo="", es_ultimo=True, es_raiz=True):
    if es_raiz:
        print(nodo.simbolo)
        nuevo_prefijo = ""
    else:
        print(prefijo + ("   " if es_ultimo else "   ") + nodo.simbolo)
        nuevo_prefijo = prefijo + ("    " if es_ultimo else "    ")
    for i, h in enumerate(nodo.hijos):
        imprimir_ast(h, nuevo_prefijo, i == len(nodo.hijos) - 1, False)

#Depende de la construccion del lenguaje almacena los datos de forma distinta en los nodos
def construir(n, h):
    # S -> S P
    if n == 1:
        if h[0].simbolo == "programa":
            h[0].hijos.append(h[1])
            return h[0]
        return Nodo("programa", [h[0], h[1]])
    # S -> P | P -> E | E -> T | T -> id/num/nil/t | I -> id
    if n in (2, 4, 15, 7, 18, 19, 20, 21):
        return h[0]
    # P -> ( defun id ( LS ) E )
    if n == 3:
        return Nodo("defun", [h[2], h[4], h[6]])
    # LS -> I LS
    if n == 5:
        return Nodo("( )", [h[0]] + h[1].hijos)
    # LS -> I
    if n == 6:
        return Nodo("( )", [h[0]])
    # E -> ( I E )   llamada a función: id(E)
    if n == 8:
        h[1].hijos.append(h[2])
        return h[1]
    # E -> ( if E E E )
    if n == 9:
        return Nodo("if", [h[2], h[3], h[4]])
    # E -> ( E + E )
    if n == 10:
        return Nodo("+", [h[1], h[3]])
    # E -> ( first E ) | ( rest E ) | ( null E )
    if n in (11, 12, 13):
        return Nodo(h[1].simbolo, [h[2]])
    # E -> ' ( C )
    if n == 14:
        return Nodo("'", h[2].hijos)
    # C -> C T
    if n == 16:
        h[0].hijos.append(h[1])
        return h[0]
    # C -> T
    if n == 17:
        return Nodo("C", [h[0]])
        
def parse(tokens: list):
    tokens = tokens + ["$"]
    pila = [(0, None)] #El segundo parametro guarda el nodo para generar el AST
    i = 0

    while True:
        estado = pila[-1][0]
        token = tokens[i]
        accion = transiciones[estado][simbolos[token]]

        #Si acepta, terminamos
        if accion == "acc":
            return True, pila[-1][1]

        #Cuando solo es un número y esta en no terminales, shift
        if isinstance(accion, int) and accion != 0:
            pila.append((accion, Nodo(token)))
            i += 1

        #Con "rn", reduce
        elif isinstance(accion, str):
            n = int(accion[1:])
            lhs, rhs = producciones[n]
            k = len(rhs)
            #Saca de la pila
            hijos = [nodo for _, nodo in pila[len(pila) - k:]] if k else []
            if k:
                del pila[-k:]
            #Contruimos el ASA
            nodo = construir(n, hijos)
            #Con el nuevo estado transicionado despues de eleminiar
            #Realizamos el movimiento
            destino = transiciones[pila[-1][0]][simbolos[lhs]]
            if destino == 0:
                print(f"Error: goto inválido en estado {pila[-1][0]} con {lhs}")
                return False, None
            pila.append((destino, nodo))

        #Por default, la accion es 0 y es error
        else:
            print(f"Syntax Error: token '{token}' (posición {i}), estado {estado}")
            return False, None
    


if __name__ == "__main__":
    simbolos = {"(":0,")":1,"'":2,"defun":3,"if":4,"+":5,"first":6,"rest":7,"null":8,"id":9,"num":10,"nil":11,"t":12,"$":13,
                "S":14,"P":15,"LS":16,"I":17,"E":18,"C":19,"T":20}

    transiciones = [
    [3,0,5,0,0,0,0,0,0,7,8,9,10,0,1,2,0,0,4,0,6],
    [3,0,5,0,0,0,0,0,0,7,8,9,10,"acc",0,11,0,0,4,0,6],
    ["r2","r2","r2","r2","r2","r2","r2","r2","r2","r2","r2","r2","r2","r2",0,0,0,0,0,0,0],
    [20,0,5,12,15,0,17,18,19,14,8,9,10,0,0,0,0,13,16,0,6],
    ["r4","r4","r4","r4","r4","r4","r4","r4","r4","r4","r4","r4","r4","r4",0,0,0,0,0,0,0],
    [21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ["r15","r15","r15","r15","r15","r15","r15","r15","r15","r15","r15","r15","r15","r15",0,0,0,0,0,0,0],
    ["r18","r18","r18","r18","r18","r18","r18","r18","r18","r18","r18","r18","r18","r18",0,0,0,0,0,0,0],
    ["r19","r19","r19","r19","r19","r19","r19","r19","r19","r19","r19","r19","r19","r19",0,0,0,0,0,0,0],
    ["r20","r20","r20","r20","r20","r20","r20","r20","r20","r20","r20","r20","r20","r20",0,0,0,0,0,0,0],
    ["r21","r21","r21","r21","r21","r21","r21","r21","r21","r21","r21","r21","r21","r21",0,0,0,0,0,0,0],
    ["r1","r1","r1","r1","r1","r1","r1","r1","r1","r1","r1","r1","r1","r1",0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,22,0,0,0,0,0,0,0,0,0,0,0],
    [20,0,5,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,23,0,6],
    ["r7","r7","r7","r7","r7","r7","r7","r7","r7","r7","r7","r7","r7","r7",0,0,0,0,0,0,0],
    [20,0,5,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,24,0,6],
    [0,0,0,0,0,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [20,0,5,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,26,0,6],
    [20,0,5,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,27,0,6],
    [20,0,5,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,28,0,6],
    [20,0,5,0,15,0,17,18,19,14,8,9,10,0,0,0,0,13,16,0,6],
    [0,0,0,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,0,29,30],
    [31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [20,0,5,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,33,0,6],
    [20,0,5,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,34,0,6],
    [0,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,36,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,37,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,38,0,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,0,0,39],
    ["r17","r17","r17","r17","r17","r17","r17","r17","r17","r17","r17","r17","r17","r17",0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,42,0,0,0,0,0,0,40,41,0,0,0],
    ["r8","r8","r8","r8","r8","r8","r8","r8","r8","r8","r8","r8","r8","r8",0,0,0,0,0,0,0],
    [20,0,5,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,43,0,6],
    [0,44,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ["r11","r11","r11","r11","r11","r11","r11","r11","r11","r11","r11","r11","r11","r11",0,0,0,0,0,0,0],
    ["r12","r12","r12","r12","r12","r12","r12","r12","r12","r12","r12","r12","r12","r12",0,0,0,0,0,0,0],
    ["r13","r13","r13","r13","r13","r13","r13","r13","r13","r13","r13","r13","r13","r13",0,0,0,0,0,0,0],
    ["r14","r14","r14","r14","r14","r14","r14","r14","r14","r14","r14","r14","r14","r14",0,0,0,0,0,0,0],
    ["r16","r16","r16","r16","r16","r16","r16","r16","r16","r16","r16","r16","r16","r16",0,0,0,0,0,0,0],
    [0,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,"r6",0,0,0,0,0,0,0,42,0,0,0,0,0,0,46,41,0,0,0],
    ["r7","r7","r7","r7","r7","r7","r7","r7","r7","r7","r7","r7","r7","r7",0,0,0,0,0,0,0],
    [0,47,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ["r10","r10","r10","r10","r10","r10","r10","r10","r10","r10","r10","r10","r10","r10",0,0,0,0,0,0,0],
    [20,0,5,0,0,0,0,0,0,7,8,9,10,0,0,0,0,0,48,0,6],
    ["r5","r5","r5","r5","r5","r5","r5","r5","r5","r5","r5","r5","r5","r5",0,0,0,0,0,0,0],
    ["r9","r9","r9","r9","r9","r9","r9","r9","r9","r9","r9","r9","r9","r9",0,0,0,0,0,0,0],
    [0,49,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ["r3","r3","r3","r3","r3","r3","r3","r3","r3","r3","r3","r3","r3","r3",0,0,0,0,0,0,0]]

    producciones = {
    1:  ("S",  ["S", "P"]),
    2:  ("S",  ["P"]),
    3:  ("P",  ["(", "defun", "id", "(", "LS", ")", "E", ")"]),
    4:  ("P",  ["E"]),
    5:  ("LS", ["I", "LS"]),
    6:  ("LS", ["I"]),
    7:  ("I",  ["id"]),
    8:  ("E",  ["(", "I", "E", ")"]),
    9:  ("E",  ["(", "if", "E", "E", "E", ")"]),
    10: ("E",  ["(", "E", "+", "E", ")"]),
    11: ("E",  ["(", "first", "E", ")"]),
    12: ("E",  ["(", "rest", "E", ")"]),
    13: ("E",  ["(", "null", "E", ")"]),
    14: ("E",  ["'", "(", "C", ")"]),
    15: ("E",  ["T"]),
    16: ("C",  ["C", "T"]),
    17: ("C",  ["T"]),
    18: ("T",  ["id"]),
    19: ("T",  ["num"]),
    20: ("T",  ["nil"]),
    21: ("T",  ["t"]),
    }

    prueba1 = ["(","num","+","(","num","+","num",")",")"]
    prueba2 = ["(","if","nil","num","num",")"]
    prueba3 = ["(", "first", "'", "(", "num", ")", ")"]
    prueba4 = ["(","defun","id","(","id",")","num",")"]
    prueba5 = ["(","null","num",")"]
    prueba_error1 = ["(","+","num",")"] #Falta izquierda de la suma
    prueba_error2 = ["(","if","t","num",")"] #Falta rama else del if
    prueba_error3 = ["(", "first", "(", "num", ")", ")"] #Falta ' a la lista y un terminal no va entre parentesis
    prueba_error4 = ["(","defun","(","id",")","num",")"] #Funcion sin nombre
    prueba_error5 = ["(","null","num"] #Parentesis desbalanceados


    result1, asa1 = parse(prueba1)
    result2, asa2 = parse(prueba2)
    result3, asa3 = parse(prueba3)
    result4, asa4 = parse(prueba4)
    result5, asa5 = parse(prueba5)

    print(result1)
    imprimir_ast(asa1)
    print("\n"+str(result2))
    imprimir_ast(asa2)
    print("\n"+str(result3))
    imprimir_ast(asa3)
    print("\n"+str(result4))
    imprimir_ast(asa4)
    print("\n"+str(result5))
    imprimir_ast(asa5)

    print("Programas con error: ")
    print(parse(prueba_error1))
    print(parse(prueba_error2))
    print(parse(prueba_error3))
    print(parse(prueba_error4))
    print(parse(prueba_error5))
