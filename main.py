from threading import Thread
from random import randint
import random
import string
import sys
import os

NUMERO_DE_THREADS = 1 # ESTE VALOR INDICA A QUANTIDADE DE THREADS QUE SERÃO GERADAS.
                      # Vale ressaltar que, como não foram implementadas estratégias de sincro-
                      # nização, aumentar o número de threads serve para ilustrar a dessincro-
                      # nização das alterações num ambiente desordenado.

# Classe que extende da classe Thread.

class Th(Thread):

  # -----------------------------------------------------------
  #
  # Funcao de inicialização da thread. Avisa no terminal sobre sua criacao e gera um 
  # countdown aleatorio entre 0 e 10. O countdown serve para que, no caso de varias
  # threads estarem sendo executadas, a ideia de desincronização possa ficar mais nítida.
  #
  # -----------------------------------------------------------

  def __init__ (self, num):
    sys.stdout.write("Criando a thread de numero " + str(num) + "\n")
    sys.stdout.flush()
    Thread.__init__(self)
    self.num = num
    self.countdown = randint(0, 10)

  # -----------------------------------------------------------
  #
  # Funcao run, que é a função de execução da thread. Basicamente, é como se fosse o main
  # da thread. Aqui o countdown é eventualmente zerado, um caractere aleatório é selecionado
  # e é chamada a função de alterar o arquivo. O arquivo a ser alterado também é selecionado
  # aleatoriamente de acordo com seu nome.
  #
  # -----------------------------------------------------------

  def run(self):
    while (self.countdown):
      sys.stdout.write("Thread " + str(self.num) + " (" + str(self.countdown) + ")\n")
      sys.stdout.flush()
      self.countdown -= 1

    randomLetter = random.choice(string.ascii_letters)
    nomeArquivo = "arquivos/arquivo"+str(randint(1,3))+".txt"
    self.alteraArquivo(nomeArquivo, randomLetter)

  # -----------------------------------------------------------
  #
  # Funcao de alterar o arquivo. Ela abre o arquivo em questão e faz uma concatenação da string
  # passada para ela no fim do arquivo. Por fim, ela chama a funcao de replicação.
  #
  # -----------------------------------------------------------

  def alteraArquivo(self, nomeArquivo, randomLetter):
    f = open(nomeArquivo, "a")
    f.write(randomLetter)
    f.close()
    self.replicaAlteracao(nomeArquivo, randomLetter)

  # -----------------------------------------------------------
  #
  # Funcao de replicação. Ela varre todos os arquivos na pasta indicada e altera todos os que
  # tiverem o nome diferente do arquivo original com a mesma alteração do original. Vale ressaltar
  # que, CASO NÃO SEJAM IMPLEMENTADAS ESTRATÉGIAS DE SINCRONIZAÇÃO, as alterações serão feitas de
  # maneira desordenada. Isso acontece por que as threads operam em tempos diferentes. Por isso,
  # apesar de os caracteres a serem concatenados nos arquivos serem os mesmos, a ordem pode variar
  # se esta operação estiver sendo feita com VÁRIAS THREADS SIMULTANEAS.
  #
  # -----------------------------------------------------------

  def replicaAlteracao(self, arquivoOriginal, alteracao):
    for filename in os.listdir('arquivos'):
      if ("arquivos/"+filename != arquivoOriginal):
        f = open("arquivos/"+filename, "a")
        f.write(alteracao)
        f.close()


# Corpo principal do código.

for thread_number in range (NUMERO_DE_THREADS):
  thread = Th(thread_number)
  thread.start()

