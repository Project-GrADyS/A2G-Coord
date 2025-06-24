import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

f = "experiments/experiment_fusion/algorithm_v1/data/"

def compute_poi_percentage(df):
    results = []
    for idx, row in df.iterrows():
        time_poi = row['time_poi']
        threshold = 0.8 * time_poi
        poi_cols = [col for col in df.columns if col.startswith("poi") and col != 'poi_num']
        poi_values = row[poi_cols]
        satisfied = (poi_values >= threshold).sum()
        percentage = satisfied / len(poi_cols) * 100
        results.append(percentage)
    return results

# Carregar os CSVs
csv1 = pd.read_csv(f + "experiment_fusion_ugv8_uav1_poi5_range5.csv")
csv2 = pd.read_csv(f + "experiment_fusion_ugv4_uav1_poi5_range10.csv")
csv3 = pd.read_csv(f + "experiment_fusion_ugv8_uav1_poi15_range5.csv")

# Calcular porcentagem de POIs em >= 80% de time_poi
csv1_percent = compute_poi_percentage(csv1)
csv2_percent = compute_poi_percentage(csv2)
csv3_percent = compute_poi_percentage(csv3)

# Juntar em um DataFrame para o seaborn
data = pd.DataFrame({
    "CSV1": csv1_percent,
    "CSV2": csv2_percent,
    "CSV3": csv3_percent
})

# Transformar para formato longo
data_long = data.melt(var_name="CSV", value_name="% POIs >= 80% de time_poi")

# Plot
plt.figure(figsize=(8, 6))
sns.boxplot(x="CSV", y="% POIs >= 80% de time_poi", data=data_long)
sns.swarmplot(x="CSV", y="% POIs >= 80% de time_poi", data=data_long, color=".25")
plt.title("Comparação de Experimentos - POIs em >= 80% de time_poi")
plt.ylabel("Porcentagem de POIs")
plt.xlabel("Experimento (CSV)")
plt.grid(True)
plt.tight_layout()
plt.show()