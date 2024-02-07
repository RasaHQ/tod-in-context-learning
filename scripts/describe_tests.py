import os
import glob
import yaml

# Directory to search for .yml files
directory = "e2e_tests"

# Function to recursively find files with a specific pattern
def find_files(directory, pattern):
    search_path = os.path.join(directory, '**', pattern)
    return glob.glob(search_path, recursive=True)

def describe_conversations(directory):
    # Initialize statistics
    total_conversations = 0
    min_turns = 1000
    max_turns = 0
    total_turns = 0

    # Find all .yml files in the directory and its subdirectories
    for filepath in find_files(directory, "*.yml"):
        with open(filepath, 'r') as file:
            # Load YAML file
            data = yaml.safe_load(file)

            # Iterate over all test cases in the file
            for test_case in data['test_cases']:
                total_conversations += 1
                turns = len([s for s in test_case['steps'] if 'user' in s or 'utter' in s])
                min_turns = min(min_turns, turns)
                max_turns = max(max_turns, turns)
                total_turns += turns

    # Compute average turns
    avg_turns = total_turns / total_conversations if total_conversations else 0

    # Print statistics
    print(f"Total conversations: {total_conversations}")
    print(f"Minimum turns: {min_turns}")
    print(f"Maximum turns: {max_turns}")
    print(f"Average turns: {avg_turns:.2f}")

describe_conversations(directory)
