import sys
import os
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import json

my_path = os.path.dirname(os.path.abspath(__file__))
folder_path = "experiments"
csv_prefix = "experiment_fusion"
algorithms = ["v1", "v2", "v3"]
column_name = "time_poi"

alg_df = []

for algorithm_version in algorithms:
    dataframes = []
    combined_df = []
    algorithm_path = f'{my_path}/{folder_path}/{csv_prefix}/algorithm_{algorithm_version}'
    i = 0
    for file_name in os.listdir(algorithm_path + '/data'):
        if file_name.startswith(csv_prefix) and file_name.endswith('.csv'):
            file_path = os.path.join(algorithm_path + '/data', file_name)
            df = pd.read_csv(file_path)
            #df_filtered = df[df[column_name] != -1]
            df_filtered = df[~df.eq(-1).any(axis=1)]
            if not df_filtered.empty:
                df_filtered = df_filtered.drop(columns="experiment")
                poi_columns = [col for col in df.columns if col.startswith("poi") and col != 'poi_num']
                for poi in poi_columns:
                    df_filtered[f'{poi}_time_ratio'] = df_filtered[poi] / df_filtered['time_poi'] * 100
                    
                    df_filtered[f'{poi}_time_ratio_category'] = pd.cut(df_filtered[f'{poi}_time_ratio'], 
                                                                    bins=[0, 20, 40, 80, 100], 
                                                                    labels=["0-20", "21-40", "41-80", "81-100"], 
                                                                    right=True)
                    
                category_counts = pd.DataFrame(columns=["0-20", "21-40", "41-80", "81-100"])

                for index, row in df_filtered.iterrows():
                    counts = {category: 0 for category in category_counts.columns}
                    
                    for poi in poi_columns:
                        category = row[f'{poi}_time_ratio_category']
                        if category in counts:
                            counts[category] += 1
                    
                    total_pois = len(poi_columns)
                    for category in counts:
                        counts[category] = (counts[category] / total_pois) * 100
                    
                    category_counts.loc[index] = counts
                    #avg_counts = category_counts.mean()
                    #combined_results.loc[algorithm_version] = avg_counts
                combined_df.append(category_counts)
                category_counts_mean = category_counts.mean()
                first_row = df_filtered.iloc[0][['ugv_num', 'uav_num', 'poi_num', 'comm_range']]
                joined_df = pd.DataFrame([{**category_counts_mean, **first_row}])
                #print(joined_df)
                i += 1
            dataframes.append(joined_df)
    concat_df = pd.concat(dataframes, ignore_index=True)
    #print(concat_df)
    alg_df.append(concat_df)
    #dff = pd.DataFrame(category_counts
    #combined_df = pd.concat(category_counts, ignore_index=True)
    #print(combined_df)
    #summed_df = combined_df.groupby("category")["count"].sum().reset_index()
    #print(summed_df)
    #print(combined_df)
    # Append algorithm df to list
    
    #df_all = pd.concat(combined_df, axis=0, ignore_index=True)

path = f'{my_path}/{folder_path}/{csv_prefix}'

all_df = pd.concat({'BA': alg_df[0], 'GA': alg_df[1], 'LBA': alg_df[2]}, names=['algorithm', 'old_index'])
all_df = all_df.reset_index(level=0).reset_index(drop=True)


df_grouped = all_df.groupby(['ugv_num', 'algorithm']).mean().drop(columns=["uav_num", "poi_num", "comm_range"], errors="ignore")

# Plotando o gráfico
plt.figure(figsize=(10, 6))

print(df_grouped.columns)

# Criando o gráfico para cada UGV
for ugv_num in df_grouped['ugv_num'].unique():
    subset = df_grouped[df_grouped['ugv_num'] == ugv_num]
    for algorithm in subset['algorithm'].unique():
        # Seleciona os dados do algoritmo e plota
        subset_algo = subset[subset['algorithm'] == algorithm]
        plt.plot(subset_algo.columns[2:], subset_algo.iloc[0, 2:], label=f"UGV {ugv_num} - {algorithm}")

# Adicionando título e rótulos
plt.title("Desempenho dos Algoritmos por UGV e Intervalos")
plt.xlabel("Intervalos")
plt.ylabel("Valor")
plt.legend(title="Algoritmo e UGV")

# Exibindo o gráfico
plt.tight_layout()
plt.show()

'''
plt.figure(figsize=(8, 6))
sns.heatmap(all_df, annot=True, cmap="coolwarm", fmt=".2f")

plt.xlabel("Categorias")
plt.ylabel("Número de UGVs e Algoritmos")
plt.title("Mapa de Calor das Categorias por UGVs e Algoritmos")
'''
#plt.show()

'''
df_grouped = alg_df[0]
df_grouped = df_grouped.groupby("ugv_num").mean().drop(columns=["uav_num", "poi_num", "comm_range"], errors="ignore")

print(df_grouped)

# Criando o heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df_grouped, annot=True, cmap="coolwarm", fmt=".2f")

plt.xlabel("Categorias")
plt.ylabel("Número de UGVs")
plt.title("Mapa de Calor das Distribuições por Número de UGVs")

plt.show()

df_grouped1 = alg_df[1]
df_grouped1 = df_grouped1.groupby("ugv_num").mean().drop(columns=["uav_num", "poi_num", "comm_range"], errors="ignore")

print(df_grouped1)

# Criando o heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df_grouped1, annot=True, cmap="coolwarm", fmt=".2f")

plt.xlabel("Categorias")
plt.ylabel("Número de UGVs")
plt.title("Mapa de Calor das Distribuições por Número de UGVs")

plt.show()
'''

'''
# UGV Number
sns.boxplot(data=all_df, x='ugv_num', y='time_poi', hue='algorithm', palette='crest', showfliers = False)
plt.xlabel("Number of UGVs")
plt.ylabel("Time to find all PoI")
plt.savefig(f"{path}/{csv_prefix}_boxplot_ugv_time_poi.png")
plt.clf()

# UAV Number
sns.boxplot(data=all_df, x='uav_num', y='time_poi', hue='algorithm', palette='crest', showfliers = False)
plt.xlabel("Number of UAVs")
plt.ylabel("Time to find all PoI")
plt.savefig(f"{path}/{csv_prefix}_boxplot_uav_time_poi.png")
plt.clf()

# PoI Number
sns.boxplot(data=all_df, x='poi_num', y='time_poi', hue='algorithm', palette='crest', showfliers = False)
plt.xlabel("Number of PoIs")
plt.ylabel("Time to find all PoI")
plt.savefig(f"{path}/{csv_prefix}_boxplot_poi_time_poi.png")
plt.clf()

# Communication Range
sns.boxplot(data=all_df, x='comm_range', y='time_poi', hue='algorithm', palette='crest', showfliers = False)
plt.xlabel("Communication Range")
plt.ylabel("Time to find all PoI")
plt.savefig(f"{path}/{csv_prefix}_boxplot_range_time_poi.png")
plt.clf()
'''