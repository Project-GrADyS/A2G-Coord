import pandas as pd
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt

def compute_poi_percentage(row, threshold):
    time_poi = row['time_poi']
    threshold = threshold * time_poi
    poi_cols = [col for col in row.index if col.startswith("poi")]
    poi_values = row[poi_cols].astype(float)
    satisfied = (poi_values >= threshold).sum()
    return (satisfied / len(poi_cols)) * 100

conjuntos = {
    "BA": "experiments/experiment_fusion/algorithm_v1/data/",
    "GA": "experiments/experiment_fusion/algorithm_v2/data/",
    "LBA": "experiments/experiment_fusion/algorithm_v3/data/"
}

# Lista para coletar os dados de todos os conjuntos
all_data = []

for set_name, folder_path in conjuntos.items():
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        
        for _, row in df.iterrows():
            percentage = compute_poi_percentage(row, 0.5)
            all_data.append({
                "algorithm": set_name,
                "uav_num": int(row["uav_num"]),
                "ugv_num": int(row["ugv_num"]),
                "poi_num": int(row["poi_num"]),
                "comm_range": int(row["comm_range"]),
                "percentage_pois": percentage,
                "source_file": os.path.basename(csv_file)
            })

df_all = pd.DataFrame(all_data)

sns.boxplot(x="comm_range", y="percentage_pois", hue="algorithm", data=df_all, palette='crest', showfliers = False)
plt.xlabel("Communication Range")
plt.ylabel("Percentage of POIs found in 50% of time")
plt.savefig(f"experiments/experiment_fusion/metrics/individual_time/experiment_fusion_poi_boxplot_range_time.png")
plt.clf()

sns.boxplot(x="uav_num", y="percentage_pois", hue="algorithm", data=df_all, palette='crest', showfliers = False)
plt.xlabel("Number of UAVs")
plt.ylabel("Percentage of POIs found in 50% of time")
plt.savefig(f"experiments/experiment_fusion/metrics/individual_time/experiment_fusion_poi_boxplot_uav_time.png")
plt.clf()

sns.boxplot(x="ugv_num", y="percentage_pois", hue="algorithm", data=df_all, palette='crest', showfliers = False)
plt.xlabel("Number of UGVs")
plt.ylabel("Percentage of POIs found in 50% of time")
plt.savefig(f"experiments/experiment_fusion/metrics/individual_time/experiment_fusion_poi_boxplot_ugv_time.png")
plt.clf()

sns.boxplot(x="poi_num", y="percentage_pois", hue="algorithm", data=df_all, palette='crest', showfliers = False)
plt.xlabel("Number of POIs")
plt.ylabel("Percentage of POIs found in 50% of time")
plt.savefig(f"experiments/experiment_fusion/metrics/individual_time/experiment_fusion_poi_boxplot_poi_time.png")
plt.clf()