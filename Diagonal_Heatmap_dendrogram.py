
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from numpy import *
import pandas as pd
from matplotlib.colors import Normalize
from scipy.cluster.hierarchy import dendrogram, linkage
import argparse

import pandas as pd

def read_data(file_path):
    with open(file_path, 'r') as file:
        # Read the first line to determine the delimiter
        first_line = file.readline().strip()
        if ',' in first_line:
            delimiter = ','
        elif '\t' in first_line:
            delimiter = '\t'
        else:
            raise ValueError("Unable to determine the file format. Please specify the delimiter.")

    # Read the file using the determined delimiter
    df = pd.read_csv(file_path, delimiter=delimiter)
    return df

# Example usage
file_path = "modified_AAI.tsv"  # Update with your file path
df = read_data(file_path)

# Print the columns of the DataFrame to check if they are read correctly
print(df.columns)

# Concatenate 'x1' and 'x2' columns before getting unique values
unique_vals = pd.concat([df['x1'], df['x2']]).unique()

# Now unique_vals contains the unique values from 'x1' and 'x2'
print(len(unique_vals))



#df = read_data(file_path)
#df = pd.read_csv(file_path, delimiter='\t')#for direct reading

'''
# Example usage:
df = pd.DataFrame({
    "x1": ["A", "A", "A", "A", "A", "B", "B", "B", "B", "C", "C", "C", "D", "D", "E"],
    "x2": ["B", "C", "D", "E", "F", "C", "D", "E", "F", "D", "E", "F", "E", "F", "F"],
    "relation": [76.90, 75.26, 74.82, 74.61, 71.78, 75.49, 75.56, 75.41, 72.16, 74.68, 74.28, 71.71, 73.87, 72.34, 72.14]
})
'''

def draw_rectangle(ax, center_x, center_y, value=None, cmap='viridis', df=None):
    n = 4
    t = arange(0, 360 + (360 / n), 360 / n)
    x = center_x + 10 * sin(radians(t))
    y = center_y + 10 * cos(radians(t))
    ax.text(center_x, center_y, f"{value:.2f}", ha='center', va='center', fontsize=8)
    ax.fill(x, y, edgecolor='black', facecolor=get_color(value, cmap, df))  # Combine fill and boundary

def get_color(value, cmap, df):
    norm = Normalize(vmin=df['relation'].min(), vmax=df['relation'].max())
    return plt.cm.viridis(norm(value))

# (Your existing functions remain unchanged)

def draw_pyramid_of_squares(n, wide_df): 
    for i in range(n):
        for j in range(i+1):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                x = i * 10
                y = j * 10
                value = wide_df.iloc[(n) - (i - j) // 2, (i + j) // 2]
                draw_rectangle(plt.gca(), x, y, value, cmap='viridis', df=df)
                
                if j != 0:
                    value = wide_df.iloc[(n) - (i + j) // 2, (i - j) // 2]
                    draw_rectangle(plt.gca(), x, -y, value, cmap='viridis', df=df)



unique_vals = pd.concat([df['x1'], df['x2']]).unique()
n=(len(unique_vals))
print(n)
def create_wide_df(data):
    unique_vals = pd.concat([data['x1'], data['x2']]).unique()
    wide_df = pd.DataFrame(100, columns=unique_vals, index=unique_vals)

    for index, row in data.iterrows():
        wide_df.loc[row['x1'], row['x2']] = row['relation']
        wide_df.loc[row['x2'], row['x1']] = row['relation']

    return wide_df
    

'''
def draw_dendrogram(wide_df):
    corr_data = wide_df.values
    row_linkage = linkage(corr_data, method='ward', metric='euclidean')
    col_linkage = linkage(corr_data.T, method='ward', metric='euclidean')
    orientation = orientation
    no_plot = no_plot
    row_order = dendrogram(row_linkage, labels=wide_df.index, no_plot=no_plot,orientation=orientation)['leaves']
    col_order = dendrogram(col_linkage, no_plot=True)['leaves']

    corr_data = corr_data[row_order][:, col_order]
    df_order = wide_df.iloc[row_order, col_order]

    return df_order
'''
def diagonal_heatmap(data, include_dendrogram=False, cmap='viridis', show_cbar=False):
    n = len(pd.concat([data['x1'], data['x2']]).unique())
    wide_df = create_wide_df(data)

    # Set the figure size here (adjust as needed)
    fig = plt.figure(figsize=(12, 10))

    left_heatmap = 0.05
    bottom_heatmap = 0.1
    width_heatmap = 0.5
    height_heatmap = 0.7

    left_dendrogram = 0.7
    bottom_dendrogram = 0.1
    width_dendrogram = 0.15
    height_dendrogram = 0.7

    # Add heatmap
    ax_heatmap = fig.add_axes([left_heatmap, bottom_heatmap, width_heatmap, height_heatmap])
    ax_heatmap.set_axis_off()  # Turn off outer plot area lines

    # Retrieve df_order from draw_dendrogram
    corr_data = wide_df.values
    row_linkage = linkage(corr_data, method='ward', metric='euclidean')
    col_linkage = linkage(corr_data.T, method='ward', metric='euclidean')
    row_order = dendrogram(row_linkage, labels=wide_df.index, no_plot=True,orientation='right')['leaves']
    col_order = dendrogram(col_linkage, no_plot=True)['leaves']

    corr_data = corr_data[row_order][:, col_order]
    df_order = wide_df.iloc[row_order, col_order]

    #df_order = draw_dendrogram(wide_df)

    draw_pyramid_of_squares(n-1, df_order)

    if include_dendrogram:
        # Add dendrogram
        ax_dendrogram = fig.add_axes([left_dendrogram, bottom_dendrogram, width_dendrogram, height_dendrogram])
        row_order = dendrogram(row_linkage, labels=wide_df.index,orientation='right')['leaves']
    


    if show_cbar:        
        cbar_ax = fig.add_axes([0.1, 0.1, 0.27, 0.02])  # Adjust the position and size
        cbar = plt.colorbar(plt.cm.ScalarMappable(norm=Normalize(vmin=df['relation'].min(), vmax=df['relation'].max()), cmap='viridis'), cax=cbar_ax, orientation='horizontal')
        cbar.set_label('Relation Value')
    plt.savefig("heatmap_and_dendrogram.png",dpi=300)
    plt.show()
    
# Your existing DataFrame and unique_vals code remains unchanged

#diagonal_heatmap(df, include_dendrogram=True, cmap='viridis', show_cbar=True)
def main():
    parser = argparse.ArgumentParser(description='Generate heatmap with dendrogram.')
    parser.add_argument('file_path', type=str, help='Path to the input data file.')
    args = parser.parse_args()

    # Read data from the specified file
    df = read_data(args.file_path)

    # Your existing code for drawing the heatmap with dendrogram
    diagonal_heatmap(df, include_dendrogram=True, cmap='viridis', show_cbar=True)

if __name__ == "__main__":
    main()

#usage=python Diagonal_Heatmap_dendrogram.py modified_AAI.tsv

