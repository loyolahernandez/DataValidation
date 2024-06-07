#####################################################################################################################
#####################################################################################################################
# App para leer un texto y, a partir de una palabra semilla y un entero n, predecir las n palabras sucesoras de la semilla
# @Ignacio Loyola Hernández
#####################################################################################################################
#####################################################################################################################

from collections import defaultdict, Counter

# Lectura de entradas
#####################################################################################################################
#####################################################################################################################
# leer el texto
def leer_corpus():
    corpus = input("Introduce el texto del corpus: ")
    return corpus

# leer la palabra semilla
def leer_semilla(corpus):
    while True:
        semilla = input("Introduce la palabra semilla: ")
        if semilla in corpus.split():
            return semilla
        else:
            print("Palabra semilla no encontrada en el corpus. Inténtalo de nuevo.")

# leer el entero con la cantidad de palabras a predecir luego de la semilla. No puede ser mayor al 10% del cuerpo.
def leer_n(corpus):
    palabras = corpus.split()
    max_n = int(len(palabras) / 10)
    while True:
        try:
            n = int(input(f"Introduce un número entero positivo N (1 a {max_n}): "))
            if 1 <= n <= max_n:
                return n
            else:
                print(f"Por favor, introduce un número entre 1 y {max_n}.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número válido.")


# Logica de predicción
#####################################################################################################################
#####################################################################################################################

# Separar el texto en palabras
def construir_frecuencias_palabras(corpus):
    palabras = corpus.split()
    frecuencias_palabras = defaultdict(Counter)
    for i in range(len(palabras) - 1):
        frecuencias_palabras[palabras[i]][palabras[i + 1]] += 1
    return frecuencias_palabras

# Prediccion de la siguiente palabra(s)
def predecir_siguiente_palabra(palabra, frecuencias_palabras):
    if palabra in frecuencias_palabras:
        return frecuencias_palabras[palabra].most_common(1)[0][0]
    return None

# Generar frase con n palabras
def generar_frase(semilla, frecuencias_palabras, n):
    frase = [semilla]
    palabra_actual = semilla
    for _ in range(n):
        siguiente_palabra = predecir_siguiente_palabra(palabra_actual, frecuencias_palabras)
        if siguiente_palabra:
            frase.append(siguiente_palabra)
            palabra_actual = siguiente_palabra
        else:
            break
    return " ".join(frase)



def main():
    corpus = leer_corpus()
    semilla = leer_semilla(corpus)
    n = leer_n(corpus)
    
    frecuencias_palabras = construir_frecuencias_palabras(corpus)
    frase = generar_frase(semilla, frecuencias_palabras, n-1)
    
    print(f"Frase generada: {frase}")


if __name__ == "__main__":
    main()