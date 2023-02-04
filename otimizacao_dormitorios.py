from otimizacao_voos import Otimizacao
import pandas, random, math

class Otimizacao_dormitorios(object):
    def __init__(self):
        pass

    def otimizacao_dormitorios(self):
        dormitorios = ['São Paulo','Flamengo','Coritiba','Cruzeiro','Fortaleza']

        preferencias = [('Amanda', ('Cruzeiro', 'Coritiba')),
        ('Pedro', ('São Paulo', 'Fortaleza')),
        ('Marcos', ('Flamengo', 'São Paulo')),
        ('Priscila', ('São Paulo', 'Fortaleza')),
        ('Jessica', ('Flamengo', 'Cruzeiro')),
        ('Paulo', ('Coritiba', 'Fortaleza')),
        ('Fred', ('Fortaleza', 'Flamengo')),
        ('Suzana', ('Cruzeiro', 'Coritiba')),
        ('Laura', ('Cruzeiro', 'Coritiba')),
        ('Ricardo', ('Coritiba', 'Flamengo '))]

        Solucao = [6,1,2,1,2,0,2,2,0,0]
        
        dominio = [(0, (len(dormitorios) * 2) - i - 1) for i in range(0, len(dormitorios) * 2)]

        def imprimir_solucao(solucao):
            Quartos = Vagas = []

            for i in range(len(dormitorios)):
                Vagas += [i, i]

            for i in range(len(solucao)):
                atual = solucao[i]
                dormitorio = dormitorios[Vagas[atual]]
                Quartos.append([preferencias[i][0], dormitorio])
                del Vagas[atual]

            df = pandas.DataFrame(Quartos)
            df.columns = ['Estudnate','Quarto']
            print(df)

            return dormitorio

        imprimir_solucao(Solucao)

        def funcao_custo(Solucao):
            custo = 0
            Vagas = [0,0,1,1,2,2,3,3,4,4]
            for i in range(len(Solucao)):
                atual = Solucao[i]
                dormitorio = dormitorios[Vagas[atual]]
                preferencia = preferencias[i][1]

                if preferencia[0] == dormitorio:
                    custo += 0
                elif preferencia[1] == dormitorio:
                    custo += 1
                else:
                    custo += 3

                del Vagas[atual]

            return custo

        print('\nMelhor custo %d' %funcao_custo(Solucao))

        def pesquisa_rand(dominio, funcao_custo):
            melhor_custo = 9999999
            for i in range(0, 10000):
                solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
                custo = funcao_custo(Solucao)
                if custo < melhor_custo:
                    melhor_custo = custo
                    melhor_solucao = solucao

            return melhor_solucao          


        def hill_climb(dominio,funcao_custo):
            print('\nFUNÇÃO HILL CLIMB')
            solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
            while True:

                vizinhos = []

                for i in range(len(dominio)):
                    if solucao[i] > dominio[i][0]:
                        if solucao[i] != dominio[i][1]:
                            vizinhos.append(solucao[0:i] + [solucao[i] + 1] + solucao[i + 1:])
                    if solucao[i] < dominio[i][1]:
                        if solucao[i] != dominio[i][0]:
                            vizinhos.append(solucao[0:i] + [solucao[i] - 1] + solucao[i + 1:])

                atual = funcao_custo(solucao)
                melhor = atual
                for i in range(len(vizinhos)):
                    custo = funcao_custo(vizinhos[i])
                    if custo < melhor:
                        melhor = custo
                        solucao = vizinhos[i]
                if melhor == atual:
                    break
            return solucao


        def tempera_simulada(dominio, funcao_custo):
            passo, temperatura, resfriamento = 1, 10000, 0.95
            print('\nFUNÇÃO TEMPERA SIMULADA')
            solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
            while temperatura > 0.1:
                i = random.randint(0,len(dominio) - 1)
                direcao = random.randint(passo, passo)
                solucao_temp = solucao[:]
                solucao_temp[i] += direcao
                
                if solucao_temp[i] < dominio[i][0]:
                    solucao_temp[i] = dominio[i][0]
                elif solucao_temp[i] > dominio[i][1]:
                    solucao_temp[i] = dominio[i][1]

                custo_solucao = funcao_custo(solucao)
                custo_solucao_temp = funcao_custo(solucao)
                probabilidade = pow(math.e, (-custo_solucao_temp - custo_solucao) / temperatura)

                if (custo_solucao_temp < custo_solucao or random.random() < probabilidade):
                    solucao = solucao_temp

                temperatura = temperatura * resfriamento

            
            return solucao

        def genetico(dominio, funcao_genetica):
            print('\nFUNÇÃO MUTAÇÃO GENÉTICA')

            pop_inicial = []
            c1 = c2 = 0
            passo, tam_pop, prob_mutacao, elitismo, num_geracoes = 1, 50, 0.2, 0.2, 100

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
            
            return custos[0][1]
            
        print('\nFUNÇÃO RANDÔMICA')
        solucao_randomica = pesquisa_rand(dominio, funcao_custo)
        custo_randomica = funcao_custo(solucao_randomica)
        print('custo_randomica %d' %custo_randomica)
        imprimir_solucao(solucao_randomica)

        solucao_hill_climb = hill_climb(dominio, funcao_custo)
        custo_hill_climb = funcao_custo(solucao_hill_climb)
        print('custo_randomica %d' %custo_hill_climb)
        imprimir_solucao(solucao_hill_climb)

        solucao_tempera = tempera_simulada(dominio, funcao_custo)
        custo_tempera = funcao_custo(solucao_tempera)
        print('custo_randomica %d' %custo_tempera)
        imprimir_solucao(solucao_tempera)

        solucao_genetico = genetico(dominio, funcao_custo)
        custo_genetico = funcao_custo(solucao_genetico)
        print('custo_randomica %d' %custo_genetico)
        imprimir_solucao(solucao_genetico)

        return dominio

        '''
        MELHOR SOLUÇÃO:
        FUNÇÃO MUTAÇÃO GENÉTICA
        custo_randomica 2
        Estudnate     Quarto
        0    Amanda   Coritiba
        1     Pedro  São Paulo
        2    Marcos   Flamengo
        3  Priscila  São Paulo
        4   Jessica   Flamengo
        5     Paulo  Fortaleza
        6      Fred  Fortaleza
        7    Suzana   Cruzeiro
        8     Laura   Cruzeiro
        9   Ricardo   Coritiba
        '''