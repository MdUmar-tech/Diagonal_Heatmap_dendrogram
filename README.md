# Diagonal_Heatmap_dendrogram

This project provides a Python script for creating a diagonal heatmap with dendrogram using Matplotlib. The script takes input data and generates an interactive heatmap visualizing relationships between variables.
The input data should be in long form and accept both tsv and csv formate 
example file (csv) 
df = pd.read_csv(file_path, delimiter='\t')
# Example usage:
df = pd.DataFrame({
    "x1": ["A", "A", "A", "A", "A", "B", "B", "B", "B", "C", "C", "C", "D", "D", "E"],
    "x2": ["B", "C", "D", "E", "F", "C", "D", "E", "F", "D", "E", "F", "E", "F", "F"],
    "relation": [76.90, 75.26, 74.82, 74.61, 71.78, 75.49, 75.56, 75.41, 72.16, 74.68, 74.28, 71.71, 73.87, 72.34, 72.14]
})
## Features

- Diagonal heatmap visualization with dendrogram
- Customizable color mapping and labeling
- Supports interactive exploration of relationships

This repository contains code for creating a diagonal heatmap with dendrogram using Python and Matplotlib.



1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/diagonal_heatmap.git

2. Install the required dependencies:
   matplotlib==3.4.3

## Usage
3. Run the diagonal_heatmap.py script:
   keep the file and script in same folder or provide full path of both scripts location and file location
   python your_script.py modified_AAI.tsv


   if dendrograme is not required in line under def main(): section 
   diagonal_heatmap(df, include_dendrogram=True, cmap='viridis', show_cbar=True)
   can be set as False 

