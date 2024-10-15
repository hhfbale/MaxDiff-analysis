import csv as csv
import pandas as pd
import numpy as np

attr = ["informasjon og rådgivning", "farmasøytassistent", "lagerstyring", "optimal medisinering", "språkstøtte"]

def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    return data

def get_start_index(data):
    for i in range(len(data[0])):
        if data[0][i] == "Sett 1: Evaluer følgende moduler":
            return i
        
def get_end_index(data):
    for i in range(len(data[0])):
        if data[0][i] == "Sett 10: Evaluer følgende moduler":
            return i
        
# def sum_maxdiff(data):
#     start_index = get_start_index(data)
#     end_index = get_end_index(data)
#     for i in range(start_index, end_index):
#         print(data[i])
        
