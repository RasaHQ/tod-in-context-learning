import json
import re
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
table.field_names = ["Version", "Domain", "Data", "Actions", "Total Lines", "Failed Tests", "Passed Tests"]

# Process each version and root dir
versions = ['.', 'dm1_versions/version_1', 'dm1_versions/version_2', 'dm1_versions/version_3', 'dm1_versions/version_4']
for version in versions:
    version_name = version.split('/')[-1] if '/' in version else 'Root'
    test_result_file = f'test_results_{version_name}.txt' if version_name != 'Root' else 'test_results.txt'
    failed_tests, passed_tests = parse_test_results(test_result_file)
    version_data = line_counts.get(version, {})
    total_lines = sum(version_data.values())
    table.add_row([version_name, version_data.get("domain", 0), version_data.get("data", 0), version_data.get("actions", 0), total_lines, failed_tests, passed_tests])

# Print the table
print(table)
