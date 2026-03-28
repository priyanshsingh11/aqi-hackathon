import nbformat

def update_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # helper to find cells
    def find_cell(marker, cell_type='markdown'):
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == cell_type and marker in ''.join(cell.source):
                return i
        return None

    # Section 2 Observation
    idx = find_cell('2. Target Variable Distribution')
    if idx is not None:
        # The next markdown cell after this title should be the observation
        for j in range(idx + 1, len(nb.cells)):
            if nb.cells[j].cell_type == 'markdown' and '**Your Observation:**' in ''.join(nb.cells[j].source):
                nb.cells[j].source = [
                    '**Your Observation:**\n',
                    '\n',
                    '- The dataset is highly imbalanced.\n',
                    '- "Moderate" (32.9%) and "Satisfactory" (30.9%) are the most frequent AQI buckets.\n',
                    '- "Good" (4.5%) and "Severe" (7.1%) are the least common.\n',
                    '- This imbalance suggests that using simple accuracy for evaluation will be misleading; we should focus on **Macro F1-score**.'
                ]
                break

    # Section 3 Observation
    idx = find_cell('3. City-Level Profiles')
    if idx is not None:
        for j in range(idx + 1, len(nb.cells)):
            if nb.cells[j].cell_type == 'markdown' and '**Your Observation:**' in ''.join(nb.cells[j].source):
                nb.cells[j].source = [
                    '**Your Observation:**\n',
                    '\n',
                    '- There is significant variation in pollution levels across cities.\n',
                    '- Cities like **Delhi** and **Gurugram** show the highest median PM2.5 levels, often exceeding the overall mean.\n',
                    '- Southern/Coastal cities like **Thiruvananthapuram** and **Bengaluru** tend to have much lower PM2.5 medians.\n',
                    '- This indicates that "City" is a crucial feature for the model.'
                ]
                break

    # Section 4 Code and Observation
    idx = find_cell('4. Temporal Patterns')
    if idx is not None:
        # Find next # YOUR CODE
        for j in range(idx + 1, len(nb.cells)):
            if nb.cells[j].cell_type == 'code' and '# YOUR CODE' in ''.join(nb.cells[j].source):
                nb.cells[j].source = [
                    '# YOUR CODE — PM2.5 Distribution by Day of Week\n',
                    'train["DayOfWeek"] = train["Date"].dt.day_name()\n',
                    'dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]\n',
                    'plt.figure(figsize=(10, 5))\n',
                    'sns.boxplot(data=train, x="DayOfWeek", y="PM2.5", order=dow_order, palette="viridis", showfliers=False)\n',
                    'plt.title("PM2.5 Distribution by Day of Week", fontweight="bold")\n',
                    'plt.show()'
                ]
                # Then the next observation
                for k in range(j + 1, len(nb.cells)):
                    if nb.cells[k].cell_type == 'markdown' and '**Your Observation:**' in ''.join(nb.cells[k].source):
                        nb.cells[k].source = [
                            '**Your Observation:**\n',
                            '\n',
                            '- PM2.5 levels show clear seasonality; levels peak in winter months (Nov, Dec, Jan) and dip during the monsoon (July, Aug).\n',
                            '- Minor variations across days of the week suggest Sunday might have slightly lower levels.'
                        ]
                        break
                break

    # Section 5 Code and Observation
    idx = find_cell('5. PM2.5 and NO2 — Relationship to AQI')
    if idx is not None:
        for j in range(idx + 1, len(nb.cells)):
            if nb.cells[j].cell_type == 'code' and '# YOUR CODE' in ''.join(nb.cells[j].source):
                nb.cells[j].source = [
                    '# YOUR CODE — Relationship between PM2.5, NO2 and AQI Bucket\n',
                    'plt.figure(figsize=(10, 6))\n',
                    'order = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]\n',
                    'colors = ["#4CAF50", "#8BC34A", "#FFC107", "#FF9800", "#F44336", "#9C27B0"]\n',
                    'sns.scatterplot(data=train, x="PM2.5", y="NO2", hue="AQI_Bucket", hue_order=order, palette=colors, alpha=0.6)\n',
                    'plt.title("PM2.5 vs NO2 by AQI Bucket", fontweight="bold")\n',
                    'plt.xscale("log"); plt.yscale("log")\n',
                    'plt.show()'
                ]
                for k in range(j + 1, len(nb.cells)):
                    if nb.cells[k].cell_type == 'markdown' and '**Your Observation:**' in ''.join(nb.cells[k].source):
                        nb.cells[k].source = [
                            '**Your Observation:**\n',
                            '\n',
                            '- Both PM2.5 and NO2 are positively correlated with each other and with the AQI_Bucket severity.\n',
                            '- The "Severe" and "Very Poor" categories are clustered at high concentrations of both pollutants.'
                        ]
                        break
                break

    # Section 6 Original Exploration
    idx = find_cell('6. Your Own Exploration')
    if idx is not None:
        # Find 1st YOUR CODE
        found_count = 0
        for j in range(idx + 1, len(nb.cells)):
            if nb.cells[j].cell_type == 'code' and '# YOUR CODE' in ''.join(nb.cells[j].source):
                found_count += 1
                if found_count == 1:
                    nb.cells[j].source = [
                        '# YOUR CODE — Boxplots per Bucket\n',
                        'order = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]\n',
                        'colors = ["#4CAF50", "#8BC34A", "#FFC107", "#FF9800", "#F44336", "#9C27B0"]\n',
                        'plt.figure(figsize=(12, 5))\n',
                        'sns.boxplot(data=train, x="AQI_Bucket", y="PM2.5", order=order, palette=colors, showfliers=False)\n',
                        'plt.title("PM2.5 Distribution per AQI Bucket", fontweight="bold")\n',
                        'plt.show()'
                    ]
                    # Next obs
                    for k in range(j + 1, len(nb.cells)):
                        if nb.cells[k].cell_type == 'markdown' and '**Your Observation:**' in ''.join(nb.cells[k].source):
                            nb.cells[k].source = [
                                '**Your Observation:**\n',
                                '\n',
                                '- Each AQI bucket has a distinct PM2.5 range, but with some overlap suggesting other factors play a role.'
                            ]
                            break
                elif found_count == 2:
                    nb.cells[j].source = [
                        '# YOUR CODE — Correlation Heatmap\n',
                        'import numpy as np\n',
                        'numeric_cols = train.select_dtypes(include=[np.number]).columns\n',
                        'plt.figure(figsize=(8, 6))\n',
                        'sns.heatmap(train[numeric_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")\n',
                        'plt.title("Feature Correlation Heatmap", fontweight="bold")\n',
                        'plt.show()'
                    ]
                    # Next obs
                    for k in range(j + 1, len(nb.cells)):
                        if nb.cells[k].cell_type == 'markdown' and '**Your Observation:**' in ''.join(nb.cells[k].source):
                            nb.cells[k].source = [
                                '**Your Observation:**\n',
                                '\n',
                                '- High correlation between pollutants confirms they are joint drivers of AQI.'
                            ]
                            break
                    break

    with open(path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

if __name__ == "__main__":
    update_notebook("exploration.ipynb")
    print("Notebook updated successfully.")
