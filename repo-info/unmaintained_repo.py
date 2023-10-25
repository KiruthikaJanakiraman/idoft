import csv
import os
from github import Github
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--t', type=str, help='GitHub access token to overcome API rate limitations')
args = parser.parse_args()

GITHUB_API_RATE_LIMIT = 6000
GITHUB_ACCESS_TOKEN = args.t
#GITHUB_ACCESS_TOKEN = "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"
g = Github(GITHUB_ACCESS_TOKEN)

with open('repo-info/repo-info.csv', mode ='r') as file:

    csvFile = csv.reader(file)
    set = set()

    for line in csvFile:
        if(line[1].replace(".", "").isnumeric()):
            if float(line[1]) > 24.0:
                set.add(line[0])


input_csv = 'pr-data.csv'
output_csv = 'temp.csv'

column_to_change = 5  # Change the second column (0-indexed)
counter = 0
# Open the input CSV file in read mode and the output CSV file in write mode
with open(input_csv, 'r', newline='') as input_file, open(output_csv, 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    for row in reader:
        # Check if the current row has enough columns
        counter+=1
        if column_to_change < len(row) and row[0] in set:
            # Update the desired column with the new value
            repo_name = row[0].split('github.com/')[1]
            repo = Github(GITHUB_ACCESS_TOKEN).get_repo(repo_name)
            branch = repo.get_branch(repo.default_branch)
            row[-1] = str(branch.commit.commit.author.date).split(" ")[0]
            row[column_to_change] = "Unmaintained"
        writer.writerow(row)
        print(counter)
#     os.remove(input_csv)
#     os.rename(output_csv, 'pr-data.csv')