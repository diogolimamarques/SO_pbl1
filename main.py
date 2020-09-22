import Th
import sys
import filaPrioridade
from random import randint

NUMERO_DE_THREADS = 100 # ESTE VALOR INDICA A QUANTIDADE DE THREADS QUE SERÃO GERADAS.
                      # Vale ressaltar que, como não foram implementadas estratégias de sincro-
                      # nização, aumentar o número de threads serve para ilustrar a dessincro-
                      # nização das alterações num ambiente desordenado.

MODO_DE_OPERACAO = 0  # 0 = escritores tem prioridade 
                      # 1 = leitores tem prioridade
                      # 2 = prioridade equivalente
                      
# Corpo principal do código.

escalonador = filaPrioridade.filaPrioridade(MODO_DE_OPERACAO)

for thread_number in range (NUMERO_DE_THREADS):
  tipo = randint(0,1)
  #tipo = 0
  thread = Th.Th(thread_number, tipo, escalonador) # gera aleatoriamente um escritor ou leitor
  threadRef = Th.ThRef(thread_number, tipo)
  escalonador.insert(threadRef)
  sys.stdout.write("Proximo da fila: "+str(escalonador.retornaProximo())+"\n")
  sys.stdout.flush()
  thread.start()

while(True):
  loop = 0

#while not escalonador.isEmpty(): 
  #print(escalonador.proximo()) 
