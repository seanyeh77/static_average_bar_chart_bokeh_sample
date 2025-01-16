# README

## Overview
This script generates an interactive bar chart using Bokeh to visualize daily data and compute averages over a selected time range. It includes a range selection tool for custom visualization and dynamically updates the displayed average based on the selected range.

## Features
- **Data Generation**: Generates 30 days of test data with random values.
- **Interactive Chart**: Visualizes daily values as a bar chart.
- **Rolling Average**: Includes a rolling average line (7-day default).
- **Range Selector**: Enables dynamic selection of date ranges.
- **Dynamic Average Display**: Updates and displays the average value for the selected range in real-time.

## Requirements
The script requires the following Python libraries:
- `pandas`
- `numpy`
- `bokeh`

To install the required libraries, run:
```bash
pip install pandas numpy bokeh
```

## File Descriptions
- `test_data.csv`: Contains the generated test data with dates and values.
- `static_average_bar_chart.html`: The output HTML file containing the interactive chart.

## How to Use

### 1. Generate Test Data
The script generates random test data for the past 30 days. Each day has a random value between 80 and 120.

### 2. Run the Script
Run the script in a Python environment. The script will:
1. Generate a CSV file (`test_data.csv`) with the test data.
2. Create an interactive HTML file (`static_average_bar_chart.html`) for visualization.

### 3. Open the HTML File
After running the script, open `static_average_bar_chart.html` in a web browser to view the interactive chart.

## Function Descriptions

### `generate_test_data()`
Generates a CSV file (`test_data.csv`) containing 30 days of random data with the following columns:
- `date`: The date of the data point.
- `value`: A random value between 80 and 120.

### `show_data(df, data_path, label)`
Visualizes the data in an interactive chart.

#### Parameters:
- `df`: DataFrame containing the data to visualize. Must include `date` and `value` columns.
- `data_path`: Path to save the HTML file.
- `label`: A label to display in the title and average calculation.

#### Features:
- Displays daily values as a bar chart.
- Adds a rolling average line (default 7 days).
- Includes a range selection tool to dynamically adjust the view and calculate averages for the selected range.

### JavaScript Callback
A `CustomJS` callback dynamically updates the average display based on the selected range in the chart.

## Example Output
- **Title**: Displays the selected range's average with a label.
- **Bar Chart**: Visualizes daily values with bars.
- **Rolling Average Line**: Highlights trends using a red line.
- **Range Selector**: Allows custom date range selection.

## Customization
- **Rolling Average Window**: Change the `avg_day` parameter in `show_data()` to modify the rolling average window size.
- **Range Display**: Adjust initial range settings in the `RangeTool` section.

## Output
The script generates an interactive HTML file (`static_average_bar_chart.html`) that can be shared and viewed in any modern web browser.

