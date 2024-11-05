import pandas as pd
import glob
import os

def combine_csv_files(directory_path = 'CSVs', output_filename='combined_output.csv'):
    """
    Combines all CSV files in the specified directory that have the same header structure.
    
    Parameters:
    directory_path (str): Path to the directory containing CSV files
    output_filename (str): Name of the output combined CSV file
    
    Returns:
    str: Path to the combined CSV file
    """
    # Get all CSV files in the directory
    all_files = glob.glob(os.path.join(directory_path, "*.csv"))
    
    if not all_files:
        raise ValueError(f"No CSV files found in {directory_path}")
    
    # Create a list to store all dataframes
    df_list = []
    
    # Read each CSV file and append to the list
    for file in all_files:
        try:
            df = pd.read_csv(file)
            df['source_file'] = os.path.basename(file)  # Add filename as a column
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")
    
    if not df_list:
        raise ValueError("No valid CSV files could be read")
    
    # Combine all dataframes
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Save the combined dataframe
    output_path = os.path.join(directory_path, output_filename)
    combined_df.to_csv(output_path, index=False)
    
    return output_path
 