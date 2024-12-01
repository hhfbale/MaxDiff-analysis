import pandas as pd

def calculate_maxdiff_scores(row):
    """
    Calculate MaxDiff scores using best-worst counting method.
    Returns a dictionary with the scores for each attribute.
    """
    attributes = [
        "Informasjon og rådgivning",
        "Farmasøytassistent",
        "Lagerstyring",
        "Optimal medisinering",
        "Språkstøtte"
    ]
    
    # Initialize counters for each attribute
    best_counts = {attr: 0 for attr in attributes}
    worst_counts = {attr: 0 for attr in attributes}
    
    # Count best and worst selections across all 10 sets
    for i in range(1, 11):
        best_col = f'Rangering nr. {i}: Velg den MEST viktige modulen'
        worst_col = f'Rangering nr. {i}: Velg den MINST viktige modulen'
        
        best_choice = row[best_col]
        worst_choice = row[worst_col]
        
        best_counts[best_choice] += 1
        worst_counts[worst_choice] += 1
    
    # Calculate total scores (best - worst)
    scores = {}
    for attr in attributes:
        scores[attr] = {
            'Best': best_counts[attr],
            'Worst': worst_counts[attr],
            'Total': best_counts[attr] - worst_counts[attr]
        }
    
    return scores
