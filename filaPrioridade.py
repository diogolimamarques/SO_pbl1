import sys

# Classe que imprementa uma fila de prioridade adaptada para a resolução do problema.

class filaPrioridade(object): 

  # Inicialização da fila

  def __init__(self, op): 
    self.queue = [] 
    self.modoDeOperacao = op
  
  def __str__(self): 
    return ' '.join([str(i) for i in self.queue]) 
  
  # Checa se a fila está vazia
  def isEmpty(self): 
    return len(self.queue) == 0
  
  # Insere um elemento no fim da fila

  def insert(self, data): 
    self.queue.append(data) 
  
  # Função principal da fila de prioridade. Ela varre a fila por completo e retorna o
  # primeiro índice numérico do elemento priorizado. Caso não haja distinção de prioridade,
  # ela simplesmente retorna o primeiro elemento da lista (FIFO)

  def retornaProximo(self):
    if self.isEmpty():
      return 0
    try:
      max = 0
      if (self.modoDeOperacao != 2): # se nao distinguir leitores e escritores
        for i in range(len(self.queue)-1):
          if (self.modoDeOperacao == 0): # se priorizar escritores
            if self.queue[i].tipo < self.queue[max].tipo:
              max = i
          elif (self.modoDeOperacao == 1): # se priorizar leitores
            if self.queue[i].tipo > self.queue[max].tipo: 
              max = i
      prox = self.queue[max].num
      return prox
    except IndexError: 
      return -1

  # Busca na lista pelo elemento de acordo com seu índice numérico e o remove.

  def deletaElemento(self, num):
    for i in range(len(self.queue)):
      if self.queue[i].num == num:
        del self.queue[i]
        return
