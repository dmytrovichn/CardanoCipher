def read_key(file_name):
    try:
        with open(file_name, "r") as file:
            text = file.read()
        text = text.split(",")
        points = []
        for line in text:
            row, col = tuple(line)
            points.append((int(row), int(col)))
        return points
    except:
        raise Exception("Can't read key from file")


def write_key(file_name, key_points):
    try:
        text = [f"{row}{col}" for row, col in key_points]
        text = ",".join(text)
        with open(file_name, "w") as file:
            file.write(text)
    except:
        raise Exception("Can't write key to the file")


def read_text(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def write_text(file_name, text):
    with open(file_name, "w") as f:
        f.write(text)
