import numpy as np

def matrix_multiplication(a, b):
    try:
        return np.matmul(a, b)
    except ValueError:
        print("Matrices are not compatible for multiplication")
        return None

def rotationX(angle):
    rotation_matrix = np.array([[1, 0, 0],
                                [0, np.cos(angle), -np.sin(angle)],
                                [0, np.sin(angle), np.cos(angle)]])
    return rotation_matrix

def rotationY(angle):
    rotation_matrix = np.array([[np.cos(angle), 0, -np.sin(angle)],
                                [0, 1, 0],
                                [np.sin(angle), 0, np.cos(angle)]])
    return rotation_matrix

def rotationZ(angle):
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                [np.sin(angle), np.cos(angle), 0],
                                [0, 0, 1]])
    return rotation_matrix