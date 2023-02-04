# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time, random, math

class Otimizacao(object):
    def __init__(self,pessoas, destino, dominio, agenda):
        self.pessoas = pessoas
        self.destino = destino
        self.dominio = dominio
        self.agenda = agenda
    
    def otimizacao(self):
        inicio = time.time()
        
        voos = {}
        
        for linha in open('voos.txt'):
            _origem, _destino, _saida, _chegada, _preco = linha.split(',')
            voos.setdefault((_origem, _destino), []) #setdefault retorna o item com a chave especificada. Se o valor não exita ele add no dicionário uma nova chave com os valores
            voos[(_origem, _destino)].append((_saida, _chegada, int(_preco)))

        return voos
    def imprime_agenda(self):
        id_voo = -1
        voos = Otimizacao().otimizacao()
        for i in range(len(self.agenda) // 2):
            nome = self.pessoas[i][0]
            origem = self.pessoas[i][1]
            id_voo += 1
            ida = voos[(origem, self.destino)][agenda[id_voo]]
            id_voo += 1
            volta = voos[(self.destino, origem)][agenda[id_voo]]
            print('%10s%10s %5s-%5s R$%3s %5s-%5s R$%3s' % (nome, origem, ida[0], ida[1], ida[2],
                                                            volta[0], volta[1], volta[2]))
        
    #Função para manipular minutos
    def get_minutos(hora):
        x = time.strptime(hora, '%H:%M')
        minutos = x[3] * 60 + x[4]
        return minutos
    
    def funcao_custo(self):
        preco_total = 0
        ultima_chegada = 0 #pessoa que chega mais tarde
        primeira_partida = 1439#voo de retorno 1439 = máximo de minutos de atraso
        
        id_voo = -1
        for i in range(len(self.agenda) // 2):
            origem = self.pessoas[i][1]
            id_voo += 1
            ida = voos[(origem, self.destino)][self.agenda[id_voo]]
            id_voo += 1
            volta = voos[(self.destino, origem)][self.agenda[id_voo]]
            
            preco_total += ida[2]
            preco_total += volta[2]
            
            if ultima_chegada < get_minutos(ida[1]):
                ultima_chegada = get_minutos(ida[1])
                
            if primeira_partida > get_minutos(volta[0]):
                primeira_partida = get_minutos(volta[0])
                
        
        total_espera = 0
        id_voo = -1
        for i in range(len(self.agenda) // 2):
            origem = self.pessoas[i][1]
            id_voo += 1
            ida = voos[(origem, self.destino)][self.agenda[id_voo]]
            id_voo += 1
            volta = voos[(self.destino, origem)][self.agenda[id_voo]]
            
            total_espera += ultima_chegada - get_minutos(ida[1])
            total_espera += get_minutos(volta[0]) - primeira_partida
            
        if ultima_chegada > primeira_partida:
            preco_total += 50
            
        return preco_total + total_espera

    
    def pesquisa_rand(self):
        melhor_custo = 9999999
        for i in range(0, 10000):
            solucao = [random.randint(self.dominio[i][0], self.dominio[0][1]) for i in range(len(self.dominio))]
            custo = Otimizacao().funcao_custo(solucao)
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_solucao = solucao
        
        return melhor_solucao          
    
    print('\n',titulo,'\n')
    solucao_randomica = pesquisa_rand(self.dominio)
    custo_randomico = funcao_custo(solucao_randomica)
    imprime_agenda(solucao_randomica)
    print('\nMelhor Custo = R$ %0.2f' %custo_randomico)
    fim = time.time()
    print('\nTempo %s: %0.2fs\n' %(titulo,fim-inicio))

    def hill_climb(self):
        titulo = 'FUNÇÃO HILL CLIMB'
        print('\n',titulo,'\n')
        agenda = [random.randint(self.dominio[i][0], self.dominio[i][1]) for i in range(len(self.dominio))]
        while True:

            vizinhos = []

            for i in range(len(self.dominio)):
                if agenda[i] > self.dominio[i][0]:
                    if agenda[i] != self.dominio[i][1]:
                        vizinhos.append(agenda[0:i] + [agenda[i] + 1] + agenda[i + 1:])
                if agenda[i] < self.dominio[i][1]:
                    if agenda[i] != self.dominio[i][0]:
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
        return titulo, agenda, melhor

    inicio = time.time()
    titulo, solucao_hill_climb, custo = hill_climb(self.dominio, Otimizacao().funcao_custo)
    imprime_agenda(solucao_hill_climb)
    print('\nMelhor Custo Hill Climb = R$ %2.2f' %custo)
    fim = time.time()
    print('\nTempo %s: %0.2fs\n' %(titulo,fim-inicio))

    def tempera_simulada(dominio, funcao_custo, temperatura, resfriamento, passo):
        titulo = 'FUNÇÃO TEMPERA SIMULADA'
        print('\n',titulo,'\n')
        agenda = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
        while temperatura > 0.1:
            i = random.randint(0,len(dominio) - 1)
            direcao = random.randint(-passo, passo)
            agenda_temp = agenda[:]
            agenda_temp[i] += direcao
            
            if agenda_temp[i] < dominio[i][0]:
                agenda_temp[i] = dominio[i][0]
            elif agenda_temp[i] > dominio[i][1]:
                agenda_temp[i] = dominio[i][1]

            custo_agenda = funcao_custo(agenda)
            custo_agenda_temp = funcao_custo(agenda_temp)
            probabilidade = pow(math.e, (-custo_agenda_temp - custo_agenda) / temperatura)

            if (custo_agenda_temp < custo_agenda or random.random() < probabilidade):
                agenda = agenda_temp

            temperatura = temperatura * resfriamento

        
        return titulo, agenda, custo_agenda

    inicio = time.time()
    titulo, solucao_tempera_simulada, custo_tempera_simulada = tempera_simulada(self.dominio, Otimizacao().funcao_custo, 10000, 0.95, 2)
    imprime_agenda(solucao_tempera_simulada)
    print('\nMelhor Custo Tempera Simulada = R$ %.2f\n' %custo_tempera_simulada)
    fim = time.time()
    print('\nTempo %s = %0.2fs\n' %(titulo,fim-inicio))

    agenda = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]

    def mutacao(dominio, passo, agenda):
        i = random.randint(0, len(dominio) - 1)
        mutante = agenda

        if random.random() < 0.5:
            if agenda[i] != dominio[i][0]:
                mutante = agenda[0:i] + [agenda[i] - passo] + agenda[i + 1:]
            else:
                if agenda[i] != dominio[i][1]:
                    mutante = agenda[0:i] + [agenda[i] + passo] + agenda[i + 1:]
        
        return mutante

    #mutante = mutacao(dominio, 1, agenda)

    def cruzamento(dominio, agenda1, agenda2):
        i = random.randint(1, len(dominio) - 2)
        
        return agenda1[0:i] + agenda2[i:]

    agenda1 = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
    agenda2 = [0,1, 2,5, 8,9, 2,3, 5,1, 0,6]

    agenda3 = cruzamento(self.dominio, agenda1, agenda2)
    print('Agenda pós mutação = ',agenda3)

    def genetico(dominio, funcao_custo, tam_pop, passo, prob_mutacao, elitismo, num_geracoes):
        titulo = 'FUNÇÃO MUTAÇÃO GENÉTICA'
        print('\n',titulo,'\n')

        pop_inicial = []
        c1 = c2 = 0
        
        for i in range(tam_pop):
            agenda = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
            pop_inicial.append(agenda)

        num_elitismo = int(elitismo * tam_pop)

        for i in range(num_geracoes):
            custos = [(funcao_custo(individuo), individuo) for individuo in pop_inicial]
            custos.sort()
            individuos_ordnados = [individuo for (custo, individuo) in custos]

            pop_inicial = individuos_ordnados[0:num_elitismo]

            while len(pop_inicial) < tam_pop:
                if random.random() < prob_mutacao:
                    m = random.randint(0,num_elitismo)
                    pop_inicial.append(mutacao(dominio, passo, individuos_ordnados[m]))
                else:
                    while c1 == c2:
                        c1 = random.randint(0,num_elitismo)
                        c2 = random. randint(0,num_elitismo)
                    pop_inicial.append(cruzamento(dominio, individuos_ordnados[c1], individuos_ordnados[c2]))
        
        return titulo, custos[0][1]
        
    inicio = time.time()
    titulo, solucao_mutacao_genetica = genetico(self.dominio, Otimizacao().funcao_custo, 100, 2, 0.2, 0.2, 500)
    custo_mutacao_genetica = Otimizacao().funcao_custo(solucao_mutacao_genetica)
    imprime_agenda(solucao_mutacao_genetica)
    print('\nMelhor Custo Mutacao Genetica = R$ %.2f' %custo_mutacao_genetica)
    fim = time.time()
    print('\nTempo %s = %0.2fs\n' %(titulo,fim-inicio))
