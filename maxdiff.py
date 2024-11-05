import pandas as pd
import numpy as np
import itertools
import random
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

attributes = [
    "Informasjon og rådgivning",
    "Farmasøytassistent",
    "Lagerstyring",
    "Optimal medisinering",
    "Språkstøtte"
]

def generate_maxdiff_sets(attributes, num_sets=5, items_per_set=3):

    #Creates random maxdiff sets

    all_combinations = list(itertools.combinations(attributes, items_per_set)) #Creates all possible combinations of attributes
    maxdiff_sets = random.sample(all_combinations, num_sets) #Gives 5 random samples from all comvinations
    return maxdiff_sets

def generate_respondent_data(maxdiff_sets, num_respondents=20):

    #Simulate respondent data

    data = []
    for respondent in range(num_respondents):
        for set_num, attribute_set in enumerate(maxdiff_sets):
            best = random.choice(attribute_set)
            worst = random.choice([attr for attr in attribute_set if attr != best])
            data.append({"Respondent":respondent+1, "Set":set_num+1, "Best":best, "Worst":worst})
    return data


def calculate_importance_scores(respondent_data):
    #Calculation of importance score - lists need to be panda series to use value_counts

    best_counts = pd.Series([item['Best'] for item in respondent_data]).value_counts()
    worst_counts = pd.Series([item['Worst'] for item in respondent_data]).value_counts()

    best_worst_counts = pd.DataFrame({'Best':best_counts, 'Worst': worst_counts}).fillna(0)
    best_worst_counts['Total'] = best_worst_counts['Best'] - best_worst_counts['Worst']

    return best_worst_counts.sort_values(by='Total', ascending=False)

def plot_importance_scores(importance_scores):
    plt.figure(figsize=(10,6))
    sns.barplot(x=importance_scores.index, y=importance_scores['Total'], palette='viridis')
    plt.title('MaxDiff Attribute Importance')
    plt.xlabel('Attributes')
    plt.ylabel('Importance Score (Best - Worst)')
    plt.xticks(rotation=45)
    plt.show()

maxdiff_sets = generate_maxdiff_sets(attributes)
respondent_data = generate_respondent_data(maxdiff_sets)
importance_scores = calculate_importance_scores(respondent_data)

print(importance_scores)
plot_importance_scores(importance_scores)