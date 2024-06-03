import numpy as np

def sub_matrix(M : list, indexes : list):
    len_ind = len(indexes)
    new_M = np.zeros((len_ind,len_ind)).tolist()
    for i in range(len_ind):
        for j in range(len_ind):
            new_M[i][j] = M[indexes[i]][indexes[j]]

    return new_M
