from otimizacao_voos import Otimizacao
from otimizacao_dormitorios import Otimizacao_dormitorios
from funcao_custo import Funcao_Custo
from pyinputplus import inputChoice, RetryLimitException
import os,time

if __name__ == "__main__":
    os.system('clear')

    try:
        num = ['1','2']
        escolha = '2'#inputChoice(num, limit=3, prompt='ESCOLHA UMA DAS ALTERNATIVAS ABAIXO\n1 - Problema dos Voos\n2 - Problema dos Dormitórios\n')
    except RetryLimitException:
        print('Acabaram suas chances')
    else:
        if escolha == '1':
            inicio = time.time()
            titulo = 'FUNÇÃO OTIMIZAÇÃO'
            pessoas = [('Amanda','CWB'),
                        ('Pedro','GIG'),
                        ('Marcos','POA'),
                        ('Priscila','FLN'),
                        ('Jessica','CNF'),
                        ('Paulo','GYN')]
            
            destino = 'GRU'
            dominio = [(0,9)] * (len(pessoas) * 2)
            agenda = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
            agenda2 = [0,1, 2,5, 8,9, 2,3, 5,1, 0,6]
            temperatura, resfriamento, passo, tam_pop, prob_mutacao, elitismo, num_geracoes = 10000, 0.95, 2, 50, 0.2, 0.2, 100
            

            print('\n',titulo,'\n')
            solucao = Otimizacao(pessoas, destino, dominio, agenda, agenda2, 0, temperatura, resfriamento, passo, tam_pop, prob_mutacao, elitismo, num_geracoes).pesquisa_rand()
            custo_randomico = Funcao_Custo(agenda, pessoas, destino).funcao_custo()
            Otimizacao(pessoas, destino, dominio, agenda, agenda2, solucao, temperatura, resfriamento, passo, tam_pop, prob_mutacao, elitismo, num_geracoes).imprime_agenda()
            print('\nMelhor Custo = R$ %0.2f' %custo_randomico)
            fim = time.time()
            print('\nTempo %s: %0.2fs\n' %(titulo,fim-inicio))

            
            inicio = time.time()
            titulo, solucao, custo = Otimizacao(pessoas, destino, dominio, agenda, agenda2, solucao, temperatura, resfriamento, passo, tam_pop, prob_mutacao, elitismo, num_geracoes).hill_climb()
            Otimizacao(pessoas, destino, dominio, agenda, agenda2, solucao, temperatura, resfriamento, passo, tam_pop, prob_mutacao, elitismo, num_geracoes).imprime_agenda()
            print('\nMelhor Custo Hill Climb = R$ %2.2f' %custo)
            fim = time.time()
            print('\nTempo %s: %0.2fs\n' %(titulo,fim-inicio))


            inicio = time.time()
            titulo, solucao, custo_tempera_simulada = Otimizacao(pessoas, destino, dominio, agenda, agenda2, solucao, temperatura, resfriamento, passo, tam_pop, prob_mutacao, elitismo, num_geracoes).tempera_simulada()
            Otimizacao(pessoas, destino, dominio, agenda, agenda2, solucao, temperatura, resfriamento, passo, tam_pop, prob_mutacao, elitismo, num_geracoes).imprime_agenda()
            print('\nMelhor Custo Tempera Simulada = R$ %.2f\n' %custo_tempera_simulada)
            fim = time.time()
            print('\nTempo %s = %0.2fs\n' %(titulo,fim-inicio))

            inicio = time.time()
            titulo, solucao = Otimizacao(pessoas, destino, dominio, agenda, agenda2, solucao, temperatura, resfriamento, passo, tam_pop, prob_mutacao, elitismo, num_geracoes).genetico()
            custo_mutacao_genetica = Funcao_Custo(agenda, pessoas, destino).funcao_custo()
            Otimizacao(pessoas, destino, dominio, agenda, agenda2, solucao, temperatura, resfriamento, passo, tam_pop, prob_mutacao, elitismo, num_geracoes).imprime_agenda()
            print('\nMelhor Custo Mutacao Genetica = R$ %.2f' %custo_mutacao_genetica)
            fim = time.time()
            print('\nTempo %s = %0.2fs\n' %(titulo,fim-inicio))
        else:
            Otimizacao_dormitorios().otimizacao_dormitorios()
