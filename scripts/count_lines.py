import os
import glob
import json
from prettytable import PrettyTable

# Directories to search for .yml files
directories = {
    "domain": "*.yml",
    "data": "*.yml"
}

# Root directories to loop over (excluding 'actions' as it's only in the root)
root_dirs = ['.', 'dm1_versions/version_1', 'dm1_versions/version_2', 'dm1_versions/version_3', 'dm1_versions/version_4']

# Data file to store line counts
data_file = 'line_counts.json'

# Function to count non-empty lines in a file
def count_lines_in_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return sum(1 for line in file if line.strip())
    except FileNotFoundError:
        return 0

# Function to recursively find files with a specific pattern
def find_files(directory, pattern):
    search_path = os.path.join(directory, '**', pattern)
    return glob.glob(search_path, recursive=True)

# Function to calculate line counts
def calculate_line_counts(root_dirs):
    data = {}
    # Count lines in 'actions' directory once, as it's only in the root
    actions_line_count = sum(count_lines_in_file(file) for file in find_files('.', '*.py'))
    
    for root_dir in root_dirs:
        line_counts = { "domain": 0, "data": 0, "actions": actions_line_count }
        
        for dir, pattern in directories.items():
            for filepath in find_files(os.path.join(root_dir, dir), pattern):
                line_count = count_lines_in_file(filepath)
                line_counts[dir] += line_count

        data[root_dir] = line_counts
    return data

# Calculate line counts and save to file
data = calculate_line_counts(root_dirs)
with open(data_file, 'w') as file:
    json.dump(data, file)

# Generate and print PrettyTable
table = PrettyTable()
table.field_names = ["Root Directory", "Domain", "Data", "Actions", "Total Lines"]
for root_dir, counts in data.items():
    total_lines = sum(counts.values())
    table.add_row([root_dir, counts["domain"], counts["data"], counts["actions"], total_lines])

print(table)
