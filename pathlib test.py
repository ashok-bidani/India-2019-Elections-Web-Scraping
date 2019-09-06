from pathlib import Path

data_folder = Path('output_data')
file = data_folder / 'test.csv'

with open(file, 'r') as reader:
    for line in reader:
        print(line)