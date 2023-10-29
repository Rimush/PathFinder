from time import time
from random import random, shuffle
from math import cos, sin, sqrt, atan2, pi, inf


class Path:
    def __init__(self, index, length):
        self.index = index
        self.length = length


class ACO:

    def __init__(self, ants, iteration, a, b, p, q):
        self.ants = ants            # Количество муравьев
        self.iteration = iteration  # Количество итераций
        self.a = a                  # Альфа
        self.b = b                  # Бета
        self.p = p                  # Коэффициент испарения феромона
        self.q = q                  # Сила феромона

    @staticmethod
    def __select_i(selection):
        sum_numbers = sum(selection)
        if sum_numbers == 0:
            return len(selection) - 1

        rnd_number = random()
        cur_number = 0
        for i in range(len(selection)):
            cur_number += selection[i] / sum_numbers
            if cur_number >= rnd_number:
                return i

    @staticmethod
    def __earthly_distance(a, b):
        radian_latitude_a = a[0] * pi / 180
        radian_latitude_b = b[0] * pi / 180
        radian_longitude_a = a[1] * pi / 180
        radian_longitude_b = b[1] * pi / 180
        cos_latitude_a = cos(radian_latitude_a)
        cos_latitude_b = cos(radian_latitude_b)
        sin_latitude_a = sin(radian_latitude_a)
        sin_latitude_b = sin(radian_latitude_b)
        delta = radian_longitude_b - radian_longitude_a
        cos_delta = cos(delta)
        sin_delta = sin(delta)

        y = sqrt((cos_latitude_b * sin_delta) ** 2 +
                 (cos_latitude_a * sin_latitude_b - sin_latitude_a * cos_latitude_b * cos_delta) ** 2)

        x = sin_latitude_a * sin_latitude_b + cos_latitude_a * cos_latitude_b * cos_delta

        distance = atan2(y, x)

        return distance * 6372.795

    @staticmethod
    def __calculate_distance(matrix_distance, index):
        distance = 0
        for i in range(len(index) - 1):
            distance += matrix_distance[index[i]][index[i + 1]]

        return distance

    @staticmethod
    def __shift(path):
        zero = path.index(0)
        new_path = path[zero:] + path[1:zero] + [0]
        for index in range(len(new_path)):
            new_path[index] = new_path[index] + 1

        return new_path

    def __distance_matrix(self, points):
        matrix = []
        for a in points:
            line = []
            for b in points:
                line.append(self.__earthly_distance(a, b))
            matrix.append(line)

        return matrix

    def __create_index(self, matrix_distance, matrix_pheromone):
        length = len(matrix_distance)
        unvisited_index = list(range(length))
        shuffle(unvisited_index)
        visited_index = [unvisited_index.pop()]

        for _ in range(length - 1):
            i = visited_index[-1]
            selection = []
            for j in unvisited_index:
                selection.append(
                    (matrix_pheromone[i][j] ** self.a) * ((1 / max(matrix_distance[i][j], 10 ** -5)) ** self.b)
                )
            selected_i = self.__select_i(selection)
            visited_index.append(unvisited_index.pop(selected_i))
        visited_index.append(visited_index[0])

        return visited_index

    def update_matrix_pheromone(self, matrix_pheromone, tmp_index, tmp_length):
        length = len(matrix_pheromone)
        for i in range(length):
            for j in range(i, length):
                matrix_pheromone[i][j] *= 1 - self.p
                matrix_pheromone[j][i] *= 1 - self.p
        for i in range(self.ants):
            delta = self.q / tmp_length[i]
            index = tmp_index[i]
            for j in range(length):
                matrix_pheromone[index[j]][index[j + 1]] += delta
                matrix_pheromone[index[j + 1]][index[j]] += delta

    def run(self, points):
        length = len(points)
        dm = self.__distance_matrix(points)

        matrix_pheromone = []
        for i in range(length):
            tmp_line = []
            for j in range(length):
                tmp_line.append(1)
            matrix_pheromone.append(tmp_line)

        res_index = []
        res_length = inf
        for _ in range(self.iteration):
            tmp_index = []
            tmp_length = []
            for _ in range(self.ants):
                index = self.__create_index(dm, matrix_pheromone)
                tmp_index.append(index)
                tmp_length.append(ACO.__calculate_distance(dm, index))
            self.update_matrix_pheromone(matrix_pheromone, tmp_index, tmp_length)
            best_length = min(tmp_length)
            if best_length < res_length:
                res_length = best_length
                res_index = tmp_index[tmp_length.index(best_length)]

        return Path(self.__shift(res_index), res_length)


def open_file(file):
    print('Open file')
    tmp_points = []

    with open(file, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            if line == '':
                continue

            latitude, longitude = line.split(',')
            tmp_points.append((float(latitude), float(longitude)))

    return tmp_points


def save_file(path):
    print('Save file')
    open('output.txt', 'w', encoding='utf8')
    with open('output.txt', 'a') as f:
        f.write('Медведев Илья Валерьевич\n')
        f.write(f'{str(round(path.length))}\n')
        index = ''
        for i in path.index:
            index += f'{i},'
        f.write(index[:-1])


if __name__ == "__main__":
    print('Begin')
    start = time()

    count = 5
    points = open_file('input.txt')
    _ants = len(points)
    _iteration = round(100 + (_ants * 0.2))

    aco = ACO(ants=_ants, iteration=_iteration, a=1.5, b=1.2, p=0.6, q=10)
    paths = []

    for i in range(count):
        print(f'Run №{str(i + 1)}')
        paths.append(aco.run(points=points))
        print(f'  {paths[len(paths)-1].length}')
        print(f'  {paths[len(paths) - 1].index}')

    path = paths[0]
    for i in range(1, len(paths)):
        if paths[i].length < path.length:
            path = paths[i]

    print('Choice')
    print(f'  {path.length}')
    print(f'  {path.index}')

    save_file(path)
    print(f'Time spent {str(time() - start)} sec.')
    print('End')





