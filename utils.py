import os


def read_classification_from_file(filepath):
    dictionary = {}
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split(' ')
            if len(line) == 2:
                dictionary[line[0]] = line[1].replace('\n', '')

    return dictionary


if __name__ == '__main__':
    print(read_classification_from_file('spam-data-12-s75-h25/1/!truth.txt'))
