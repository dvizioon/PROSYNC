import sys
sys.path.append(".")

# Modules/variation.py

def openVariante(arquivo, nome_bloco):
    """
    Lê as variáveis de um bloco específico de um arquivo.
    
    Parâmetros:
    arquivo (str): Caminho do arquivo a ser lido.
    nome_bloco (str): Nome do bloco a ser lido.
    
    Retorna:
    list: Uma lista de strings com as variáveis do bloco especificado.
    """
    variaveis = []
    bloco_encontrado = False

    with open(arquivo, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            if line.startswith("->"):
                if bloco_encontrado:
                    break
                if line[2:].strip() == nome_bloco:
                    bloco_encontrado = True
                continue

            if bloco_encontrado and line.startswith("-"):
                variaveis.append(line[2:])
    
    return variaveis

def openVariante_index(arquivo, nome_bloco, indice):
    """
    Lê uma variável específica de um bloco de um arquivo.
    
    Parâmetros:
    arquivo (str): Caminho do arquivo a ser lido.
    nome_bloco (str): Nome do bloco de onde se deseja ler a variável.
    indice (int): Índice da variável a ser retornada.
    
    Retorna:
    str: A variável no índice especificado ou None se o bloco ou índice forem inválidos.
    """
    variaveis = openVariante(arquivo, nome_bloco)
    if indice < 0 or indice >= len(variaveis):
        return None
    return variaveis[indice]
