from Model import Model
import numpy as np
from Intermediary import Intermediary

transformation_matrix = [[0.00257904, 0.0 , 0.0 , 0.0],
                            [0.0, 0.00257904, 0.0 , 0.0],
                            [0.0, 0.0, 0.00257904, 0.0],
                            [0.0, 0.0, 0.0, 1.0]]

project_matrix = np.identity(4)
project_matrix[2][2] = 0
model_matrix = np.identity(4)
figure = Intermediary(Model('olen'), project_matrix, model_matrix)

new_verts = [*map(lambda vert: vert @ transformation_matrix, figure.model.vertices)]

with open('obj/deer.obj', 'w', encoding='utf8') as file:
    for vert in new_verts:
        file.write(f'v {vert[0]:.8f} {vert[1]:.8f} {vert[2]:.8f} {vert[3]:.8f}\n')
    file.write('\n')
    for face in figure.model.faces:
        file.write(f'f {face[0]} {face[1]} {face[2]}\n')
    file.write('\n')
