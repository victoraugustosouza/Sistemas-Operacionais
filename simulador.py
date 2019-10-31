#Trabalho1 de Sistemas Operacionais: Algoritmos de substituição de páginas,
#descrição: http://wiki.inf.ufpr.br/maziero/doku.php?id=so:algoritmos_de_substituicao_de_paginas
#Alunos: Victor Augusto Souza de Oliveira
#		 João Pedro Gandarela

#Versão Python Utilizada: 3.7.3
# Bibliotecas: sys 
#			   collections
#			   datetime
#
#Execução via linha de comando:
#
# Modelo: $ python nome_do_arquivo.py numero_de_quadros < arquivo_com_referencias.txt
# Exemplo $ python simulador.py 1024 < vsim-gcc.txt
#
#
import sys
from collections import namedtuple
from datetime import datetime

data = sys.stdin.readlines() #get data file from stdin
# print(data)
vetor_de_paginas = []
lru = namedtuple("lru", "page date")

for i in range(len(data)):
	vetor_de_paginas.append(int(data[i].strip("\n"))) #saving data

n_quadros = int(sys.argv[1]) #get second argument from comand line, that is the number of quartos
# print(n_quadros)

def pagina_saida_otimo(contador,ram,vetor):
	vetor_auxiliar = len(ram)*[-1]
	cont = contador
	temp=-1
	for j in range(len(ram)):
		pagina = ram[j]
		if(j>0):
			if(vetor_auxiliar[j-1]==temp):
				return vetor_auxiliar.index(temp)
		for k in range(0,len(vetor)):
			if(pagina == vetor[k]):
				vetor_auxiliar[j] = k
				break

	maior = -2 
	
	if temp in vetor_auxiliar:
		return vetor_auxiliar.index(temp)

	for m in vetor_auxiliar:
		if m > maior:
			maior = m
	if maior > -1:
		return vetor_auxiliar.index(maior)
	return 0


def OTIMO(vetor,n_quadros):

	pag_fault = 0
	ram =  []
	contador = 0
	#print(len(vetor_de_paginas))

	while(contador < len(vetor)):
		pagina=vetor[contador]
		#print(contador)
		if pagina in ram:

			contador=contador+1
			continue
		else:
			pag_fault=pag_fault+1

		if(len(ram) < n_quadros ):
			ram.append(pagina)
		
		else:
			num = pagina_saida_otimo(contador,ram,vetor[contador+1:])
			del ram[num]
		
			ram.append(pagina)
		contador=contador+1
		#print(contador)


	print("OPT: {} PFs. ".format(str(pag_fault)))




def FIFO(vetor_de_paginas,n_quadros):
	pag_fault = 0
	ram =  []
	contador = 0
	#print(len(vetor_de_paginas))

	while(contador < len(vetor_de_paginas)):
		pagina=vetor_de_paginas[contador]
		#print(contador)
		if pagina in ram:

			contador=contador+1
			continue
		else:
			pag_fault=pag_fault+1

		if(len(ram) < n_quadros ):
			ram.append(pagina)
		
		else:
			del ram[0]
		
			ram.append(pagina)
		contador=contador+1
	print("FIFO: {} PFs, ".format(str(pag_fault)), end="        ")

def pagina_saida_lru(ram,m):
	minor = m[0]
	for index in range(len(m)):
		if(m[index].date < minor.date):
			minor=m[index]
	return ram.index(int(minor.page))
	
def update_time(page,m):
	for index in range(len(m)):
		if(m[index].page == page):
			del m[index]
			m.append(lru(page=page, date=datetime.now()))
			return m

def delete_m(m,new_page, old):
	for index in range(len(m)):
		if(m[index].page==old):
			del m[index]
			return m


def LRU(vetor_de_paginas,n_quadros):
	pag_fault = 0
	ram =  []
	contador = 0
	lru = namedtuple("lru", "page date")
	m = []

	while(contador < len(vetor_de_paginas)):
		pagina=vetor_de_paginas[contador]

		if pagina in ram:
			contador=contador+1
			m=update_time(pagina,m)
			continue
		else:
			pag_fault=pag_fault+1


		if(len(ram) < n_quadros ):
			ram.append(pagina)
			m.append(lru(page=pagina, date=datetime.now()))
			# print(contador)
			# print(len(m))
		
		else:
			# print(len(ram))
			num = pagina_saida_lru(ram,m)
			m=delete_m(m,pagina,ram[num])
			# print(num)
			del ram[num]
			ram.append(pagina)
			m.append(lru(page=pagina, date=datetime.now()))
		contador=contador+1
	print("LRU: {} PFs, ".format(str(pag_fault)), end="        ")





#print(ram)
#print(contador)
print("{} quadros,	{} refs:".format(n_quadros,len(data)),end="       ")
FIFO(vetor_de_paginas,n_quadros)
LRU(vetor_de_paginas,n_quadros)
OTIMO(vetor_de_paginas,n_quadros)