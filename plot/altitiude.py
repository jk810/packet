from pathlib import Path
import math

data_name = f'1000sat_4hop_6con'
current_file_path = Path(__file__)
results_path = str(current_file_path.parents[1]) + f'/results/{data_name}/'

# open xyz text file and extract values
xyz = open(results_path + 'xyz.txt', 'r')
pos = {}
for i, line in enumerate(xyz):
    a = line.split()
    pos[str(i)] = (float(a[0]), float(a[1]), float(a[2]))
xyz.close()


alt = []
for item in pos.values():
    alt.append(math.sqrt(item[0]**2 + item[1]**2 + item[2]**2))

print(sum(alt) / len(alt) - 6378)