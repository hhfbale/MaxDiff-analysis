import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from combineCSV import combine_csv_files
from maxdiff_analysis import calculate_maxdiff_scores
import plotter

class Respondent:
    def __init__(self, age, academic, role, experience, location, maxdiff, comment, currentRankings):
        self.age = age
        self.academic = academic
        self.role = role
        self.experience = experience
        self.location = location
        self.maxdiff = maxdiff  # Will now be a dictionary with 'Best', 'Worst', and 'Total' counts
        self.comment = comment
        self.currentRankings = currentRankings
    
    def __str__(self):
        return f"Respondent(age={self.age}, role={self.role}, location={self.location})"
    

def load_survey_data(csv_folder='CSVs', combined_filename='combined_output.csv'):
    combined_filepath = os.path.join(csv_folder, combined_filename)
    
    if not os.path.exists(combined_filepath):
        print(f"Combined CSV file not found at {combined_filepath}")
        print("Creating combined CSV file...")
        combine_csv_files(csv_folder, combined_filename)
        if not os.path.exists(combined_filepath):
            raise FileNotFoundError(f"Failed to create combined CSV file at {combined_filepath}")
        print("Combined CSV file created successfully.")
    
    return parse_survey_data(combined_filepath)


def parse_survey_data(file_path):
    try:
        df = pd.read_csv(file_path, sep=',')
    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")
    
    respondents = []
    
    for _, row in df.iterrows():
        try:
            maxdiff_scores = calculate_maxdiff_scores(row)
            current_rankings = get_current_rankings(row)
            
            respondent = Respondent(
                age=int(row['Hva er din alder?']),
                academic=int(row['Hvor mange års utdannelse har du utenom videregående skole?']),
                role=row['Hva er din rolle i apoteket?'],
                experience=int(row['Hvor mange års erfaring har du i din nåværende rolle?']),
                location=row['Hvor er du ansatt?'],
                maxdiff=maxdiff_scores,
                comment=row['Hvilket av de foreslåtte verktøyene skilte seg mest ut og hvorfor?'],
                currentRankings=current_rankings
            )
            
            respondents.append(respondent)
        except Exception as e:
            print(f"Warning: Skipping row due to error: {e}")
            continue
    
    return respondents


# Rest of the code remains the same...
def get_current_rankings(row):
    ranking_cols = [
        'Jeg er svært fornøyd med nåværende, digitale verktøy',
        'Jeg er svært fornøyd med DESIGNET i nåværende, digitale verktøy',
        'Jeg er svært fornøyd med SAMHANDLINGEN MED ANDRE VERKTØY i nåværende, digitale verktøy',
        'Jeg er svært fornøyd med BRUKERVENNLIGHETEN i nåværende, digitale verktøy',
        'Jeg er svært fornøyd med LÆRINGSKURVEN i nåværende, digitale verktøy',
        'Jeg er svært fornøyd med EFFEKTIVITETEN i nåværende, digitale verktøy',
        'Jeg er svært fornøyd med PÅLITELIGHETEN i nåværende, digitale verktøy',
        'Jeg er svært fornøyd med BRUKERSTØTTEN i nåværende, digitale verktøy',
        'Jeg er svært fornøyd med DATASIKKERHETEN i nåværende, digitale verktøy'
    ]
    
    return {col.split('med ')[-1].split(' i')[0].lower(): int(row[col]) 
            for col in ranking_cols}
# Example usage:
if __name__ == "__main__":
    try:
        respondents = load_survey_data()
        print(f"Successfully loaded {len(respondents)} survey responses")
        
        # Example: Print first respondent's data and plot their scores
        # if respondents:
        #     print("\nFirst respondent details:")
        #     print(f"Age: {respondents[0].age}")
        #     print(f"Role: {respondents[0].role}")
        #     print(f"MaxDiff scores: {respondents[0].maxdiff}")
        #     print(f"Current rankings: {respondents[0].currentRankings}")
            
        #     # Plot individual scores
        #     plotter.plot_respondent_scores(respondents[0])
        #     plt.show()
            
        #     # Plot aggregate scores
        #     plotter.plot_aggregate_scores(respondents)
        #     plt.show()

        #     # Detailed individual plot
        #     plotter.plot_maxdiff_detailed(respondents[0])
        #     plt.show()
        
    except Exception as e:
        print(f"Error: {e}")