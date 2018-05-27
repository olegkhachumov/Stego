import math
import time
import stego.wht as wht

"""
Содержит необходимые функции для работы с кодом Рида-Маллера RM(1,m)
Предоставляет возможность создавать кодовую и проверочную матрицы, кодировать,
вычислять синдром, декодировать, используя переборный декодер, декодер на основе БПУ,
декодер на основе подхода Лицына-Шеховцова

"""

def print_matrix(checkMatrix):
	#распечатывает проверочную / кодовую матрицу
	#так как они хранятся в виде словаря 
	f=[]
	for i in range(len(checkMatrix)):
		for j in range(len(checkMatrix[0])):
			if(j in checkMatrix[i]):
				f.append(1)
			else:
				f.append(0)
		print(i, '  ', f)
		f=[]



def generator(n, k, checkMatrix):
	#генерирует все строки проверочной матрицы при r>1
	#наверняка можно сделать быстрее с модулем itertools
	#но работает эта штука один раз, так что все равно
	a=[i+1 for i in range(0, k)]
	p=k
	length = len(checkMatrix)-1
	if n==k:		
		length+=1
		checkMatrix.update({length:[]})
		for i in range(len(checkMatrix[0])):
			f = True
			for j in a:
				if i not in checkMatrix[j]:
					f= False
			if f:
				checkMatrix[length].append(i)
	else:
		while p>=1:
			#обработка сочетания:
			length+=1
			checkMatrix.update({length:[]})
			for i in range(len(checkMatrix[0])):
				f = True
				for j in a:
					if i not in checkMatrix[j]:
						f= False
				if f:
					checkMatrix[length].append(i)

			if(a[k-1]==n):
				p=p-1
			else:
				p=k

			if p>=1:
				for i in range(k, p-1, -1):
					a[i-1]=a[p-1]+i-p+1



def make_check_matrix(r,m):
	#генерирует проверочную матрицу кода RM(r,m)
	if r<-1 or r==m:
		raise ValueError
	t=m-r-1;
	n=pow(2,m);
	checkMatrix ={0:[]}
	checkMatrix[0]=[i for i in range(n)]
	if t == 0:
		return checkMatrix
	for i in range(1, m+1):
		 checkMatrix.update({i:[]})
	for i in range(0, n):
		f = wht.int_to_list(i, m)
		for j in range(1, m+1):
			if(f[j-1]==1):
				checkMatrix[j].append(i)


	for i in range(2,t+1):
		generator(m, i, checkMatrix)
	#print(checkMatrix)
	return checkMatrix

def make_coding_matrix(r,m):
	#создает кодовую матрицу для кода RM(r,m)
	return make_check_matrix(m-r-1,m)

def coding(f, codingMatrix):
	#кодирует слово из пространства F_2^k
	g=[0 for i in range(len(codingMatrix[0]))]
	for i in range(len(f)):
		if(f[i]==1):
			for j in codingMatrix[i]:
				g[j]=g[j]^1
	return g


def compute_sindrom(f, checkMatrix): 
	#Вычисляет синдром от слова f 
	s=[0 for i in range(len(checkMatrix))]
	for i in range(len(checkMatrix)):
		for j in checkMatrix[i]:
			s[i]=s[i]^f[j]
	return s


def make_equation(checkMatrix):
	#работает в паре с функцией solve
	#выдает необходимые соотношения для нахождения вектора q по синдрому s: q*H^t = s
	equation = {}
	for i in range(0, len(checkMatrix)):
		equation.update({checkMatrix[i][0]:[i]})
	for i in range(len(checkMatrix)-1, 0, -1):
		for j in range(i-1, -1, -1):
			if(checkMatrix[i][0] in checkMatrix[j]):
				equation[checkMatrix[j][0]].append(i) 
	return equation



def solve(equation, checkMatrix, s):
	# работает в паре с функцией makeEquation, находит вектор q по синдрому s: q*H^t = s
	q=[0 for i in range(len(checkMatrix[0]))]
	for i in equation:
		for j in equation[i]:
			q[i]^=s[j]
	return q


def make_codewords(codingMatrix, m):
	#генерирует все кодовые слова RM(1,m)
	codewords={}
	f=[0 for i in range(len(codingMatrix[0]))]
	for i in range(pow(2, m+1)):
		codewords.update({i:coding(wht.int_to_list(i,m+1),codingMatrix)})
	return codewords

def brute_force_decoder(f, codewords):
	#переборный декодер для кода RM(1,m)
	g=[]
	dist = len(f)
	for i in codewords:
		w=wht.weight(wht.xor(f,codewords[i]))
		if(w < dist):
			dist = w
			g = codewords[i]
	return g

def decoderLS(f, m):
	#декодер на основе подхода Лицына-Шеховцова для кода RM(1,m)
	#названия переменных ужасные, но соответствуют тем, что используются в оригинальной статье
	F=[]
	S=[]
	S1=[]
	s=[0,0]
	v=[0 for i in range(m+1)]
	for i in f:
		F.append(1-2*i)
		S.append(0)	
	i = len(f)
	j = 1
	while j!=m+1:
		length = len(F)//2
		for k in range(length):
			S[k]=F[2*k]
			S[len(F)//2+k]=F[2*k+1]
		S1.clear()	
		s=[0,0]
		S1.append(wht.sum(S[0:length], S[length:2*length]))
		S1.append(wht.dif(S[0:length], S[length:2*length]))
		for i in range(length):
			s[0]+=abs(S1[0][i])
			s[1]+=abs(S1[1][i])
		if(s[0]>s[1]):
			
			F=list(S1[0])
		else:
			v[m+1-j]=1
			F=list(S1[1])
		j+=1	
	if(abs(S1[0][0])>abs(S1[1][0])):
		if(S1[0][0])<0:
			v[0]=1
	else:
		if(S1[1][0])<0:
			v[0]=1
	return v


def decoder_wht(f):
	#декодер на быстром преобразовании Уолша-Адамара для кода RM(1,m)
	F=wht.wht(f)
	pos = wht._abs(F).index(max(wht._abs(F)))
	g=[0]
	if F[pos] <0:
		g[0] = 1
	g.extend(wht.int_to_list(pos,int(math.log2(len(f)))))
	return g
