import json
import re
import os
from prettytable import PrettyTable

# Function to read line count data
def read_line_count_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to parse test results
def parse_test_results(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            match = re.search(r'(\d+) failed, (\d+) passed', content)
            if match:
                return int(match.group(1)), int(match.group(2))  # Failed, Passed
            else:
                return 0, 0  # No data found
    except FileNotFoundError:
        return 0, 0  # File not found

# Read line count data
line_counts = read_line_count_data('line_counts.json')

# Initialize table
table = PrettyTable()
table.field_names = ["Version", "Conversation Type", "Failed Tests", "Passed Tests"]

# Process each version and directory
versions = ['version_1', 'version_2', 'version_3']
for version in versions:
    version_path = f'dm1_versions/{version}' if version != 'root' else '.'
    #version_name = version if version != 'root' else 'Root'
    # Loop through each subdirectory in e2e_tests
    for subdir in os.listdir('e2e_tests'):
        test_result_file = f'test_results/{version}_{subdir}.txt'
        failed_tests, passed_tests = parse_test_results(test_result_file)
        version_data = line_counts.get(version_path, {})
        total_lines = sum(version_data.values())
        table.add_row([version, subdir, failed_tests, passed_tests])

# Print the table
print(table)
