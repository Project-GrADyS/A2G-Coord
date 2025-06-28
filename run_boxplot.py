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

alg_df = []

for algorithm_version in algorithms:
    dataframes = []
    algorithm_path = f'{my_path}/{folder_path}/{csv_prefix}/algorithm_{algorithm_version}'
    for file_name in os.listdir(algorithm_path + '/data'):
        if file_name.startswith(csv_prefix) and file_name.endswith('.csv'):
            file_path = os.path.join(algorithm_path + '/data', file_name)
            df = pd.read_csv(file_path)
            df_filtered = df[[col for col in df.columns if not (col.startswith("poi") and col!= "poi_num")]]
            df_filtered = df_filtered[df_filtered[column_name] != -1]
            df_filtered = df_filtered.drop(columns="experiment")
            dataframes.append(df_filtered)

    combined_df = pd.concat(dataframes, ignore_index=True)
    print(combined_df)
    alg_df.append(combined_df)

path = f'{my_path}/{folder_path}/{csv_prefix}/metrics/boxplot_average_time'

#all_df = pd.concat({'BA': alg_df[0], 'GA': alg_df[1], 'LBA': alg_df[2]}, names=['algorithm', 'old_index'])
#all_df = pd.concat({'v7': alg_df[0]}, names=['algorithm', 'old_index'])
all_df = pd.concat({'GBA': alg_df[0], 'BSA': alg_df[1]}, names=['algorithm', 'old_index'])
all_df = all_df.reset_index(level=0).reset_index(drop=True)

# UGV Number
sns.boxplot(data=all_df, x='ugv_num', y='time_poi', hue='algorithm', palette='crest', showfliers = False)
plt.xlabel("Number of UGVs")
plt.ylabel("Time to find all POI")
plt.savefig(f"{path}/{csv_prefix}_boxplot_ugv_time.png")
plt.clf()

# UAV Number
sns.boxplot(data=all_df, x='uav_num', y='time_poi', hue='algorithm', palette='crest', showfliers = False)
plt.xlabel("Number of UAVs")
plt.ylabel("Time to find all POI")
plt.savefig(f"{path}/{csv_prefix}_boxplot_uav_time.png")
plt.clf()

# PoI Number
sns.boxplot(data=all_df, x='poi_num', y='time_poi', hue='algorithm', palette='crest', showfliers = False)
plt.xlabel("Number of PoIs")
plt.ylabel("Time to find all POI")
plt.savefig(f"{path}/{csv_prefix}_boxplot_poi_time.png")
plt.clf()

# Communication Range
sns.boxplot(data=all_df, x='comm_range', y='time_poi', hue='algorithm', palette='crest', showfliers = False)
plt.xlabel("Communication Range")
plt.ylabel("Time to find all POI")
plt.savefig(f"{path}/{csv_prefix}_boxplot_range_time.png")
plt.clf()

# Time Interval
sns.boxplot(data=all_df, x='time_interval', y='time_poi', hue='algorithm', palette='crest', showfliers = False)
plt.xlabel("Time Interval")
plt.ylabel("Time to find all POI")
plt.savefig(f"{path}/{csv_prefix}_boxplot_timeInterval_time.png")
plt.clf()

