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

# Initialize table with updated fields
table = PrettyTable()
field_names = ["Subdirectory"]
versions = ['version_1', 'version_2', 'version_3']
total_passes = {version: 0 for version in versions}
total_tests = {version: 0 for version in versions}

# Append version names as part of the field names
for version in versions:
    field_names.append(f"Version {version[-1]} Results")  # Assuming version format is consistent
table.field_names = field_names

# Initialize a dictionary to hold test results
test_results = {}

# Process each version and directory
for version in versions:
    # Loop through each subdirectory in e2e_tests
    for subdir in os.listdir('e2e_tests'):
        if subdir not in test_results:
            test_results[subdir] = []
        test_result_file = f'test_results/{version}_{subdir}.txt'
        failed_tests, passed_tests = parse_test_results(test_result_file)
        total_passes[version] += passed_tests
        total_tests[version] += passed_tests + failed_tests
        test_results[subdir].append(f"{passed_tests}/{passed_tests + failed_tests}")

# Add rows to the table for each subdirectory with accumulated results
for subdir, results in test_results.items():
    row = [subdir] + results
    table.add_row(row)

# Print the table
print(table)

# Calculate and print pass rate for each version
print(f"Total number of tests: {total_tests['version_1']}")
for version in versions:
    if total_tests[version] > 0:
        pass_rate = (total_passes[version] / total_tests[version]) * 100
        print(f"{version} Pass Rate: {pass_rate:.2f}%")
    else:
        print(f"{version} Pass Rate: No data")
