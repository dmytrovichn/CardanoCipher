from cardano import Cardano
from pprint import pprint
from file_manager import read_text, write_text

# matrix = [
#         ["+", "+", "+", "0"],
#         ["+", "+", "0", "+"],
#         ["0", "+", "+", "+"],
#         ["+", "0", "+", "+"]
#     ]
# 4x4
# 'мамамиларамурано' -> рмрмиаааммлнуаоа  рмрмиаааммлнуаоа
#
# 6x6
# 'мамамиларамураномамамиларамураноeeee'


print("Menu")
while True:

    op = int(input("Option\n1-Encrypt\n2-Decrypt\n0-Exit\n~ "))
    if op == 2:
        try:
            key_length = int(input("Please enter matrix size k x k (k should be only even): k = "))
            cardano = Cardano(key_length)
        except Exception as e:
            print(e)
            print("Please enter new matrix size.")
            continue

        print("Please add key")
        key_op = int(input("1-Choice position on matrix\n2-Import from file\n~ "))
        if key_op == 1:
            matrix = Cardano.create_key_matrix(key_length)
            print("Key:")
            pprint(matrix)
        else:
            try:
                file_name = input("Enter file name: ")
                points = Cardano.read_key_from_file(f"{file_name}.txt")
                matrix = Cardano.insert_point_to_matrix(points, key_length)
                print("Key:")
                pprint(matrix)
            except Exception as e:
                print(e)
                continue

        file_name = input("Please enter plain text file name: ")
        try:
            save_file_name = f'docs/decrypted_{file_name}.txt'
            file_name = f'docs/{file_name}.txt'
            plain_text = read_text(file_name)
            text_block = [plain_text[x:x + key_length ** 2] for x in range(0, len(plain_text), key_length ** 2)]
            plain_text = ""
            for text in text_block:
                plain_text += cardano.decrypt(text, matrix)
            write_text(save_file_name, plain_text)
        except Exception as e:
            print(e)
    elif op == 1:
        try:
            key_length = int(input("Please enter matrix size k x k (k should be only even): k = "))
            cardano = Cardano(key_length)
        except Exception as e:
            print(e)
            print("Please enter new matrix size.")
            continue

        print("Please add key")
        key_op = int(input("1-Choice position on matrix\n2-Import from file\n3-Auto generate\n~ "))

        if key_op == 1:
            matrix = Cardano.create_key_matrix(key_length)
            print("Key:")
            pprint(matrix)
        elif key_op == 2:
            try:
                file_name = input("Enter file name: ")
                points = Cardano.read_key_from_file(f"{file_name}.txt")
                matrix = Cardano.insert_point_to_matrix(points, key_length)
                print("Key:")
                pprint(matrix)
            except Exception as e:
                print(e)
                continue
        else:
            matrix = Cardano.auto_generate_matrix_key(key_length)
            print("Key:")
            pprint(matrix)

        file_name = input("Please enter cipher text file name: ")
        try:
            save_file_name = f'docs/encrypted_{file_name}.txt'
            file_name = f'docs/{file_name}.txt'
            plain_text = read_text(file_name)
            text_block = [plain_text[x:x+key_length**2] for x in range(0, len(plain_text), key_length**2)]
            cipher = ""
            for text in text_block:
                cipher += cardano.encrypt(text, matrix)
            write_text(save_file_name, cipher)

            more_op = int(input("Do you want save key? 1-Y 2-N "))
            if more_op == 1:
                file_name = input("Enter file name: ")
                cardano.write_key_to_file(f"{file_name}.txt")
        except Exception as e:
            print(e)
    elif op == 0:
        break


