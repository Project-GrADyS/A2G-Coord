import sys
import os
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import json

my_path = os.path.dirname(os.path.abspath(__file__))
folder_path = "experiments"
csv_prefix = sys.argv[1]
algorithms = json.loads(sys.argv[2])
column_name = "time_poi"

all_dataframes = []

for algorithm_version in algorithms:
    dataframes = []
    algorithm_path = f'{my_path}/{folder_path}/{csv_prefix}/algorithm_{algorithm_version}'
    for file_name in os.listdir(algorithm_path + '/data'):
        if file_name.startswith(csv_prefix) and file_name.endswith('.csv'):
            file_path = os.path.join(algorithm_path + '/data', file_name)
            df = pd.read_csv(file_path)
            df_filtered = df[[col for col in df.columns if not (col.startswith("poi") and col!= "poi_num")]].copy()
            df_filtered["algorithm"] = algorithm_version
            dataframes.append(df_filtered)

    combined_df = pd.concat(dataframes, ignore_index=True)
    all_dataframes.append(combined_df)

final_df = pd.concat(all_dataframes, ignore_index=True)

output_dir = os.path.join(my_path, folder_path, csv_prefix)
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, csv_prefix + '_combined.csv')
final_df.to_csv(output_path, index=False)