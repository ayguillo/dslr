import numpy as np

def transposition(matrice):
	matrice_column_nb, matrice_line_nb = len(matrice[0]), len(matrice)
	new_matrice = []
	for i in range(matrice_column_nb):
		new_matrice.append([])
	for line in range(matrice_line_nb):
		for column in range (matrice_column_nb):
			new_matrice[column] += [matrice[line][column]]
	return np.array(new_matrice)

def product(matrice1, matrice2):
	matrice1_column_nb, matrice1_line_nb = len(matrice1[0]), len(matrice1)
	matrice2_column_nb, matrice2_line_nb = len(matrice2[0]), len(matrice2)
	new_matrice = []
	if matrice1_column_nb != matrice2_line_nb or matrice1_line_nb != matrice2_column_nb:
		return None
	for line in range(matrice1_line_nb):
		new_matrice.append([])
		for column in range(matrice2_column_nb):
			tmp = 0
			for i in range(matrice1_column_nb):
				print(matrice1[line][i], matrice2[i][column])
				tmp += matrice1[line][i] * matrice2[i][column]
			new_matrice[line] += [tmp]
	return np.array(new_matrice)

def product_by_nb(matrice, nb):
	matrice_column_nb, matrice_line_nb = len(matrice[0]), len(matrice)
	for line in range(matrice_line_nb):
		for column in range(matrice_column_nb):
			matrice[line][column] = matrice[line][column] * nb
	return matrice

# A = np.array([[1,2,5],[3,4,6]])
# print(A)
# # print(transposition(A))
# # print(A.T)
# # print()
# B = np.array([[9,8], [7,6], [5,4]])
# print(B)
# print(product(A, B))
# print(A @ B)
# # print(B)
# print(transposition(B))
# print(B.T)