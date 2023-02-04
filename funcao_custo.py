import time

class Funcao_Custo(object):
    def __init__(self, agenda, pessoas, destino):
        self.agenda = agenda
        self.pessoas = pessoas
        self.destino = destino
        

    def funcao_custo(self):
        preco_total = 0
        ultima_chegada = 0 #pessoa que chega mais tarde
        primeira_partida = 1439#voo de retorno 1439 = máximo de minutos de atraso
        
        voos = {}
        
        for linha in open('voos.txt'):
            _origem, _destino, _saida, _chegada, _preco = linha.split(',')
            voos.setdefault((_origem, _destino), []) #setdefault retorna o item com a chave especificada. Se o valor não exita ele add no dicionário uma nova chave com os valores
            voos[(_origem, _destino)].append((_saida, _chegada, int(_preco)))
        
        #Função para manipular minutos
        def get_minutos(hora):
            x = time.strptime(hora, '%H:%M')
            minutos = x[3] * 60 + x[4]
            return minutos

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