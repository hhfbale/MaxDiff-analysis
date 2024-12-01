import numpy as np
from scipy import stats
import pandas as pd

def extract_attribute_scores(respondents, attribute):
    """
    Extract scores for a specific attribute across all respondents.
    """
    return [resp.maxdiff[attribute]['Total'] for resp in respondents]


def perform_normality_tests(respondents, attributes):
    """
    Perform multiple normality tests on the distribution of scores for each attribute.
    """
    
    results = []
    
    for attr in attributes:
        scores = extract_attribute_scores(respondents, attr)
        statistic, p_value = stats.shapiro(scores)
        
        results.append({
            'Attribute': attr,
            'Shapiro_Statistic': statistic,
            'P_Value': p_value,
            'Is_Normal': p_value > 0.1,
            'Mean': np.mean(scores),
            'Median': np.round(np.median(scores)),
            'Skewness': stats.skew(scores),
            'Kurtosis': stats.kurtosis(scores)
        })
    
    return pd.DataFrame(results)

# Example usage
if __name__ == "__main__":
    from extractData import load_survey_data
    attributes = [
        "Informasjon og rådgivning",
        "Farmasøytassistent",
        "Lagerstyring",
        "Optimal medisinering",
        "Språkstøtte"
    ]
    try:
        respondents = load_survey_data()
        print(perform_normality_tests(respondents, attributes))

    except Exception as e:
        print(f"Error: {e}")