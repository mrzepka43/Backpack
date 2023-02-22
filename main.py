import time
import math
import random
import sys
import threading


################### Algorytm brute-force ###############
def w(x, data):
    size = 0
    for i in range(len(x)):
        if x[i] == '1':
            size += int(data[i][0])
    return size


def f(x, data):
    worth = 0
    for i in range(len(x)):
        if x[i] == '1':
            worth += int(data[i][1])
    return worth


def brute_force(file):
    source = open(file)
    liczba_przedmiotow, pojemnosc = source.readline().split()
    liczba_przedmiotow = int(liczba_przedmiotow)
    data = []
    for i in range(liczba_przedmiotow):
        data.append(())
    for i in range(liczba_przedmiotow):
        a = source.readline().split()
        data[i] = a
    pojemnosc = int(pojemnosc)
    fmax = 0
    bin_fmax = ''
    size_chosen = 0
    for i in range(1, 2 ** liczba_przedmiotow):
        bin_num = bin(i)
        bin_num = bin_num[len(bin_num):1:-1]
        size = w(bin_num, data)
        if size <= pojemnosc:
            worth = f(bin_num, data)
            if worth > fmax:
                fmax = worth
                bin_fmax = bin_num
                size_chosen = size

    print("Rzeczy włozone do plecaka:")
    print(bin_fmax)
    print("Maksymalna wartosc rzeczy włożonych do plecaka:")
    print(fmax)
    print("Waga tych rzeczy:")
    print(size_chosen)


################### Algorytm zachlanny ###############
def az(file):
    source = open(file)
    liczba_przedmiotow, pojemnosc = source.readline().split()
    liczba_przedmiotow = int(liczba_przedmiotow)
    data = []
    for i in range(liczba_przedmiotow):
        data.append([])
    for i in range(liczba_przedmiotow):
        a = source.readline().split()
        data[i] = a
    pojemnosc = int(pojemnosc)

    # obliczanie wartosci na jednostke masy i dopisywanie indeksu
    for i in range(liczba_przedmiotow):
        value = int(data[i][1]) / int(data[i][0])
        value = str(value)
        data[i].append(value)
        data[i].append(str(i))
        for j in range(4):
            data[i][j] = float(data[i][j])

    res = []
    for i in range(liczba_przedmiotow):
        res.append(0)

    data = sorted(data, key=lambda x: x[2], reverse=True)
    # print(data)

    nr_item = 0
    size_used = 0
    value_in_backpack = 0
    weight = 0
    while size_used < pojemnosc and nr_item < liczba_przedmiotow:
        if size_used + float(data[nr_item][0]) <= pojemnosc:
            item_id = int(data[nr_item][3])
            size_used += float(data[nr_item][0])
            res[item_id] = 1
            value_in_backpack += data[nr_item][1]
            weight += data[nr_item][0]

        nr_item += 1

    print("Rzeczy włozone do plecaka:")
    print(res)
    print("Maksymalna wartosc rzeczy włożonych do plecaka:")
    print(value_in_backpack)
    print("Waga tych rzeczy:")
    print(weight)


################### Algorytm dynamiczny ##############
def ad(file):
    source = open(file)
    liczba_przedmiotow, pojemnosc = source.readline().split()
    liczba_przedmiotow = int(liczba_przedmiotow)
    pojemnosc = int(pojemnosc)
    data = []
    for i in range(liczba_przedmiotow + 1):
        data.append([])

    data[0].append(str(liczba_przedmiotow))
    data[0].append(str(pojemnosc))

    for i in range(1, liczba_przedmiotow + 1):
        a = source.readline().split()
        data[i] = a

    PD_matrix = []

    # tworzenie macierzy wynikowej
    for i in range(liczba_przedmiotow + 1):
        PD_matrix.append([])
        for j in range(pojemnosc + 1):
            PD_matrix[i].append(0)
    for i in range(1, liczba_przedmiotow + 1):
        for j in range(1, pojemnosc + 1):
            if int(data[i][0]) > j:
                PD_matrix[i][j] = PD_matrix[i-1][j]
            else:
                PD_matrix[i][j] = max(PD_matrix[i-1][j], PD_matrix[i - 1][j-int(data[i][0])] + int(data[i][1]))

    fmax = PD_matrix[liczba_przedmiotow][pojemnosc]
    res = []
    weight = 0
    while liczba_przedmiotow > 0:
        if PD_matrix[liczba_przedmiotow][pojemnosc] > PD_matrix[liczba_przedmiotow - 1][pojemnosc]:
            res.append(liczba_przedmiotow)
            pojemnosc -= int(data[liczba_przedmiotow][0])
            weight += int(data[liczba_przedmiotow][0])
        liczba_przedmiotow -= 1

    print("Rzeczy włozone do plecaka:")
    print(res)
    print("Maksymalna wartosc rzeczy włożonych do plecaka:")
    print(fmax)
    print("Waga tych rzeczy:")
    print(weight)

################### Generowanie Plecaka ##############


def generate_backpack(filename, items_quantity, maxcapacity):
    file = open(filename, 'w')
    file.write(str(items_quantity) + ' ' + str(maxcapacity) + '\n')

    for i in range(items_quantity):
        r = random.randint(1, maxcapacity)
        v = random.randint(1, 100)
        file.write(str(r) + ' ' + str(v) + '\n')

    file.close()

################### Testy ############################

# Brute force
items = 40000
capacity =[100, 200, 300, 400, 500, 1000, 2000, 3000, 4000, 5000]

for i in capacity:
    print(i)
    generate_backpack('plecak.txt', items, i)
    file = open('wyniki_pojemnosc_dynamiczny.txt', 'a')

    start = time.time()
    ad('plecak.txt')
    stop = time.time()
    result = stop - start

    file.write(str(i) + ' ' + str(result) + '\n')







