import csv
import os
from github import Github
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--t', type=str, help='GitHub access token to overcome API rate limitations')
args = parser.parse_args()

GITHUB_API_RATE_LIMIT = 6000
GITHUB_ACCESS_TOKEN = args.t
g = Github(GITHUB_ACCESS_TOKEN)

with open('repo-info/repo-info.csv', mode ='r') as file:

    csvFile = csv.reader(file)
    set = set()

    for line in csvFile:
        if(line[1].replace(".", "").isnumeric()):
            if float(line[1]) > 24.0:
                set.add(line[0])


input_csv = 'pr-data.csv'
output_csv = 'output.csv'

column_to_change = 5  # Change the second column (0-indexed)
counter = 0
# Open the input CSV file in read mode and the output CSV file in write mode
df = pd.read_csv(input_csv)
for index, row in df.iterrows():
   # print( pd.isna(row[column_to_change]))
    if column_to_change < len(row) and pd.isna(row[column_to_change]) and row[0] in set:
        # Update the desired column with the new value
        print("inside if")
        repo_name = row[0].split('github.com/')[1]
        repo = Github(GITHUB_ACCESS_TOKEN).get_repo(repo_name)
        branch = repo.get_branch(repo.default_branch)
        df.at[index, -1] = str(branch.commit.commit.author.date).split(" ")[0]
        df.at[index, column_to_change] = "Unmaintained"

df.to_csv(input_csv, index=False)