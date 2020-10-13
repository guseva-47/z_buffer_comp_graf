# афинные преобразования
import numpy as np
from math import sin, cos, radians

def dilation(x, y, z):
    """Матрица растяжения/сжатия"""
    matrix = np.identity(4)
    matrix[0][0], matrix[1][1], matrix[2][2] = x, y, z
    return matrix

def reflectionX():
    """Отражения по X"""
    matrix = np.identity(4)
    matrix[0][0] = -1
    return matrix

def reflectionY():
    """Отражения по Y"""
    matrix = np.identity(4)
    matrix[1][1] = -1
    return matrix

def reflectionZ():
    """Отражения по Z"""
    matrix = np.identity(4)
    matrix[2][2] = -1
    return matrix

def translation(x, y, z):
    """Матрица переноса"""
    matrix = np.identity(4)
    matrix[3][0], matrix[3][1], matrix[3][2] = x, y, z
    return matrix

def rotationX(angle):
    """Вращение вокруг X"""
    matrix = np.identity(4)
    matrix[1][1], matrix[1][2] = cos(angle), sin(angle)
    matrix[2][1], matrix[2][2] = -sin(angle), cos(angle)
    return matrix

def rotationY(angle):
    """Вращение вокруг Y"""
    matrix = np.identity(4)
    matrix[0][0], matrix[0][2] = cos(angle), -sin(angle)
    matrix[2][0], matrix[2][2] = sin(angle), cos(angle)
    return matrix

def rotationZ(angle):
    """Вращение вокруг Z"""
    matrix = np.identity(4)
    matrix[0][0], matrix[0][1] = cos(angle), sin(angle)
    matrix[1][0], matrix[1][1] = -sin(angle), cos(angle)
    return matrix

def orthoPoject():
    """Ортографическая проекция"""
    project_matrix = np.identity(4)
    project_matrix[2][2] = 0
    return project_matrix

def perspectiveProject(z):
    """Перспективная проекция"""
    matrix = np.identity(4)
    matrix[2, 2] = 0
    matrix[2, 3] = -1/z
    return matrix

def cosougProject(f, angle):
    """Косоугольная проекция"""
    project_matrix = np.identity(4)
    project_matrix[2][2] = 0
    project_matrix[2][0] = -f * cos(angle)
    project_matrix[2][1] = -f * sin(angle)
    return project_matrix

def cavalerProject():
    """Проекция Ковалье"""
    return cosougProject(1, radians(45))

def kabinetProject():
    """Кабинетная проекция"""
    return cosougProject(0.5, radians(45))
