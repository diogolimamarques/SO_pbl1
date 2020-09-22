from threading import Thread
from random import randint
import random
import string
import sys
import os

# Classe que extende da classe Thread.

class Th(Thread):

  # -----------------------------------------------------------
  #
  # Funcao de inicialização da thread. Avisa no terminal sobre sua criacao e gera um 
  # countdown aleatorio entre 0 e 10. O countdown serve para que, no caso de varias
  # threads estarem sendo executadas, a ideia de desincronização possa ficar mais nítida.
  #
  # -----------------------------------------------------------

  def __init__ (self, num, type, escalonador):
    Thread.__init__(self)
    self.num = num
    self.countdown = randint(0, 10)
    self.type = type # 0 = escritor, 1 = leitor
    self.escalonador = escalonador

    if self.type == 0:
      tipo = "ESCRITOR"
    elif self.type == 1:
      tipo = "LEITOR"

    sys.stdout.write("Criando a thread de numero " + str(num) + " e tipo " + tipo + "\n")
    sys.stdout.flush()

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
      #sys.stdout.write("Thread " + str(self.num) + " (" + str(self.countdown) + ")\n")
      sys.stdout.flush()
      self.countdown -= 1

    if self.type == 0:
      randomLetter = random.choice(string.ascii_letters)
      nomeArquivo = "arquivos/arquivo"+str(randint(1,3))+".txt"
      self.alteraArquivo(nomeArquivo, randomLetter)
    elif self.type == 1:
      nomeArquivo = "arquivos/arquivo"+str(randint(1,3))+".txt"
      self.leArquivo(nomeArquivo)

  # -----------------------------------------------------------
  #
  # Funcao de alterar o arquivo. Ela abre o arquivo em questão e faz uma concatenação da string
  # passada para ela no fim do arquivo. Por fim, ela chama a funcao de replicação.
  #
  # -----------------------------------------------------------

  def alteraArquivo(self, nomeArquivo, randomLetter):
    permissao = False

    sys.stdout.write("Thread de numero " + str(self.num) + " aguardando permissao para escrever\n")
    sys.stdout.flush()

    while(permissao == False):
      if (self.escalonador.retornaProximo() == self.num):
        permissao = True

    sys.stdout.write("Thread de numero " + str(self.num) + " escrevendo agora\n")
    sys.stdout.flush()

    f = open(nomeArquivo, "a")
    f.write(randomLetter)
    f.close()
    self.replicaAlteracao(nomeArquivo, randomLetter)

    sys.stdout.write("Thread de numero " + str(self.num) + " concluiu operacao de escrita\n")
    sys.stdout.flush()

    self.escalonador.deletaElemento(self.num)

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


  def leArquivo(self, nomeArquivo):
    permissao = False

    sys.stdout.write("Thread de numero " + str(self.num) + " aguardando permissao para ler\n")
    sys.stdout.flush()

    while(permissao == False):
      if (self.escalonador.retornaProximo() == self.num):
        permissao = True
    f = open(nomeArquivo, "r")
    sys.stdout.write("Thread "+str(self.num)+" lendo o arquivo no endereco: "+nomeArquivo+"\n")
    sys.stdout.write("Conteudo encontrado: "+f.read()+"\n")
    sys.stdout.flush()
    f.close()

    self.escalonador.deletaElemento(self.num)

# Classe simplificada que representa uma determinada thread dentro da lista de prioridade

class ThRef():
  def __init__(self, num, tipo): 
    self.num = num
    self.tipo = tipo
