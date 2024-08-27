def limpa_texto(cadeia):
    """
    cad. carateres → cad. carateres
    recebe uma cadeia e substitui os carateres brancos por espacos
    """

    tuplo_car = ('\t', '\n', '\v', '\f', '\r', ' ')
    for i in range(len(cadeia)):
        if cadeia[i] in tuplo_car:
            cadeia = cadeia[:i] + ' ' + cadeia[i+1:]
            #o carater branco e' substituido pelo espaco

    i = 0
    while i < len(cadeia) - 1: 
        if cadeia[i] == ' ': 
            if cadeia[i+1] == ' ': 
                #se o carater a seguir a um espaco tambem for um espaco 
                cadeia = cadeia[:i+1] + cadeia[i+2:] 
                #elimina-se a repeticao do espaco
                i = i - 1 #para voltar 'a posicao anterior
        i += 1
    
    cadeia = cadeia.strip()

    return cadeia

def corta_texto(cadeia, largura):
    """
    cad. carateres x inteiro → cad. carateres x cad. carateres
    recebe uma cadeia e um valor da largura e divide a cadeia em duas: 
    a primeira com um comprimento da largura e a segunda com a restante cadeia
    """

    cadeia = cadeia.strip()
    if len(cadeia) <= largura:
        return cadeia, '' #retorna a primeira subcadeia e a segunda vazia

    while cadeia[largura] != ' ':
        largura = largura - 1 
        #o valor da largura vai diminuindo ate' encontrar um espaco
        if largura == 0:
            return '', cadeia 
            #retorna a primeira subcadeia vazia e o resto fica na segunda 

    subcadeia_1 = cadeia[:largura]
    subcadeia_2 = cadeia[largura + 1:]

    subcadeia_1 = subcadeia_1.strip()
    subcadeia_2 = subcadeia_2.strip()

    return subcadeia_1, subcadeia_2

def insere_espacos(cadeia, largura):
    """
    cad. carateres x inteiro → cad. carateres
    recebe uma cadeia e um valor da largura e insere espacos 
    ate' a cadeia ter o comprimento da largura
    """

    largura_atual = 0
    if ' ' in cadeia: #se a cadeia de entrada conter duas ou mais palavras
        lista_cadeia = cadeia.split()
        for i in lista_cadeia:
            largura_atual += len(i) 
            #calcular a soma do comprimento das palavras sem espacos entre elas
        while largura_atual < largura:
            for i in range(len(lista_cadeia) - 1): 
                #len - 1 para nao ser inserido o espaco na ultima palavra
                lista_cadeia[i] = lista_cadeia[i] + ' '
                largura_atual += 1
                if largura_atual == largura: 
                    break
        cadeia = ''
        for palavra in lista_cadeia:
            cadeia = cadeia + palavra 
            #concatenar as palavras com os espacos numa frase
    
    else: #se a cadeia de entrada conter apenas uma palavra
        cadeia = cadeia + ' ' * (largura - len(cadeia)) 

    return cadeia

def justifica_texto(cadeia, largura):
    """
    cad. carateres x inteiro → tuplo
    recebe uma cadeia e um valor da largura e devolve a cadeia 
    justicada com a determinada largura
    """

    if not (isinstance(cadeia, str) and isinstance(largura, int) and \
        len(cadeia) > 0 and largura > 0):
        raise ValueError("justifica_texto: argumentos invalidos")

    cadeia = limpa_texto(cadeia)
    lista_cadeia = cadeia.split()
    for i in lista_cadeia:
        if len(i) > largura:
            raise ValueError("justifica_texto: argumentos invalidos") 

    linhas = ()
    while len(cadeia) > largura:
        t = corta_texto(cadeia, largura)
        linha = t[0]
        cadeia = t[1]
        linhas = linhas + (linha,)

    if cadeia != '': #para adicionar a ultima linha na cadeia
        cadeia = cadeia + ' ' * (largura - len(cadeia)) 
        #porque e' a ultima linha

    cadeia_justificada = ()
    for linha in linhas[:]:
        linha = insere_espacos(linha, largura)
        cadeia_justificada += (linha,)
    
    cadeia_justificada += (cadeia,)

    return cadeia_justificada

def calcula_quocientes(dicionario, num_deputados):
    """
    dicionario x inteiro → dicionario
    recebe os votos de cada partido num circulo eleitoral e
    devolve os quocientes calculados com o metodo de Hondt
    """

    partidos = dicionario.keys()
    novo_dicionario = dicionario.fromkeys(partidos) 
    quocientes = []
    for partido in dicionario:
        for divisor in range(1,num_deputados + 1):
            quocientes += [dicionario[partido] / divisor]
        novo_dicionario[partido] = quocientes 
        quocientes = []

    return novo_dicionario

def atribui_mandatos(votos, num_deputados):
    """
    dicionario x inteiro → lista
    recebe os votos de um partido num circulo eleitoral e
    devolve os mandatos atribuidos aos partidos
    """

    lista_deputados = []
    quocientes = calcula_quocientes(votos, num_deputados)
    
    while len(lista_deputados) < num_deputados:
        maximo = 0
        for partido in quocientes:
            for i in range(len((quocientes[partido]))):
                if quocientes[partido][i] > maximo:
                    maximo = quocientes[partido][i]
                    partido_maximo = partido
                    posicao_maximo = i

        for partido in quocientes:
            for i in range(len((quocientes[partido]))):
                if quocientes[partido][i] == maximo: 
                    #no caso de existirem dois ou 
                    #mais partidos com igual quociente
                    if votos[partido] < votos[partido_maximo]:
                        partido_maximo = partido
                        posicao_maximo = i

        lista_deputados += [partido_maximo]
        del(quocientes[partido_maximo][posicao_maximo])

    return lista_deputados

def obtem_partidos(info):
    """
    dicionario → lista
    recebe a informacao sobre as eleicoes e devolve   
    os partidos que participaram nas eleicoes
    """

    lista_partidos = []
    for circulo_eleitoral in info:
        for partido in info[circulo_eleitoral]['votos']:
            lista_partidos += [partido]

    lista_partidos = sorted(lista_partidos)

    for partido in range(len(lista_partidos)-1,-1,-1): 
        #remover partidos repetidos
        if lista_partidos[partido] in lista_partidos[0:partido]:
            del(lista_partidos[partido])
     
    return lista_partidos

def obtem_resultado_eleicoes(info):
    """
    dicionario → lista
    recebe a informacao sobre as eleicoes e devolve os resultados das eleicoes, 
    com os partidos e o respetivo numero de deputados e numero de votos
    """

    if not (isinstance(info,dict) and len(info) > 0):
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")

    for circulo_eleitoral in info:
        if not (isinstance(circulo_eleitoral,str) and \
            'deputados' in info[circulo_eleitoral] and \
            'votos' in info[circulo_eleitoral] and \
            isinstance(info[circulo_eleitoral]['deputados'],int) and \
            info[circulo_eleitoral]['deputados'] > 0 and \
            isinstance(info[circulo_eleitoral]['votos'],dict) and \
            len(info[circulo_eleitoral]['votos']) > 0):
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")

        for chave in info[circulo_eleitoral]:
            if chave not in ('votos', 'deputados'):
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")

        for partido in info[circulo_eleitoral]['votos']:
            if not (isinstance(partido,str) and \
                isinstance(info[circulo_eleitoral]['votos'][partido],int)):
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")

    lista_mandatos = []

    for circulo_eleitoral in info:
        lista_mandatos += atribui_mandatos(info[circulo_eleitoral]['votos'],
                            info[circulo_eleitoral]['deputados'])

    lista_partidos = obtem_partidos(info)
    
    res_eleicoes = {}

    #vou criar um dicionario em que cada chave e' o partido e cada valor e' 
    #uma lista com o numero de deputados e numero de votos 

    for partido in lista_mandatos: 
        #para ir calculando o numero de deputados em cada partido
        if partido not in res_eleicoes:   
            res_eleicoes[partido] = [1,0]
        else:
            res_eleicoes[partido][0] += 1
    
    for partido in lista_partidos: 
        #no caso de o numero de deputados do partido for zero
        if partido not in res_eleicoes:
            res_eleicoes[partido] = [0,0]

    for circulo_eleitoral in info:
        for partido in info[circulo_eleitoral]['votos']:
            #para ir calculando o numero de votos de cada partido
            res_eleicoes[partido][1] += info[circulo_eleitoral]['votos'][partido]

    lista_eleicoes = []
    for partido in res_eleicoes:
        lista_eleicoes += [(partido,res_eleicoes[partido][0],
                            res_eleicoes[partido][1])]

    lista_eleicoes = sorted(lista_eleicoes, key = lambda x : x[1:], 
                            reverse = True) 
    #ordenar por ordem descendente de acordo com o numero de deputados
    #obtidos e, em caso de empate, de acordo com o numero de votos

    return lista_eleicoes

def produto_interno(tuplo1, tuplo2):
    """
    tuplo x tuplo → real
    recebe dois vetores e efetua o produto interno dos mesmos
    """

    soma = 0.0
    for i in range(len(tuplo1)):
        produto = tuplo1[i] * tuplo2[i]
        soma += produto

    return soma 

def verifica_convergencia(matriz, constantes, solucao, precisao):
    """
    tuplo x tuplo x tuplo x real → booleano
    recebe uma matriz quadrada, um vetor de constantes, a solucao atual 
    e a precisao pretendida e verifica se o valor absoluto do erro de 
    todas as equacoes e' inferior 'a precisao
    """

    for i in range(len(matriz)):
        f_i = produto_interno(matriz[i], solucao)
        erro = f_i - constantes[i]

        if abs(erro) >= precisao:
            return False

    return True

def retira_zeros_diagonal(matriz, constantes):
    """
    tuplo x tuplo → tuplo x tuplo
    recebe uma matriz quadrada e um vetor de constantes e devolve 
    uma nova matriz com as linhas reordenadas de modo a nao 
    existirem valores 0 na diagonal
    """

    def troca_linha_aux(matriz,constantes,i,j):
        if i < j: #troca a linha i com a linha j
            i,j = j,i
        matriz = matriz[:j] + (matriz[i],) + matriz[j+1:i] + \
                (matriz[j],) + matriz[i+1:]
        constantes = constantes[:j] + (constantes[i],) + constantes[j+1:i] \
                    + (constantes[j],) + constantes[i+1:]
        return matriz, constantes

    for i in range(len(matriz)):
        if matriz[i][i] == 0: #se o elemento da diagonal for zero
            for j in range(len(matriz)):
                if matriz[i][j] != 0 and matriz[j][i] != 0: 
                    #para que a troca nao coloque um zero na diagonal
                    matriz, constantes = troca_linha_aux(matriz,constantes,i,j)
                    break

    return matriz, constantes

def eh_diagonal_dominante(matriz):
    """
    tuplo → booleano
    recebe uma matriz quadrada e verifica se e' uma matriz diagonalmente 
    dominante (valor absoluto do valor da diagonal ser maior ou igual 'a 
    soma dos restantes valores absolutos da linha)
    """ 
    
    soma = 0
    for i in range(len(matriz)):
        for el in range(len(matriz[i])):
            soma += abs(matriz[i][el]) 
            #soma do valor absoluto de todos os elementos da linha
        if abs(matriz[i][i]) < soma - abs(matriz[i][i]):
            return False
        soma = 0
    return True

def resolve_sistema(matriz, constantes, precisao):
    """
    tuplo x tuplo x real → tuplo
    recebe uma matriz quadrada, um vetor de constantes e a precisao pretendida 
    e devolve a solucao do sistema de equacoes aplicando o metodo de Jacobi 
    """

    if not (isinstance(matriz,tuple) and isinstance(constantes,tuple) and \
        isinstance(precisao,float) and precisao > 0):
        raise ValueError("resolve_sistema: argumentos invalidos")

    for linha in matriz:
        if not (isinstance(linha,tuple) and len(matriz) == len(linha) \
            and len(linha) == len(constantes)):
            raise ValueError("resolve_sistema: argumentos invalidos")
        for numero in linha:
            if not (isinstance(numero,(int,float))):
                raise ValueError("resolve_sistema: argumentos invalidos")

    for numero in constantes:
        if not (isinstance(numero,(int,float))):
                raise ValueError("resolve_sistema: argumentos invalidos")

    matriz,constantes = retira_zeros_diagonal(matriz,constantes) 
    #reordena as linhas da matriz de modo a nao ter zeros na diagonal

    if not eh_diagonal_dominante(matriz):
        raise ValueError("resolve_sistema: matriz nao diagonal dominante")

    solucao = (0,) * len(matriz)
    solucao_nova = ()

    while not verifica_convergencia(matriz, constantes, solucao, precisao):
        #enquanto nao se atinge a convergencia vai-se calculando novas solucoes
        i = 0
        while i < len(solucao):
            solucao_nova += (solucao[i] + (constantes[i] - produto_interno(matriz[i], solucao)) \
                            / matriz[i][i],)
            i += 1
        solucao = solucao_nova
        solucao_nova = ()

    return solucao