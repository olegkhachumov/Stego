import math

#--------операции над двоичными векторами----------

def fft(f):
	# на входе двоичный вектор f длины 2^m, на выходе его преобразование Фурье
	n = int(math.log2(len(f)))
	F = list(f)
	F1 = [0 for i in range(len(f))]

	for i in range(n):
		pos=pow(2,i)
		for j in range(0,len(F), pow(2, i+1)): 
			for k in range(0, pos):
				F1[k+j]=F[k+j]+F[pos+k+j]
				F1[k+j+pos]=F[k+j]-F[pos+k+j]
		F=list(F1)
	return(F)


def ifft(f):
	#обратное преобразование Фурье
	n = int(math.log2(len(f)))
	F = list(f)
	F1 = [0 for i in range(len(f))]

	for i in range(n):
		pos=pow(2,i)
		for j in range(0,len(F), pow(2, i+1)):
			for k in range(0, pos):
				F1[k+j]=F[k+j]+F[pos+k+j]
				F1[k+j+pos]=F[k+j]-F[pos+k+j]
		F=list(F1)
	k=pow(2,n)	
	F = [i//k for i in F]
	return(F)

def wht(f):
	#преобразование Уолша-Адамара
	return fft([pow(-1, i) for i in f])

def iwht(f):
	#обратное преобразование Уолша-Адамара
	return [-(i-1)//2 for i in ifft(f)]	

def is_null(f):
	# только для двоичных векторов!
	#проверяет является ли вектор нулевым
	return 1 not in f

def list_to_int(arr):
	#перевод двоичного вектора в целове число
	return int('0b'+''.join(map(str,arr)), 2)

def int_to_list(a,n):
	#перевод целого числа в двоичный вектор
	return list(map(int,'0'*(n-int((lambda x: 0 if x==0 else math.log2(x))(a))-1)+bin(a)[2:]))

def xor(f,g):
	#побитовый xor двух векторов
	return [i^j for i,j in zip(f,g)]

def weight(f):
	# возвращает вес бинарного вектора f
	return f.count(1)

def distance(f,g):
	#расстояние между двумя бинарными векторами
	return weight(xor(f,g))

#--------операции над целочисленными векторами----------

def sum(f,g):
	#сложение двух векторов (уже не в F2)
	return [i+j for i,j in zip(f,g)]

def dif(f,g):
	#разность двух векторов (уже не в F2)
	return [i-j for i,j in zip(f,g)]

def _abs(f):
	#абсолютное значение вектора
	return [abs(i) for i in f]

