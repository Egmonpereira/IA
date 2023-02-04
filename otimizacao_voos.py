# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from funcao_custo import Funcao_Custo
import time, random, math

class Otimizacao(object):
    def __init__(self, pessoas, destino, dominio, agenda, agenda2, solucao, temperatura, resfriamento, passo, tam_pop, prob_mutacao, elitismo, num_geracoes):
        self.pessoas = pessoas
        self.destino = destino
        self.dominio = dominio
        self.agenda = agenda
        self.agenda2 = agenda2
        self.solucao = solucao
        self.temperatura = temperatura
        self.resfriamento = resfriamento
        self.passo = passo
        self.tam_pop = tam_pop
        self.prob_mutacao = prob_mutacao
        self.elitismo = elitismo
        self.num_geracoes = num_geracoes

    def imprime_agenda(self):
        id_voo = -1
        
        voos = {}
        
        for linha in open('voos.txt'):
            _origem, _destino, _saida, _chegada, _preco = linha.split(',')
            voos.setdefault((_origem, _destino), []) #setdefault retorna o item com a chave especificada. Se o valor não exita ele add no dicionário uma nova chave com os valores
            voos[(_origem, _destino)].append((_saida, _chegada, int(_preco)))

        for i in range(len(self.agenda) // 2):
            nome = self.pessoas[i][0]
            origem = self.pessoas[i][1]
            id_voo += 1
            ida = voos[(origem, self.destino)][self.agenda[id_voo]]
            id_voo += 1
            volta = voos[(self.destino, origem)][self.agenda[id_voo]]
            print('%10s%10s %5s-%5s R$%3s %5s-%5s R$%3s' % (nome, origem, ida[0], ida[1], ida[2],
                                                            volta[0], volta[1], volta[2]))
    
    def pesquisa_rand(self):
        melhor_custo = 9999999
        for i in range(0, 10000):
            solucao = [random.randint(self.dominio[i][0], self.dominio[0][1]) for i in range(len(self.dominio))]
            custo = Funcao_Custo(self.agenda, self.pessoas, self.destino).funcao_custo()
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_solucao = solucao
        
        return melhor_solucao          

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

            atual = Funcao_Custo(agenda, self.pessoas, self.destino).funcao_custo()
            melhor = atual
            for i in range(len(vizinhos)):
                custo = Funcao_Custo(vizinhos[i], self.pessoas, self.destino).funcao_custo()
                if custo < melhor:
                    melhor = custo
                    agenda = vizinhos[i]
            if melhor == atual:
                break
        return titulo, agenda, melhor

    def tempera_simulada(self):
        titulo = 'FUNÇÃO TEMPERA SIMULADA'
        print('\n',titulo,'\n')
        agenda = [random.randint(self.dominio[i][0], self.dominio[i][1]) for i in range(len(self.dominio))]
        while self.temperatura > 0.1:
            i = random.randint(0,len(self.dominio) - 1)
            direcao = random.randint(-self.passo, self.passo)
            agenda_temp = agenda[:]
            agenda_temp[i] += direcao
            
            if agenda_temp[i] < self.dominio[i][0]:
                agenda_temp[i] = self.dominio[i][0]
            elif agenda_temp[i] > self.dominio[i][1]:
                agenda_temp[i] = self.dominio[i][1]

            custo_agenda = Funcao_Custo(agenda, self.pessoas, self.destino).funcao_custo()
            custo_agenda_temp = Funcao_Custo(agenda, self.pessoas, self.destino).funcao_custo()
            probabilidade = pow(math.e, (-custo_agenda_temp - custo_agenda) / self.temperatura)

            if (custo_agenda_temp < custo_agenda or random.random() < probabilidade):
                agenda = agenda_temp

            self.temperatura = self.temperatura * self.resfriamento

        
        return titulo, agenda, custo_agenda

    def genetico(self):
        titulo = 'FUNÇÃO MUTAÇÃO GENÉTICA'
        print('\n',titulo,'\n')

        pop_inicial = []
        c1 = c2 = 0

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

        def cruzamento(dominio, agenda1, agenda2):
            i = random.randint(1, len(dominio) - 2)
            
            return agenda1[0:i] + agenda2[i:]

        for i in range(self.tam_pop):
            agenda = [random.randint(self.dominio[i][0], self.dominio[i][1]) for i in range(len(self.dominio))]
            pop_inicial.append(agenda)

        num_elitismo = int(self.elitismo * self.tam_pop)

        for i in range(self.num_geracoes):
            custos = [(Funcao_Custo(individuo, self.pessoas, self.destino).funcao_custo(), individuo) for individuo in pop_inicial]
            custos.sort()
            individuos_ordnados = [individuo for (custo, individuo) in custos]

            pop_inicial = individuos_ordnados[0:num_elitismo]

            while len(pop_inicial) < self.tam_pop:
                if random.random() < self.prob_mutacao:
                    m = random.randint(0,num_elitismo)
                    pop_inicial.append(mutacao(self.dominio, self.passo, individuos_ordnados[m]))
                else:
                    while c1 == c2:
                        c1 = random.randint(0,num_elitismo)
                        c2 = random. randint(0,num_elitismo)
                    pop_inicial.append(cruzamento(self.dominio, individuos_ordnados[c1], individuos_ordnados[c2]))
        
        return titulo, custos[0][1]