import os
import pandas as pd
import matplotlib.pyplot as plt

temperature = 0.5
file_name = 'PSSBPSUT'
dir_name= "C:\\Users\\cdiggs\\janus\\requirements_evaluation\\Fixed Req Variable Temp\\" + str(temperature) + "_" + file_name + "_evaluations\\"
suffix = '.txt'
path = os.path.join(dir_name, file_name + suffix)

data = []

# Loop through files in the directory
for filename in os.listdir(dir_name):
    if filename.endswith(".txt"):  # Adjust the file extension if needed
        print(filename)
        with open(os.path.join(dir_name, filename), "r") as file:
            lines = file.readlines()

        # Extract values from each line
        values = {}
        for line in lines:
            key, value = line.strip().split(" - ")
            values[key] = float(value)

        data.append(values)

df = pd.DataFrame(data)

# Define colors for each histogram
colors = ['skyblue', 'orange', 'green', 'purple']

# Create a single image with four subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
plt.subplots_adjust(hspace=0.5)  # Adjust vertical spacing

# Loop through each metric and create a histogram subplot with a different color
for idx, (column, color) in enumerate(zip(df.columns, colors)):
    row = idx // 2
    col = idx % 2
    axes[row, col].hist(df[column], bins=10, range=(0.5, 5.5), color=color, edgecolor='black', align='mid')
    axes[row, col].set_title(f'{column} Histogram')
    axes[row, col].set_xlabel('Rating')
    axes[row, col].set_ylabel('Frequency')
    axes[row, col].set_xticks(range(1, 6))
    axes[row, col].set_xlim(0.5, 5.5)  # Adjust x-axis limits
    axes[row, col].grid(False)  # Remove gridlines

plt.suptitle('Metric Histograms (Temperature=' + str(temperature) + ')', fontsize=16)

# Display the combined plot
#plt.show()
plt.savefig(file_name + '_temp'+ str(temperature) + '.png')