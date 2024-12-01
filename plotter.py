import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import extractData

def pltHistogram(scores_df, attribute=None):

    if attribute is None:
        attribute = scores_df.columns[0]
    elif attribute not in scores_df.columns:
        raise ValueError(f"Attribute '{attribute}' not found in dataframe. Available attributes: {list(scores_df.columns)}")

    plt.figure(figsize=(10, 6))

    mean = scores_df[attribute].mean()
    median = np.round(scores_df[attribute].median())
    mode = scores_df[attribute].mode().iloc[0] 
    
    sns.histplot(
        data=scores_df[attribute],
        bins=range(-6,8),
        binrange=(-6,6),
        discrete = True,
        color='skyblue',
        edgecolor='black'
    )

    ax = plt.gca()
    y_min, y_max = ax.get_ylim()
    marker_y = y_min 
    y_buff = y_min - (y_max - y_min) * 0.05

    plt.plot(mean, marker_y, 'rv', markersize=10, label=f'Mean: {mean:.2f}')
    plt.plot(median, marker_y, 'g^', markersize=10, label=f'Median: {median:.2f}')
    plt.plot(mode, marker_y, 'D', markersize=10, label=f'Mode: {mode:.2f}')

    plt.legend(fontsize=16)
    
    plt.xlabel('MaxDiff Utility Score', fontsize=20)
    plt.ylabel('Count', fontsize=20)

    ax = plt.gca()
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.tick_params(axis='both', which='major', labelsize=16)

    plt.ylim(y_buff, y_max)
    
    return plt.gcf()

def pltBoxplot(scores_df):
    label_map = {
        "Informasjon og rådgivning": "Info & Advice",
        "Farmasøytassistent": "Pharm. Ass.",
        "Lagerstyring": "Invent. mgmt.",
        "Optimal medisinering": "Opt. med.",
        "Språkstøtte": "Lang. support"
    }

    plot_df = scores_df.copy()
    plot_df.columns = [label_map[col] for col in plot_df.columns]

    plt.figure(figsize=(12, 6))

    sns.boxplot(
        data=plot_df,
        color='skyblue',
        width=0.5,
        showfliers=True,
        medianprops={'color': 'black', 'linewidth': 2}
    )
    plt.ylabel('MaxDiff Score', fontsize=16)

    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=14)
    plt.xticks(rotation=0, ha='right')
    plt.tight_layout()
    
    return plt.gcf()

def pltBoxplotCurrentRankings(respondents):

    rankings_data = []
    for resp in respondents:
        rankings_data.append(resp.currentRankings)
    
    rankings_df = pd.DataFrame(rankings_data)

    label_map = {
        'nåværende, digitale verktøy': 'Current tools',
        'designet': 'Design',
        'samhandlingen med andre verktøy': 'Interaction',
        'brukervennligheten': 'Usability',
        'læringskurven': 'Learning Curve',
        'effektiviteten': 'Efficiency',
        'påliteligheten': 'Reliability',
        'brukerstøtten': 'User Support',
        'datasikkerheten': 'Data Security'
    }

    plot_df = rankings_df.copy()
    plot_df.columns = [label_map.get(col, col) for col in plot_df.columns]

    plt.figure(figsize=(14, 6))
    
    sns.boxplot(
        data=plot_df,
        color='lightgreen',
        width=0.5,
        showfliers=True,
        medianprops={'color': 'black', 'linewidth': 2}
    )

    plt.ylabel('Rating (0-10)', fontsize=16)
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=14)
    plt.xticks(rotation=45, ha='right') 
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    return plt.gcf()


if __name__ == "__main__":
    try:
        attributes = [
        "Informasjon og rådgivning",
        "Farmasøytassistent",
        "Lagerstyring",
        "Optimal medisinering",
        "Språkstøtte"
    ]
        respondents = extractData.load_survey_data()
        scores = extractData.attribute_scores()
    
    except Exception as e:
        print(f"Error: {e}")