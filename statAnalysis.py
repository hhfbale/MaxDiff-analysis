import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations,combinations_with_replacement

def extract_attribute_scores(respondents, attribute):
    """
    Extract scores for a specific attribute across all respondents.
    """
    return [resp.maxdiff[attribute]['Total'] for resp in respondents]

def perform_normality_tests(respondents, attributes):
    """
    Perform Shapiro-Wilk normality test on the distribution of scores for each attribute.
    """
    
    results = []
    
    for attr in attributes:
        scores = extract_attribute_scores(respondents, attr)
        statistic, p_value = stats.shapiro(scores)
        
        results.append({
            'Attribute': attr,
            'Shapiro_Statistic': statistic,
            'P_Value': p_value,
            'Is_Normal': p_value > 0.05,  # Common threshold for normality
            'Mean': np.mean(scores),
            'Std': np.std(scores),
            'n': len(scores)
        })
    
    return pd.DataFrame(results)


def print_normality_summary(results_df):
    """
    Print a readable summary of the normality test results.
    """
    print("\nNormality Test Results Summary:")
    print("-" * 80)
    
    for _, row in results_df.iterrows():
        print(f"\nAttribute: {row['Attribute']}")
        print(f"Mean Score: {row['Mean']:.2f} (SD: {row['Std']:.2f})")
        print(f"Sample Size: {row['n']}")
        print(f"Shapiro-Wilk Statistic: {row['Shapiro_Statistic']:.4f}")
        print(f"P-Value: {row['P_Value']:.4f}")
        
        if row['Is_Normal']:
            conclusion = "✓ Distribution appears normal (p > 0.05)"
        else:
            conclusion = "✗ Distribution appears non-normal (p ≤ 0.05)"
        print(f"Conclusion: {conclusion}")


def analyze_maxdiff_small_sample(respondents, attributes):
    """
    Perform statistical analysis appropriate for small sample MaxDiff data
    """
    print("MaxDiff Analysis for Small Sample (n=7)")
    print("-" * 50)
    
    # Create dictionary of scores for each attribute
    scores_dict = {attr: extract_attribute_scores(respondents, attr) for attr in attributes}
    
    # 1. Basic descriptive statistics
    print("\n1. Descriptive Statistics:")
    print("-" * 30)
    desc_stats = pd.DataFrame({
        attr: {
            'Mean': np.mean(scores),
            'Median': np.median(scores),
            'Std Dev': np.std(scores),
            'Min': np.min(scores),
            'Max': np.max(scores),
            'IQR': np.percentile(scores, 75) - np.percentile(scores, 25)
        }
        for attr, scores in scores_dict.items()
    }).round(2)
    print(desc_stats)
    
    # 2. Friedman test for overall differences
    print("\n2. Friedman Test (Overall Comparison):")
    print("-" * 30)
    # Prepare data for Friedman test
    friedman_data = pd.DataFrame({attr: scores_dict[attr] for attr in attributes})
    statistic, p_value = stats.friedmanchisquare(*[scores_dict[attr] for attr in attributes])
    print(f"Friedman test statistic: {statistic:.4f}")
    print(f"p-value: {p_value:.4f}")
    if p_value < 0.05:
        print("Significant differences found between attributes (p < 0.05)")
    else:
        print("No significant differences found between attributes (p >= 0.05)")
    
    # 3. Pairwise Wilcoxon signed-rank tests
    print("\n3. Pairwise Wilcoxon Signed-rank Tests:")
    print("-" * 30)
    print("(Note: With small sample size, these should be interpreted cautiously)")
    
    pairs = list(combinations(attributes, 2))
    wilcoxon_results = []
    
    for attr1, attr2 in pairs:
        statistic, p_value = stats.wilcoxon(scores_dict[attr1], 
                                          scores_dict[attr2],
                                          alternative='two-sided')
        effect_size = statistic / (len(scores_dict[attr1]) * (len(scores_dict[attr1]) + 1) / 2)
        wilcoxon_results.append({
            'Pair': f"{attr1} vs {attr2}",
            'Statistic': statistic,
            'P-value': p_value,
            'Effect Size': effect_size,
            'Mean Diff': np.mean(scores_dict[attr1]) - np.mean(scores_dict[attr2])
        })
    
    wilcoxon_df = pd.DataFrame(wilcoxon_results)
    print(wilcoxon_df.round(4))
    
    # 4. Spearman correlations
    print("\n4. Spearman Correlations:")
    print("-" * 30)
    print("(Note: Correlations with n=7 are very unstable)")
    
    corr_matrix = pd.DataFrame(index=attributes, columns=attributes)
    for attr1, attr2 in combinations_with_replacement(attributes, 2):
        corr, p_value = stats.spearmanr(scores_dict[attr1], scores_dict[attr2])
        corr_matrix.loc[attr1, attr2] = f"{corr:.2f} (p={p_value:.3f})"
        corr_matrix.loc[attr2, attr1] = f"{corr:.2f} (p={p_value:.3f})"
    
    print(corr_matrix)
    
    # 5. Additional considerations
    print("\n5. Important Considerations:")
    print("-" * 30)
    print("- Small sample size (n=7) means all statistical tests have low power")
    print("- P-values should be interpreted very cautiously")
    print("- Effect sizes and descriptive statistics may be more informative")
    print("- Visual inspection of the data is recommended")
    
    return {
        'descriptive_stats': desc_stats,
        'friedman_results': (statistic, p_value),
        'wilcoxon_results': wilcoxon_df,
        'correlation_matrix': corr_matrix
    }

def dagostino_z_skewness(b1, n):
    a = b1*np.sqrt(((n + 1)*(n + 2))/(6*(n - 2)))
    b = (3*(n**2 + 27*n - 70)*(n + 1)*(n + 3))/((n - 2)*(n + 5)*(n + 7)*(n + 9))
    c = np.sqrt(2*(b - 1))-1
    d = np.sqrt(c)
    e = 1/(np.sqrt(np.log(d)))
    f = a/(np.sqrt(2/(c - 1)))
    
    z = e*np.log(f + np.sqrt(f**2 + 1))
    return z


def test_skewness_kurtosis(data, attribute_name=None):
    """
    Calculate and test skewness and kurtosis for a single sample.
    """
    n = len(data)
    
    # Calculate skewness and kurtosis
    skewness = stats.skew(data)
    kurtosis = stats.kurtosis(data) 
    
    # Standard error calculations
    # These are approximations and may not be reliable for small samples
    se_skewness = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
    se_kurtosis = np.sqrt(24 * n * (n - 1) ** 2 / ((n - 3) * (n - 2) * (n + 3) * (n + 5)))
    
    # Calculate test statistics
    z_skew = dagostino_z_skewness(skewness,n)
    print(f'dagostino z: {z_skew}')
    z_skewness = skewness / se_skewness if se_skewness != 0 else 0
    print(f'simplified z: {z_skewness}')
    z_kurtosis = kurtosis / se_kurtosis if se_kurtosis != 0 else 0
    
    # P-values (two-tailed test)
    p_skewness = 2 * (1 - stats.norm.cdf(abs(z_skewness)))
    p_kurtosis = 2 * (1 - stats.norm.cdf(abs(z_kurtosis)))
    
    
    results = {
        'n_samples': n,
        'skewness': {
            'value': skewness,
            'se': se_skewness,
            'z_score': z_skewness,
            'p_value': p_skewness
        },
        'kurtosis': {
            'value': kurtosis,
            'se': se_kurtosis,
            'z_score': z_kurtosis,
            'p_value': p_kurtosis
        }
    }
    
    # Print results with appropriate warnings
    if attribute_name:
        print(f"\nNormality Analysis for {attribute_name}")
        print("-" * 50)
    
    
    print("\nSkewness Analysis:")
    print(f"Value: {skewness:.3f} (SE: {se_skewness:.3f})")
    print(f"Z-score: {z_skewness:.3f} (p-value: {p_skewness:.3f})")
    
    print("\nKurtosis Analysis:")
    print(f"Value: {kurtosis:.3f} (SE: {se_kurtosis:.3f})")
    print(f"Z-score: {z_kurtosis:.3f} (p-value: {p_kurtosis:.3f})")
    
    return results

def analyze_distributions(respondents, attributes):
    """
    Analyze distributions for all attributes in the MaxDiff study
    """
    print("Distribution Analysis for MaxDiff Scores")
    print("=" * 50)
    
    results = {}
    
    for attr in attributes:
        scores = extract_attribute_scores(respondents, attr)
        results[attr] = test_skewness_kurtosis(scores, attr)
        print("\n" + "=" * 50)
    
    # Visual summary
    summary_df = pd.DataFrame({
        attr: {
            'Skewness': results[attr]['skewness']['value'],
            'Kurtosis': results[attr]['kurtosis']['value'],
        }
        for attr in attributes
    }).round(3)
    
    print("\nSummary Table:")
    print(summary_df)
    
    return results

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
        # Load data
        respondents = load_survey_data()
        
        # Perform normality tests
        #results = perform_normality_tests(respondents,attributes)
        results = analyze_distributions(respondents,attributes)
        
        # Print summary
        #print_normality_summary(results)
            

        # Create and show distribution plots
        #plot_distributions(respondents, attributes)
        #plt.show()
        
        # Print detailed results table
        # print("\nDetailed Results Table:")
        # print(results.to_string(index=False))
        
    except Exception as e:
        print(f"Error: {e}")