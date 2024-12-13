from file_manager import read_key, write_key
import random
from pprint import pprint


class Cardano:

    def __init__(self, matrix_size):
        if matrix_size % 2 != 0:
            raise Exception("Wrong matrix size k x k, k should be only even number")
        self.key_length = int(matrix_size ** 2 / 4)
        self.matrix_size = matrix_size
        self.key_points = []
        self.base_points = []

    def get_steps_and_rotate_matrix(self, key_matrix):
        if self.key_points:
            first_step = False
        else:
            first_step = True

        temp_matrix = [row.copy() for row in key_matrix]

        column_range = range(self.matrix_size - 1, -1, -1) if not first_step else range(self.matrix_size)
        for row in range(self.matrix_size):
            for index, column in enumerate(column_range):
                if first_step and temp_matrix[row][column] == '+':
                    self.key_points.append((row, index))
                elif not first_step:
                    if temp_matrix[column][row] == '+':
                        self.key_points.append((row, index))
                    key_matrix[row][index] = temp_matrix[column][row]

    def set_steps(self, key_matrix):
        self.key_points = []

        """Step 1 start matrix key"""
        self.get_steps_and_rotate_matrix(key_matrix)
        """Step 2 rotate to 90 degree"""
        self.get_steps_and_rotate_matrix(key_matrix)
        """Step 3 rotate to 90 degree"""
        self.get_steps_and_rotate_matrix(key_matrix)
        """Step 4 rotate to 90 degree"""
        self.get_steps_and_rotate_matrix(key_matrix)

        self.base_points = self.key_points[:self.key_length]

    def encrypt(self, plain_text, key_matrix):
        cipher_text = ''
        encrypted_matrix = [row.copy() for row in key_matrix]

        plain_text = self.validate_text(plain_text)

        if not self.key_points:
            self.set_steps(key_matrix)

        if len(set(self.key_points)) != self.matrix_size**2:
            raise Exception(f"You provide bed key matrix len position "
                            f"{len(set(self.key_points))}, matrix {self.matrix_size**2}")

        for index, point in enumerate(self.key_points):
            row, column = point
            encrypted_matrix[row][column] = plain_text[index]

        for row in encrypted_matrix:
            cipher_text += ''.join(row)

        return cipher_text

    def decrypt(self, cipher_text, key_matrix):
        plain_text = ''
        encrypted_matrix = [row.copy() for row in key_matrix]

        if not self.key_points:
            self.set_steps(key_matrix)

        index = 0
        for row in range(self.matrix_size):
            for column in range(self.matrix_size):
                encrypted_matrix[row][column] = cipher_text[index]
                index += 1

        if len(set(self.key_points)) != self.matrix_size**2:
            raise Exception("You provide bed key matrix")

        for row, column in self.key_points:
            plain_text += encrypted_matrix[row][column]

        return plain_text

    def validate_text(self, text):
        if self.matrix_size**2 > len(text):
            return text + " " * ((self.matrix_size**2) - len(text))
        return text

    @staticmethod
    def create_empty_matrix(matrix_size):
        full_matrix = [['*'] * matrix_size for i in range(matrix_size)]
        small_matrix = [['*'] * (int(matrix_size/2)) for i in range(int(matrix_size/2))]

        index = 1
        for i in range(int(matrix_size/2)):
            for j in range(int(matrix_size/2)):
                small_matrix[i][j] = str(index)
                full_matrix[i][j] = str(index)
                index += 1

        Cardano.rotate_matrix(small_matrix, int(matrix_size/2))
        for i in range(int(matrix_size/2)):
            for j in range(int(matrix_size/2), matrix_size):
                full_matrix[i][j] = small_matrix[i][j-int(matrix_size/2)]

        Cardano.rotate_matrix(small_matrix, int(matrix_size / 2))
        for i in range(int(matrix_size/2), matrix_size):
            for j in range(int(matrix_size/2), matrix_size):
                full_matrix[i][j] = small_matrix[i-int(matrix_size/2)][j-int(matrix_size/2)]

        Cardano.rotate_matrix(small_matrix, int(matrix_size / 2))
        for i in range(int(matrix_size/2), matrix_size):
            for j in range(int(matrix_size/2)):
                full_matrix[i][j] = small_matrix[i-int(matrix_size/2)][j]

        return full_matrix

    @staticmethod
    def rotate_matrix(matrix, length):
        temp_matrix = [row.copy() for row in matrix]
        for row in range(length):
            for index, column in enumerate(range(length - 1, -1, -1)):
                matrix[row][index] = temp_matrix[column][row]

    def write_key_to_file(self, file_name):
        write_key(file_name, self.base_points)

    @staticmethod
    def read_key_from_file(file_name):
        return read_key(file_name)

    @staticmethod
    def create_key_matrix(matrix_size):
        matrix = Cardano.create_empty_matrix(matrix_size)
        print("Empty matrix")
        pprint(matrix)
        for i in range(int(matrix_size ** 2 / 4)):
            print(f"Point {i + 1}/{int(matrix_size ** 2 / 4)}")
            row = int(input(f"Enter row between 0 and {matrix_size-1}: "))
            column = int(input(f"Enter column between 0 and {matrix_size-1}: "))
            pos = str(matrix[row][column])
            for j in range(matrix_size):
                matrix[j] = ",".join(matrix[j]).replace(pos, "-").split(",")
            matrix[row][column] = "+"
            pprint(matrix)
        return matrix

    @staticmethod
    def insert_point_to_matrix(points, matrix_size):
        if len(points) != (matrix_size**2)/4:
            raise Exception("You enter wrong size of matrix or bed key")
        matrix = [["-"] * matrix_size for i in range(matrix_size)]
        for row, col in points:
            matrix[row][col] = "+"

        return matrix

    @staticmethod
    def auto_generate_matrix_key(key_length):
        matrix = Cardano.create_empty_matrix(key_length)
        i = 0
        while int(key_length**2/4) != i:
            row = int(random.randint(0, key_length-1))
            col = int(random.randint(0, key_length-1))
            if matrix[row][col] not in ["-", "+"]:
                pos = matrix[row][col]
                for j in range(key_length):
                    matrix[j] = ",".join(matrix[j]).replace(pos, "-").split(",")
                matrix[row][col] = "+"
                i += 1

        return matrix
