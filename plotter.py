import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statAnalysis import extract_attribute_scores

def plot_respondent_scores(respondent):
    """
    Create a styled bar plot of a single respondent's MaxDiff scores
    """
    # Prepare the data
    scores = pd.DataFrame.from_dict(
        {k: v['Total'] for k, v in respondent.maxdiff.items()}, 
        orient='index',
        columns=['Score']
    )
    
    # Sort values for better visualization
    scores = scores.sort_values('Score', ascending=True)
    
    # Set style
    plt.style.use('classic')  # Using classic style instead of seaborn
    
    # Create figure with white background
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Create bars
    colors = plt.cm.RdYlBu(np.linspace(0, 1, len(scores)))
    bars = ax.barh(range(len(scores)), scores['Score'], color=colors)
    
    # Set y-tick labels
    ax.set_yticks(range(len(scores)))
    ax.set_yticklabels(scores.index)
    
    # Customize the plot
    ax.set_title('Individual MaxDiff Attribute Importance', 
                pad=20, 
                fontsize=14, 
                fontweight='bold')
    ax.set_xlabel('Importance Score (Best - Worst)', 
                 fontsize=12, 
                 fontweight='bold')
    ax.set_ylabel('Attributes', 
                 fontsize=12, 
                 fontweight='bold')
    
    # Add value labels on the bars
    for i, v in enumerate(scores['Score']):
        ax.text(v, i, f' {v:0.2f}', va='center')
    
    # Add a vertical line at x=0
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.2)
    
    # Add grid for better readability
    ax.grid(True, axis='x', alpha=0.3)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add respondent info in the title
    plt.suptitle(f'Respondent Profile: Age {respondent.age}, Role: {respondent.role}', 
                 fontsize=10, 
                 style='italic')
    
    plt.tight_layout()
    return fig

def plot_aggregate_scores(respondents):
    """
    Create a styled bar plot of aggregate MaxDiff scores across all respondents
    """
    # Aggregate scores across all respondents
    aggregate_scores = {
        "Informasjon og rådgivning": 0,
        "Farmasøytassistent": 0,
        "Lagerstyring": 0,
        "Optimal medisinering": 0,
        "Språkstøtte": 0
    }
    
    # Count total respondents for average calculation
    n_respondents = len(respondents)
    
    for respondent in respondents:
        for attr, scores in respondent.maxdiff.items():
            aggregate_scores[attr] += scores['Total']
    
    # Convert to average scores
    aggregate_scores = {k: v/n_respondents for k, v in aggregate_scores.items()}
    
    scores_df = pd.DataFrame.from_dict(
        aggregate_scores, 
        orient='index',
        columns=['Score']
    )
    
    # Sort values
    scores_df = scores_df.sort_values('Score', ascending=True)
    
    # Set style
    plt.style.use('classic')
    
    # Create figure with white background
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Create bars
    colors = plt.cm.RdYlBu(np.linspace(0, 1, len(scores_df)))
    bars = ax.barh(range(len(scores_df)), scores_df['Score'], color=colors)
    
    # Set y-tick labels
    ax.set_yticks(range(len(scores_df)))
    ax.set_yticklabels(scores_df.index)
    
    # Customize the plot
    ax.set_title('Aggregate MaxDiff Attribute Importance', 
                pad=20, 
                fontsize=14, 
                fontweight='bold')
    ax.set_xlabel('Average Importance Score (Best - Worst)', 
                 fontsize=12, 
                 fontweight='bold')
    ax.set_ylabel('Attributes', 
                 fontsize=12, 
                 fontweight='bold')
    
    # Add value labels on the bars
    for i, v in enumerate(scores_df['Score']):
        ax.text(v, i, f' {v:0.2f}', va='center')
    
    # Add a vertical line at x=0
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.2)
    
    # Add grid for better readability
    ax.grid(True, axis='x', alpha=0.3)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add sample size info in the title
    plt.suptitle(f'Based on {n_respondents} respondents', 
                 fontsize=10, 
                 style='italic')
    
    plt.tight_layout()
    return fig

def plot_maxdiff_detailed(respondent):
    """
    Create a detailed plot showing Best, Worst, and Total scores for each attribute
    """
    # Prepare the data
    data = []
    for attr, scores in respondent.maxdiff.items():
        data.extend([
            {'Attribute': attr, 'Type': 'Best', 'Count': scores['Best']},
            {'Attribute': attr, 'Type': 'Worst', 'Count': -scores['Worst']},  # Negative for visualization
        ])
    
    df = pd.DataFrame(data)
    
    # Sort by total score
    total_scores = {k: v['Total'] for k, v in respondent.maxdiff.items()}
    sorted_attrs = sorted(total_scores.items(), key=lambda x: x[1])
    attr_order = [x[0] for x in sorted_attrs]
    
    # Set style
    plt.style.use('classic')
    
    # Create figure with white background
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Create grouped bars
    bar_width = 0.35
    y_pos = np.arange(len(attr_order))
    
    best_data = [respondent.maxdiff[attr]['Best'] for attr in attr_order]
    worst_data = [-respondent.maxdiff[attr]['Worst'] for attr in attr_order]
    
    ax.barh(y_pos - bar_width/2, best_data, bar_width, label='Best', color='#2ecc71')
    ax.barh(y_pos + bar_width/2, worst_data, bar_width, label='Worst', color='#e74c3c')
    
    # Customize the plot
    ax.set_yticks(y_pos)
    ax.set_yticklabels(attr_order)
    
    ax.set_title('Detailed MaxDiff Scores by Attribute', 
                pad=20, 
                fontsize=14, 
                fontweight='bold')
    ax.set_xlabel('Count', 
                 fontsize=12, 
                 fontweight='bold')
    ax.set_ylabel('Attributes', 
                 fontsize=12, 
                 fontweight='bold')
    
    # Add value labels
    for i, v in enumerate(best_data):
        ax.text(v, i - bar_width/2, f' {v:0.0f}', va='center')
    for i, v in enumerate(worst_data):
        ax.text(v, i + bar_width/2, f' {v:0.0f}', va='center')
    
    # Add a vertical line at x=0
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.2)
    
    # Add grid for better readability
    ax.grid(True, axis='x', alpha=0.3)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Customize legend
    ax.legend(title='Selection Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add respondent info in the title
    plt.suptitle(f'Respondent Profile: Age {respondent.age}, Role: {respondent.role}', 
                 fontsize=10, 
                 style='italic')
    
    plt.tight_layout()
    return fig

def plot_distributions(respondents,attributes):
    """
    Create visualization of MaxDiff score distributions,
    optimized for discrete values between -6 and +6
    """
    
    # Create subplot grid
    fig, axes = plt.subplots(len(attributes), 1, figsize=(12, 3*len(attributes)))
    plt.style.use('classic')
    
    for i, attr in enumerate(attributes):
        ax = axes[i]
        scores = extract_attribute_scores(respondents, attr)
        
        # Count occurrences of each score
        score_counts = pd.Series(scores).value_counts().sort_index()
        
        # Create bar plot
        bars = ax.bar(score_counts.index, score_counts.values,
                     color=['#e74c3c' if x < 0 else '#2ecc71' if x > 0 else '#3498db' for x in score_counts.index],
                     edgecolor='black')
        
        # Set fixed x-axis limits and ticks
        ax.set_xlim(-7, 7)
        ax.set_xticks(range(-6, 7))
        
        # Add mean and median lines
        mean_val = np.mean(scores)
        median_val = np.median(scores)
        ax.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='blue', linestyle='--', label=f'Median: {median_val:.2f}')
        
        # Add zero line
        ax.axvline(0, color='black', linestyle='-', alpha=0.2)
        
        # Add count labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'n={int(height)}',
                   ha='center', va='bottom')
        
        # Add statistical information
        stats_text = (
            f'n = {len(scores)}\n'
            f'Mean = {mean_val:.2f}\n'
            f'Median = {median_val:.2f}\n'
            f'Std Dev = {np.std(scores):.2f}'
        )
        
        ax.text(0.02, 0.95, stats_text,
                transform=ax.transAxes, 
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Customize plot
        ax.set_title(f'Distribution of Scores: {attr}', pad=20, fontsize=12, fontweight='bold')
        ax.set_xlabel('MaxDiff Score (Best - Worst)')
        ax.set_ylabel('Number of Respondents')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
    plt.tight_layout()
    return fig