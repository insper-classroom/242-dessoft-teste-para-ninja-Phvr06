from random import randint, shuffle

def gera_numeros() -> list:
    numeros = []
    soma = 0
    for i in range(2):
        sorteado = randint(1, 30)
        while sorteado in numeros:
            sorteado = randint(1, 30)
        numeros.append(sorteado)
        soma += sorteado
    
    sorteado = randint(min(numeros), max(numeros))
    while sorteado in numeros:
        sorteado = randint(min(numeros), max(numeros))
        
    numeros.append(sorteado)
    
    shuffle(numeros)
    
    numeros.append(soma)
    
    return numeros