import subprocess
import csv
import time
import json
from multiprocessing import Pool, cpu_count
from simulation_config.folder_config import create_folder

start_time = time.time()

num_experiments = 5

args = {
    "ugv_num": ["2", "4", "8"],
    "uav_num": ["2", "3"],
    "poi_num": ["5", "15", "25"],
    "communication_range": ["5", "10", "20"],
    "generate_graph": 0,
    "csv_path": "experiment_timeIntervalUAV",
    "map_size": "100",
    "time_interval": ["20", "100", "500"],
    "algorithms": ["v7"]
}

header = ['experiment', 'ugv_num', 'uav_num', 'poi_num', 'comm_range', 'time_interval','time_poi']

# Create experiment folder structure
folder_path = f'experiments/{args["csv_path"]}'
create_folder(folder_path)
create_folder(f'{folder_path}/metrics')
create_folder(f'{folder_path}/metrics/mean_time')
create_folder(f'{folder_path}/metrics/boxplot_average_time')
create_folder(f'{folder_path}/metrics/individual_time')

# Create folders for each algorithm
for algorithm_version in args["algorithms"]:
    create_folder(f'{folder_path}/algorithm_{algorithm_version}/analysis')
    create_folder(f'{folder_path}/algorithm_{algorithm_version}/data')
    create_folder(f'{folder_path}/algorithm_{algorithm_version}/images')

# Função que executa um experimento
def run_simulation(params):
    i, ugv_num, uav_num, poi_num, comm_range, file_name, csv_path, map_size, generate_graph, algorithms, time_interval = params
    subprocess.run([
        "pypy", "main.py",
        str(i + 1),
        ugv_num,
        uav_num,
        poi_num,
        comm_range,
        str(generate_graph),
        file_name,
        csv_path,
        map_size,
        json.dumps(algorithms),
        time_interval
    ])

# Gerar os arquivos CSV com cabeçalhos e montar lista de execuções
task_list = []
for time_interval in args["time_interval"]:
    for comm_range in args["communication_range"]:
        for uav_num in args["uav_num"]:
            for ugv_num in args["ugv_num"]:
                for poi_num in args["poi_num"]:
                    header_list = ['poi' + str(p+1) for p in range(int(poi_num))]
                    for algorithm_version in args["algorithms"]:
                        algorithm_path_data = f'{folder_path}/algorithm_{algorithm_version}/data'
                        file_name = f'{args["csv_path"]}_ugv{ugv_num}_uav{uav_num}_poi{poi_num}_range{comm_range}_timeInterval{time_interval}'
                        with open(f"{algorithm_path_data}/{file_name}.csv", 'w') as file:
                            dw = csv.DictWriter(file, fieldnames=header + header_list)
                            dw.writeheader()
                    for i in range(num_experiments):
                        file_name = f'{args["csv_path"]}_ugv{ugv_num}_uav{uav_num}_poi{poi_num}_range{comm_range}_timeInterval{time_interval}'
                        task_list.append((
                            i, ugv_num, uav_num, poi_num, comm_range,
                            file_name, args["csv_path"], args["map_size"],
                            args["generate_graph"], args["algorithms"], time_interval
                        ))

# Executar simulações em paralelo
with Pool(cpu_count()) as pool:
    pool.map(run_simulation, task_list)

#Join CSVs
subprocess.run(["pypy", "join_csvs.py", args["csv_path"], json.dumps(args["algorithms"])],)

# Gerar gráficos
subprocess.run(["pypy", "run_graphs.py", args["csv_path"], json.dumps(args["algorithms"])])
subprocess.run(["pypy", "run_boxplot.py", args["csv_path"], json.dumps(args["algorithms"])])

# Medir tempo
end_time = time.time()
total_time = end_time - start_time
h = total_time // 3600
m = (total_time % 3600) // 60
s = total_time % 60

print("\n")
print(f"Total simulation time: {h:.0f} hours {m:.0f} minutes and {s:.2f} seconds")
print("\n")
