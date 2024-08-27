def cria_gerador(b, s):
    """
    int x int → gerador
    recebe um numero de bits e um estado e devolve o gerador
    """

    if not (isinstance(b, int) and isinstance(s, int) and (b == 32 or b == 64)\
        and s > 0 and s < 2 ** b):
        raise ValueError("cria_gerador: argumentos invalidos")

    return {'bits': b, 'estado': s}
    #representacao interna gerador -> dicionario

def cria_copia_gerador(g):
    """
    gerador → gerador
    recebe um gerador e devolve uma copia nova do gerador
    """

    return g.copy()

def obtem_estado(g):
    """
    gerador → int
    devolve o estado atual do gerador g sem o alterar
    """

    return g['estado']

def define_estado(g, s):
    """
    gerador x int → int
    define o novo valor do estado do gerador g como sendo s, e devolve s
    """

    g['estado'] = s

    return s

def atualiza_estado(g):
    """
    gerador → int
    atualiza o estado do gerador g de acordo com o algoritmo xorshift
    de geracao de numeros pseudoaleatorios, e devolve-o
    """

    if g['bits'] == 32:
        g['estado'] ^= ( g['estado'] << 13 ) & 0xFFFFFFFF
        g['estado'] ^= ( g['estado'] >> 17 ) & 0xFFFFFFFF
        g['estado'] ^= ( g['estado'] << 5 ) & 0xFFFFFFFF

    elif g['bits'] == 64:
        g['estado'] ^= ( g['estado'] << 13 ) & 0xFFFFFFFFFFFFFFFF
        g['estado'] ^= ( g['estado'] >> 7 ) & 0xFFFFFFFFFFFFFFFF
        g['estado'] ^= ( g['estado'] << 17 ) & 0xFFFFFFFFFFFFFFFF

    return g['estado']

def eh_gerador(arg):
    """
    universal → booleano
    vefifica se o argumento e' um gerador
    """

    return isinstance(arg, dict) and len(arg) == 2 and 'bits' in arg and \
        'estado' in arg and isinstance(arg['bits'], int) and \
        isinstance(arg['estado'], int) and (arg['bits'] == 32 or \
        arg['bits'] == 64) and arg['estado'] > 0 and \
        arg['estado'] < 2 ** arg['bits']

def geradores_iguais(g1, g2):
    """
    gerador x gerador → booleano
    verifica se os argumentos sao ambos geradores e se sao iguais
    """

    return eh_gerador(g1) and eh_gerador(g2) and g1['bits'] == g2['bits'] and \
        g1['estado'] == g2['estado']

def gerador_para_str(g):
    """
    gerador → str
    devolve a cadeia de carateres que representa o seu argumento
    """

    return 'xorshift' + str(g['bits']) + '(s=' + str(g['estado']) + ')'

def gera_numero_aleatorio(g, n):
    """
    gerador x int → int
    atualiza o estado do gerador g e devolve  
    um numero aleatorio no intervalo [1, n]
    """

    atualiza_estado(g)

    return 1 + obtem_estado(g) % n

def gera_carater_aleatorio(g, c):
    """
    gerador x str → str
    atualiza o estado do gerador g e devolve um carater aleatorio
    no intervalo entre 'A' e o carater maiusculo c
    """

    atualiza_estado(g)

    return chr(ord('A') + obtem_estado(g) % (ord(c) - ord('A') + 1))

def cria_coordenada(col, lin):
    """
    str x int → coordenada
    recebe os valores correspondentes 'a coluna e 'a linha
    e devolve a coordenada correspondente
    """

    if not (isinstance(col, str) and isinstance(lin, int) and \
        len(col) == 1 and 'A' <= col <= 'Z' and 1 <= lin <= 99):
        raise ValueError("cria_coordenada: argumentos invalidos")
    
    return col, lin
    #representacao interna coordenada -> tuplo

def obtem_coluna(c):
    """
    coordenada → str
    devolve a coluna da coordenada
    """

    return c[0]

def obtem_linha(c):
    """
    coordenada → int
    devolve a linha da coordenada
    """

    return c[1]

def eh_coordenada(arg):
    """
    universal → booleano
    vefifica se o argumento e' um coordenada
    """

    return isinstance(arg, tuple) and len(arg) == 2 and \
        isinstance(arg[0], str) and isinstance(arg[1], int) and \
        len(arg[0]) == 1 and 'A' <= arg[0] <= 'Z' and 1 <= arg[1] <= 99

def coordenadas_iguais(c1, c2):
    """
    coordenada x coordenada → booleano
    verifica se os argumentos sao coordenadas e se sao iguais
    """

    return eh_coordenada(c1) and eh_coordenada(c2) and \
        obtem_coluna(c1) == obtem_coluna(c2) and \
        obtem_linha(c1) == obtem_linha(c2) 

def coordenada_para_str(c):
    """
    coordenada → str
    devolve a cadeia de carateres que representa o seu argumento
    """

    if obtem_linha(c) < 10:
        return obtem_coluna(c) + '0' + str(obtem_linha(c)) 
    else:
        return obtem_coluna(c) + str(obtem_linha(c))

def str_para_coordenada(s):
    """
    str → coordenada
    devolve a coordenada reapresentada pelo seu argumento
    """

    if not len(s) == 3:
        raise ValueError("str_para_coordenada: argumentos invalidos")

    if s[1] == '0': #se a linha for menor que 10
        c = cria_coordenada(s[0], int(s[2])) 
    else:
        c = cria_coordenada(s[0], int(s[1:]))

    return c

def obtem_coordenadas_vizinhas(c):
    """
    coordenada → tuplo
    devolve as coordenadas vizinhas 'a coordenada c
    """

    coordenadas_vizinhas = ()

    #posicoes em relacao 'a coordenada c, em sentido dos ponteiros
    #do relogio a contar da posicao 'a esquerda de cima
    posicoes = [(-1, -1), (0, -1), (1, -1), (1, 0), \
                (1, 1), (0, 1), (-1, 1), (-1, 0)]

    #filtram-se as posicoes que nao existem:
    #se a coluna for a A ou Z filtram-se as posicoes que se encontram
    #'a esquerda ou 'a direita, respetivamente;
    #se a linha for a 1 ou a 99, filtram-se as posicoes que se encontram
    #em cima ou em baixo, respetivamente.

    if obtem_coluna(c) == 'A':
        posicoes = list(filter(lambda x: x[0] != -1, posicoes))
    if obtem_coluna(c) == 'Z':
        posicoes = list(filter(lambda x: x[0] != 1, posicoes))
    if obtem_linha(c) == 1:
        posicoes = list(filter(lambda x: x[1] != -1, posicoes))
    if obtem_linha(c) == 99:
        posicoes = list(filter(lambda x: x[1] != 1, posicoes))

    for posicao in posicoes:
        coordenadas_vizinhas += (cria_coordenada( \
                                chr(ord(obtem_coluna(c)) + posicao[0]), \
                                obtem_linha(c) + posicao[1]),)

    return coordenadas_vizinhas

def obtem_coordenada_aleatoria(c, g):
    """
    coordenada x gerador → coordenada
    recebe uma coordenada e um gerador, e 
    devolve uma coordenada gerada aleatoriamente
    """

    coordenada_aleatoria = cria_coordenada( \
                        gera_carater_aleatorio(g, obtem_coluna(c)), \
                        gera_numero_aleatorio(g, obtem_linha(c)))

    return coordenada_aleatoria

def cria_parcela():
    """
    {} → parcela
    devolve uma parcela tapada sem mina escondida
    """

    return {'estado': 'tapada', 'mina': False}
    #representacao interna parcela -> dicionario

def cria_copia_parcela(p):
    """
    parcela → parcela
    recebe uma parcela e devolve uma nova copia da parcela
    """
    
    parcela = cria_parcela()

    if eh_parcela_limpa(p):
        limpa_parcela(parcela)
    elif eh_parcela_marcada(p):
        marca_parcela(parcela)
        
    if eh_parcela_minada(p):
        esconde_mina(parcela)

    return parcela

def limpa_parcela(p):
    """
    parcela → parcela
    modifica destrutivamente a parcela modificando o seu 
    estado para limpa, e devolve a propria parcela
    """

    p['estado'] = 'limpa'
    return p

def marca_parcela(p):
    """
    parcela → parcela
    modifica destrutivamente a parcela modificando o seu estado 
    para marcada com uma bandeira, e devolve a propria parcela
    """

    p['estado'] = 'marcada'
    return p

def desmarca_parcela(p):
    """
    parcela → parcela
    modifica destrutivamente a parcela modificando o seu 
    estado para tapada, e devolve a propria parcela
    """

    p['estado'] = 'tapada'
    return p

def esconde_mina(p):
    """
    parcela → parcela
    modifica destrutivamente a parcela escondendo uma
    mina na parcela, e devolve a propria parcela
    """

    p['mina'] = True
    return p

def eh_parcela(arg):
    """
    universal → booleano
    verifica se o argumento e' uma parcela
    """

    return isinstance(arg, dict) and len(arg) == 2 and 'estado' in arg \
        and 'mina' in arg and isinstance(arg['estado'], str) and \
        isinstance(arg['mina'], bool)

def eh_parcela_tapada(p):
    """
    parcela → booleano
    verifica se a parcela se encontra tapada
    """
    return eh_parcela(p) and p['estado'] == 'tapada'

def eh_parcela_marcada(p):
    """
    parcela → booleano
    verifica se a parcela se encontra marcada com uma bandeira
    """
    return eh_parcela(p) and p['estado'] == 'marcada'

def eh_parcela_limpa(p):
    """
    parcela → booleano
    verifica se a parcela se encontra limpa
    """
    return eh_parcela(p) and p['estado'] == 'limpa'

def eh_parcela_minada(p):
    """
    parcela → booleano
    verifica se a parcela esconde uma mina
    """
    return eh_parcela(p) and p['mina'] == True

def parcelas_iguais(p1, p2):
    """
    parcela x parcela → booleano
    verifica se ambos os argumentos sao parcelas e se sao iguais
    """

    return eh_parcela(p1) and eh_parcela(p2) and p1['estado'] == p2['estado'] \
        and p1['mina'] == p2['mina']

def parcela_para_str(p):
    """
    parcela → str
    devolve a cadeia de caracteres que representa a parcela em funcao do seu 
    estado: parcelas tapadas ('#'), parcelas marcadas ('@'), parcelas limpas 
    sem mina ('?') e parcelas limpas com mina ('X')
    """

    if eh_parcela_tapada(p):
        return '#'
    elif eh_parcela_marcada(p):
        return '@'
    elif eh_parcela_limpa and not eh_parcela_minada(p):
        return '?'
    elif eh_parcela_limpa(p) and eh_parcela_minada(p):
        return 'X'

def alterna_bandeira(p):
    """
    parcela → booleano
    recebe uma parcela e modifica-a destrutivamente da seguinte
    forma: desmarca se estiver marcada e marca se estiver tapada 
    """

    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True

    elif eh_parcela_tapada(p):
        marca_parcela(p)
        return True

    return False

def cria_campo(c, l):
    """
    str x int → campo
    recebe a ultima coluna e a ultima linha de um campo de minas, e devolve 
    o campo do tamanho pretendido formado por parcelas tapadas sem minas
    """

    if not (isinstance(c, str) and isinstance(l, int) and len(c) == 1 \
        and 'A' <= c <= 'Z' and 1 <= l <= 99): 
        raise ValueError("cria_campo: argumentos invalidos") 

    campo = {}

    for coluna in range(ord('A'), ord(c) + 1):
        campo[chr(coluna)] = []
        for i in range(l):
            campo[chr(coluna)] += [cria_parcela()]

    return campo
    #representacao interna campo -> dicionario, em que as chaves
    #sao as colunas e os valores de cada chave uma lista cujos 
    #elementos sao parcelas de cada linha

def cria_copia_campo(m):
    """
    campo → campo
    recebe um campo e devolve uma nova copia do campo
    """

    m_copia = cria_campo(obtem_ultima_coluna(m), obtem_ultima_linha(m))

    [esconde_mina(obtem_parcela(m_copia, coordenada)) for \
        coordenada in obtem_coordenadas(m, 'minadas')]
    [marca_parcela(obtem_parcela(m_copia, coordenada)) for \
        coordenada in obtem_coordenadas(m, 'marcadas')]
    [limpa_parcela(obtem_parcela(m_copia, coordenada)) for \
        coordenada in obtem_coordenadas(m, 'limpas')]

    return m_copia

def obtem_ultima_coluna(m):
    """
    campo → str
    devolve a cadeia de caracteres que corresponde
    'a ultima coluna do campo de minas
    """

    return max(m.keys())

def obtem_ultima_linha(m):
    """
    campo → int
    devolve o valor inteiro que corresponde 'a ultima linha do campo de minas
    """

    #tamanho da coluna e' o numero de linhas
    return len(m['A'])
    
def obtem_parcela(m, c):
    """
    campo x coordenada → parcela
    devolve a parcela do campo que se encontra na coordenada c
    """

    return m[obtem_coluna(c)][obtem_linha(c) - 1]
    #coloca-se -1 pelo facto de o indice na lista das parcelas comecar no 0

def obtem_coordenadas(m, s):
    """
    campo x str → tuplo
    devolve as coordenadas do campo cujo estado das parcelas seja igual a s
    """ 

    tuplo = ()

    for linha in range(obtem_ultima_linha(m)):
        for coluna in range(ord(obtem_ultima_coluna(m)) - ord('A') + 1):
            parcela = obtem_parcela(m, cria_coordenada(chr(ord('A') + coluna),\
                                                        linha + 1))
            if (s == 'limpas' and eh_parcela_limpa(parcela)) or \
                (s == 'tapadas' and eh_parcela_tapada(parcela)) or \
                (s == 'marcadas' and eh_parcela_marcada(parcela)) or \
                (s == 'minadas' and eh_parcela_minada(parcela)):

                tuplo += ((cria_coordenada(chr(ord('A') + coluna), linha + 1)),)
        
    return tuplo

def obtem_numero_minas_vizinhas(m, c):
    """
    campo x coordenada → int
    devolve o numero de parcelas vizinhas da parcela 
    na coordenada que escondem uma mina
    """

    contador = 0
    coordenadas_vizinhas = obtem_coordenadas_vizinhas(c)
    parcelas_vizinhas = []

    for coordenada in coordenadas_vizinhas:
        if eh_coordenada_do_campo(m, coordenada):
            parcelas_vizinhas += [obtem_parcela(m, coordenada)]
    
    for parcela in parcelas_vizinhas:
        if eh_parcela_minada(parcela):
            contador += 1

    return contador

def eh_campo(arg):
    """
    universal → booleano
    verifica se o argumento e' um campo
    """

    if not (isinstance(arg, dict) and len(arg) > 0):
        return False
    
    nr_linhas = obtem_ultima_linha(arg)

    for coluna in arg:
        if not (isinstance(coluna, str) and len(coluna) == 1 \
            and 'A' <= coluna <= 'Z' and isinstance(arg[coluna], list) \
            and len(arg[coluna]) == nr_linhas):
            return False

        for i in range(len(arg[coluna])):
            if not eh_parcela(arg[coluna][i]):
                return False
    
    return True

def eh_coordenada_do_campo(m, c):
    """
    campo x coordenada → booleano
    verifica se a coordenada e' uma coordenada valida dentro do campo
    """

    return eh_coordenada(c) and \
        'A' <= obtem_coluna(c) <= obtem_ultima_coluna(m) and \
        1 <= obtem_linha(c) <= obtem_ultima_linha(m)

def campos_iguais(m1, m2):
    """
    campo x campo → booleano
    verifica se ambos os argumentos forem campos e forem iguais
    """

    if not (eh_campo(m1) and eh_campo(m2)) or \
        obtem_ultima_coluna(m1) != obtem_ultima_coluna(m2) or \
        obtem_ultima_linha(m1) != obtem_ultima_linha(m2):

        return False
    
    for coluna in range(ord(obtem_ultima_coluna(m1)) - ord('A') + 1):
        for linha in range(obtem_ultima_linha(m1)):
            parcela_m1 = obtem_parcela(m1, cria_coordenada(chr(ord('A') + \
                                                        coluna), linha + 1))
            parcela_m2 = obtem_parcela(m2, cria_coordenada(chr(ord('A') + \
                                                        coluna), linha + 1))
            if not parcelas_iguais(parcela_m1, parcela_m2):
                return False

    return True

def campo_para_str(m):
    """
    campo → str
    devolve uma cadeia de caracteres que representa o campo de minas 
    """

    cadeia_final = ' ' * 3

    for coluna in range(ord('A'), ord(obtem_ultima_coluna(m)) + 1):
        cadeia_final += chr(coluna)
    #inicialmente coloca-se as colunas do campo

    cadeia_final += '\n' + ' ' * 2 + '+' + '-' * \
                    (ord(obtem_ultima_coluna(m)) - ord('A') + 1) + '+'
    #de seguida coloca-se os limites superiores do campo

    cadeia_parcelas = ''
    
    for linha in range(obtem_ultima_linha(m)):
        for coluna in range(ord(obtem_ultima_coluna(m)) - ord('A') + 1):
            parcela = parcela_para_str(obtem_parcela(m, \
                    cria_coordenada(chr(ord('A') + coluna), linha + 1)))
            if parcela == '?': 
                if obtem_numero_minas_vizinhas(m, cria_coordenada(chr(ord('A')\
                                               + coluna), linha + 1)) > 0:
                    #o simbolo da parcela passa a ser o numero das minas vizinhas

                    parcela = str(obtem_numero_minas_vizinhas(m, \
                                    cria_coordenada(chr(ord('A') + coluna),\
                                                    linha + 1)))
                else:
                    parcela = ' ' 

            cadeia_parcelas += parcela

        cadeia_final += '\n' + \
            coordenada_para_str((cria_coordenada(chr(ord('A') + coluna),\
                                                        linha + 1)))[1:] + \
            '|' + cadeia_parcelas + '|'
            #acrescenta-se o numero da linha: aqui na 'coordenada_para_str'
            #a coluna e' irrelevante, dai a utilizacao de '[1:]'; 
    
        cadeia_parcelas = '' 

    cadeia_final += '\n' + ' ' * 2 + '+' + '-' * \
                    (ord(obtem_ultima_coluna(m)) - ord('A') + 1) + '+'
    #finalmente coloca-se os limites inferiores do campo

    return cadeia_final 

def coloca_minas(m, c, g, n):
    """
    campo x coordenada x gerador x int → campo
    modifica destrutivamente o campo escondendo 
    minas em parcelas dentro do campo
    """
    
    coordenadas_com_minas = [] 

    while n > 0:
        coordenada_aleatoria = obtem_coordenada_aleatoria(\
                                cria_coordenada(obtem_ultima_coluna(m), \
                                obtem_ultima_linha(m)), g)
        if coordenada_aleatoria != c and \
            coordenada_aleatoria not in obtem_coordenadas_vizinhas(c) and \
            coordenada_aleatoria not in coordenadas_com_minas: 
                        
            esconde_mina(obtem_parcela(m, coordenada_aleatoria))
            coordenadas_com_minas += [coordenada_aleatoria]
            n -= 1

    return m

def limpa_campo(m, c):
    """
    campo x coordenada → campo
    modifica destrutivamente o campo limpando 
    a parcela na coordenada e devolvendo-o
    """

    if not eh_parcela_limpa(obtem_parcela(m, c)) and \
        not eh_parcela_minada(obtem_parcela(m, c)):

        limpa_parcela(obtem_parcela(m, c))
    
        if obtem_numero_minas_vizinhas(m, c) == 0:

            for coordenada in obtem_coordenadas_vizinhas(c):
                if eh_coordenada_do_campo(m, coordenada) and \
                    eh_parcela_tapada(obtem_parcela(m, coordenada)):

                    limpa_campo(m, coordenada) 
                    #chama-se aqui a funcao limpa_campo 
                    #de modo a limpar-se recursivamente

    elif eh_parcela_minada(obtem_parcela(m, c)):
        limpa_parcela(obtem_parcela(m, c))

    return m

def jogo_ganho(m):
    """
    campo → booleano
    recebe um campo do jogo das minas e verifica se
    o jogo esta' ganho
    """ 

    for coluna in range(ord(obtem_ultima_coluna(m)) - ord('A') + 1):
        for linha in range(obtem_ultima_linha(m)):
            parcela = obtem_parcela(m, cria_coordenada(chr(ord('A') + coluna),\
                                                        linha + 1))
            if not eh_parcela_minada(parcela) and \
                not eh_parcela_limpa(parcela):
                #se existir uma parcela sem mina que nao
                #esta' limpa, o jogo ainda nao foi ganho

                return False
    
    return True
    
def turno_jogador(m):
    """
    campo → booleano
    recebe um campo de minas e oferece ao jogador a opcao
    de escolher uma acao e uma coordenada, e verifica se
    com a jogada realizada, o jogador nao perde o jogo
    """

    acao = input('Escolha uma ação, [L]impar ou [M]arcar:')
    while acao != 'L' and acao != 'M':
        acao = input('Escolha uma ação, [L]impar ou [M]arcar:')

    coordenada_valida = False
    while not coordenada_valida:
        str_coordenada = input('Escolha uma coordenada:')

        try:
            coordenada = str_para_coordenada(str_coordenada)
            
        except:
            continue

        if eh_coordenada_do_campo(m, coordenada):
            coordenada_valida = True

    if acao == 'L':
        if eh_parcela_minada(obtem_parcela(m, coordenada)):
            limpa_parcela(obtem_parcela(m, coordenada))
            return False
            #o jogador perdeu o jogo

        limpa_campo(m, coordenada)

    if acao == 'M':
        alterna_bandeira(obtem_parcela(m, coordenada))

    return True

def minas(c, l, n, d, s):
    """
    str x int x int x int x int → booleano
    verifica se o jogador ganhou ou perdeu o jogo
    """

    def calcula_nr_bandeiras(m):
        """
        campo -> int
        calcula o numero de bandeiras usadas no campo
        """

        nr_bandeiras = 0

        for coluna in range(ord(obtem_ultima_coluna(m)) - ord('A') + 1):
            for linha in range(obtem_ultima_linha(m)):
                parcela = obtem_parcela(m, cria_coordenada( \
                                        chr(ord('A') + coluna), linha + 1))
                if eh_parcela_marcada(parcela):
                    nr_bandeiras += 1

        return nr_bandeiras

    def bandeiras_para_str(m, n): 
        #para representar o numero de bandeiras utilizadas pelo jogador
        return '   [Bandeiras ' + str(calcula_nr_bandeiras(m)) + '/' + str(n) + ']'

    if not(isinstance(c, str) and isinstance(l, int) and len(c) == 1 \
        and 'A' <= c <= 'Z' and 1 <= l <= 99 and (ord(c) - ord('A') >= 4 \
        or l >= 4 )and isinstance(d, int) and isinstance(s, int) and \
        (d == 32 or d == 64) and s > 0 and s < 2 ** d and isinstance(n, int) \
        and 0 < n < (ord(c) - ord('A')) * l):
        #numero de minas nao pode ultrapassar nem ser igual 
        #ao numero de coordenadas do campo

        raise ValueError('minas: argumentos invalidos')

    m = cria_campo(c, l)
    g = cria_gerador(d, s)

    print(bandeiras_para_str(m, n))
    print(campo_para_str(m))

    #a primeira jogada vai apenas pedir uma coordenada, 
    #pois a acao vai ser automaticamente limpar

    coordenada_valida = False
    while not coordenada_valida:
        str_coordenada_turno_1 = input('Escolha uma coordenada:')

        try:
            coordenada = str_para_coordenada(str_coordenada_turno_1)
        except:
            continue

        if eh_coordenada_do_campo(m, coordenada):
            coordenada_valida = True

    #apenas apos saber a coordenada da primeira 
    #jogada e' que se posicionam as minas

    coloca_minas(m, str_para_coordenada(str_coordenada_turno_1), g, n)
    limpa_campo(m, str_para_coordenada(str_coordenada_turno_1))
    print(bandeiras_para_str(m, n))
    print(campo_para_str(m))

    while jogo_ganho(m) == False:
        if turno_jogador(m) == False:
            print(bandeiras_para_str(m, n))
            print(campo_para_str(m))
            print('BOOOOOOOM!!!')
            return False
            
        print(bandeiras_para_str(m, n))
        print(campo_para_str(m))

    print('VITORIA!!!')
    return True