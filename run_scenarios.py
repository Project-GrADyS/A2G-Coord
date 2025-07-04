import subprocess
import csv
import time
import json
from simulation_config.folder_config import create_folder
#from simulation_config.algorithm_config import set_algorithms, serialize_algorithms

start_time = time.time()

num_experiments = 2

# args = {
#     "ugv_num": ["2", "4", "8"],
#     "uav_num": ["1", "2"],
#     "poi_num": ["5", "15", "25"],
#     "communication_range": ["5", "10", "20"],
#     "generate_graph": 1,
#     "csv_path": "experiment_6",
#     "map_size": "100",
#     "algorithms": ["v1", "v2", "v3"] 
# }

args = {
    "ugv_num": ["4"],
    "uav_num": ["2","3"],
    "poi_num": ["5"],
    "communication_range": ["10"],
    "generate_graph": 1,
    "csv_path": "experiment_v7v6v5_buffer",
    "map_size": "100",
    "algorithms": ["v5", "v6", "v7"] 
}

header = ['experiment', 'ugv_num', 'uav_num', 'poi_num', 'comm_range', 'time_poi'] 

# Create experiment folder structure
folder_path = f'experiments/{args["csv_path"]}'
create_folder(folder_path)

create_folder(f'experiments/{args["csv_path"]}/metrics')
create_folder(f'experiments/{args["csv_path"]}/metrics/mean_time')
create_folder(f'experiments/{args["csv_path"]}/metrics/boxplot_average_time')
create_folder(f'experiments/{args["csv_path"]}/metrics/individual_time')

# Run experiments

# File name: name_numUGV_numUAV_numpoi_commRange

for algorithm_version in args["algorithms"]:
    algorithm_path_analysis = folder_path + f'/algorithm_{algorithm_version}/analysis'
    algorithm_path_data = folder_path + f'/algorithm_{algorithm_version}/data'
    algorithm_path_images = folder_path + f'/algorithm_{algorithm_version}/images'
    create_folder(algorithm_path_analysis)
    create_folder(algorithm_path_data)
    create_folder(algorithm_path_images)

for comm_range in args["communication_range"]:
    for uav_num in args["uav_num"]:
        for ugv_num in args["ugv_num"]:
            for poi_num in args["poi_num"]:
                header_list = []
                for p in range(int(poi_num)):
                    name_column = 'poi' + str(p+1)
                    header_list.append(name_column)
                for algorithm_version in args["algorithms"]:
                    algorithm_path_data = folder_path + f'/algorithm_{algorithm_version}/data'
                    file_name = args["csv_path"] + "_ugv" + ugv_num + "_uav" + uav_num + "_poi" + poi_num + "_range" + comm_range
                    with open(algorithm_path_data + f"/{file_name}.csv", 'w') as file: 
                        dw = csv.DictWriter(file, fieldnames=header+header_list)
                        dw.writeheader()
                for i in range(num_experiments):
                    subprocess.run(["python3", "main.py", 
                                    str(i+1), 
                                    ugv_num, 
                                    uav_num, 
                                    poi_num, 
                                    comm_range,
                                    str(args["generate_graph"]),
                                    file_name,
                                    args["csv_path"],
                                    args["map_size"],
                                    json.dumps(args["algorithms"])
                                    ],)
#Join CSVs
subprocess.run(["pypy", "join_csvs.py", args["csv_path"], json.dumps(args["algorithms"])],)

# Create graphs
subprocess.run(["pypy", "run_graphs.py", args["csv_path"], json.dumps(args["algorithms"])],)

subprocess.run(["pypy", "run_boxplot.py", args["csv_path"], json.dumps(args["algorithms"])],)

end_time = time.time()

total_time = end_time - start_time
h = total_time // 3600
m = (total_time % 3600) // 60
s = total_time % 60

print("\n")
print(f"Total simulation time: {h} hours {m} minutes and {s} seconds")
print("\n")