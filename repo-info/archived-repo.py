import csv
import os

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

# Open the input CSV file in read mode and the output CSV file in write mode
with open(input_csv, 'r', newline='') as input_file, open(output_csv, 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    for row in reader:
        # Check if the current row has enough columns
        if column_to_change < len(row) and row[0] in set:
            # Update the desired column with the new value
            row[column_to_change] = "Unmaintained"
        writer.writerow(row)

    os.remove(input_csv)
    os.rename(output_csv, 'pr-data.csv')