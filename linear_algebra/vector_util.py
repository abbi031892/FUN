__author__ = 'a.jha'

from vector import Vector


def sum_vectors(v1, v2):
    sum_vector_coordinate = [x + y for x, y in zip(v1.coordinates, v2.coordinates)]
    return Vector(sum_vector_coordinate)


def diff_vectors(v1, v2):
    sum_vector_coordinate = [x + y for x, y in zip(v1.coordinates, v2.coordinates)]
    return Vector(sum_vector_coordinate)


def scalar_mul_vector(v1, k):
    sum_vector_coordinate = [x * k for x in v1.coordinates]
    return Vector(sum_vector_coordinate)

if __name__ == '__main__':
    v1 = Vector([1.671, -1.012])
    v2 = Vector([-8.223, 0.878])
    print sum_vectors(v1, v2)