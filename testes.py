# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time, random, os

def otimizacao(self):
    inicio = time.time()
    titulo = 'FUNÇÃO OTIMIZAÇÃO'
    print('\n',titulo,'\n')
    pessoas = [('Amanda','CWB'),
               ('Pedro','GIG'),
               ('Marcos','POA'),
               ('Priscila','FLN'),
               ('Jessica','CNF'),
               ('Paulo','GYN')]
    
    destino = 'GRU'
    
    voos = {}
    '''
    for linha in open('voos.txt'):
        _origem, _destino, _saida, _chegada, _preco = linha.split(',')
        voos.setdefault((_origem, _destino), []) #setdefault retorna o item com a chave especificada. Se o valor não exita ele add no dicionário uma nova chave com os valores
        voos[(_origem, _destino)].append((_saida, _chegada, int(_preco)))
        
    agenda = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
    
    def imprime_agenda(agenda):
        id_voo = -1
        
        for i in range(len(agenda) // 2):
            nome = pessoas[i][0]
            origem = pessoas[i][1]
            id_voo += 1
            ida = voos[(origem, destino)][agenda[id_voo]]
            id_voo += 1
            volta = voos[(destino, origem)][agenda[id_voo]]
            print('%10s%10s %5s-%5s R$%3s %5s-%5s R$%3s' % (nome, origem, ida[0], ida[1], ida[2],
                                                            volta[0], volta[1], volta[2]))
    
    #Função para manipular minutos
    def get_minutos(hora):
        x = time.strptime(hora, '%H:%M')
        minutos = x[3] * 60 + x[4]
        return minutos
    
    def funcao_custo(agenda):
        preco_total = 0
        ultima_chegada = 0 #pessoa que chega mais tarde
        primeira_partida = 1439#voo de retorno 1439 = máximo de minutos de atraso
        
        id_voo = -1
        for i in range(len(agenda) // 2):
            origem = pessoas[i][1]
            id_voo += 1
            ida = voos[(origem, destino)][agenda[id_voo]]
            id_voo += 1
            volta = voos[(destino, origem)][agenda[id_voo]]
            
            preco_total += ida[2]
            preco_total += volta[2]
            
            if ultima_chegada < get_minutos(ida[1]):
                ultima_chegada = get_minutos(ida[1])
                
            if primeira_partida > get_minutos(volta[0]):
                primeira_partida = get_minutos(volta[0])
                
        
        total_espera = 0
        id_voo = -1
        for i in range(len(agenda) // 2):
            origem = pessoas[i][1]
            id_voo += 1
            ida = voos[(origem, destino)][agenda[id_voo]]
            id_voo += 1
            volta = voos[(destino, origem)][agenda[id_voo]]
            
            total_espera += ultima_chegada - get_minutos(ida[1])
            total_espera += get_minutos(volta[0]) - primeira_partida
            
        if ultima_chegada > primeira_partida:
            preco_total += 50
            
        return preco_total + total_espera
    
    
    def pesquisa_rand(dominio, funcao_custo):
        melhor_custo = 9999999
        for i in range(0, 10000):
            solucao = [random.randint(dominio[i][0], dominio[0][1]) for i in range(len(dominio))]
            custo = funcao_custo(solucao)
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_solucao = solucao
        
        return melhor_solucao          
    
    dominio = [(0,9)] * (len(pessoas) * 2)
    solucao_randomica = pesquisa_rand(dominio, funcao_custo)
    print(solucao_randomica)
    custo_randomico = funcao_custo(solucao_randomica)
    print('Melhor Custo = R$ %2.2f' %custo_randomico)
    imprime_agenda(solucao_randomica)
    fim = time.time()
    print('Tempo %s: %0.2f' %(titulo,fim-inicio))
    
    def hill_climb(dominio, funcao_custo):
        titulo = 'FUNÇÃO HILL CLIMB'
        print('\n',titulo,'\n')
        agenda = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
        while True:
    
            vizinhos = []
    
            for i in range(len(dominio)):
                if agenda[i] > dominio[i][0]:
                    if agenda[i] != dominio[i][1]:
                        vizinhos.append(agenda[0:i] + [agenda[i] + 1] + agenda[i + 1:])
                if agenda[i] < dominio[i][1]:
                    if agenda[i] != dominio[i][0]:
                        vizinhos.append(agenda[0:i] + [agenda[i] - 1] + agenda[i + 1:])
    
            atual = funcao_custo(agenda)
            melhor = atual
            for i in range(len(vizinhos)):
                custo = funcao_custo(vizinhos[i])
                if custo < melhor:
                    melhor = custo
                    agenda = vizinhos[i]
            if melhor == atual:
                break
        return agenda, titulo
    
    inicio = time.time()
    solucao_hill_climb,titulo = hill_climb(dominio, funcao_custo)
    print(solucao_hill_climb)
    custo_hill_climb = funcao_custo(solucao_hill_climb)
    print('Melhor Custo Hill Climb = R$ %2.2f' %custo_hill_climb)
    imprime_agenda(solucao_hill_climb)
    fim = time.time()
    print('\nTempo %s: %0.2f' %(titulo,fim-inicio))
    
    tempera_simulada(dominio, funcao_custo, 10000, 0.95, 1)

    def tempera_simulada(dominio, funcao_custo, temperatura, resfriamento, passo):
        titulo = 'FUNÇÃO TEMPERA SIMULADA'
        print('\n',titulo,'\n')
        agenda = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
        print(agenda)
    