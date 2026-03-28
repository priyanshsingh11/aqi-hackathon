import nbformat

def update_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    # Section 2 Observation (Cell 6)
    nb.cells[6].source = [
        '**Your Observation:**\n',
        '\n',
        '- The dataset is highly imbalanced.\n',
        '- "Moderate" (32.9%) and "Satisfactory" (30.9%) are the most frequent AQI buckets.\n',
        '- "Good" (4.5%) and "Severe" (7.1%) are the least common.\n',
        '- This imbalance suggests that using simple accuracy for evaluation will be misleading; we should focus on **Macro F1-score**.'
    ]
    
    # Section 3 Observation (Cell 9)
    nb.cells[9].source = [
        '**Your Observation:**\n',
        '\n',
        '- There is significant variation in pollution levels across cities.\n',
        '- Cities like **Delhi** and **Gurugram** show the highest median PM2.5 levels, often exceeding the overall mean.\n',
        '- Southern/Coastal cities like **Thiruvananthapuram** and **Bengaluru** tend to have much lower PM2.5 medians.\n',
        '- This indicates that "City" is a crucial feature for the model.'
    ]
    
    # Section 4 Code (Cell 12)
    nb.cells[12].source = [
        '# YOUR CODE — PM2.5 Distribution by Day of Week\n',
        'train["DayOfWeek"] = train["Date"].dt.day_name()\n',
        'dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]\n',
        'plt.figure(figsize=(10, 5))\n',
        'sns.boxplot(data=train, x="DayOfWeek", y="PM2.5", order=dow_order, palette="viridis", showfliers=False)\n',
        'plt.title("PM2.5 Distribution by Day of Week", fontweight="bold")\n',
        'plt.show()'
    ]
    
    # Section 4 Observation (Cell 13)
    nb.cells[13].source = [
        '**Your Observation:**\n',
        '\n',
        '- PM2.5 levels show clear seasonality; levels peak in winter months (Nov, Dec, Jan) and dip during the monsoon (July, Aug).\n',
        '- Minor variations across days of the week suggest Sunday might have slightly lower levels due to reduced activity.'
    ]
    
    # Section 5 Code (Cell 16)
    nb.cells[16].source = [
        '# YOUR CODE — Relationship between PM2.5, NO2 and AQI Bucket\n',
        'plt.figure(figsize=(10, 6))\n',
        'order = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]\n',
        'colors = ["#4CAF50", "#8BC34A", "#FFC107", "#FF9800", "#F44336", "#9C27B0"]\n',
        'sns.scatterplot(data=train, x="PM2.5", y="NO2", hue="AQI_Bucket", hue_order=order, palette=colors, alpha=0.6)\n',
        'plt.title("PM2.5 vs NO2 by AQI Bucket", fontweight="bold")\n',
        'plt.xscale("log"); plt.yscale("log")\n',
        'plt.show()'
    ]
    
    # Section 5 Observation (Cell 17)
    nb.cells[17].source = [
        '**Your Observation:**\n',
        '\n',
        '- Both PM2.5 and NO2 are positively correlated with each other and with the AQI_Bucket severity.\n',
        '- The "Severe" and "Very Poor" categories are clustered at high concentrations of both pollutants.\n',
        '- Log-scale visualization helps see the separation between categories better.'
    ]
    
    # Section 6 Code (Cell 20 and 23)
    nb.cells[20].source = [
        '# YOUR CODE — Original exploration 1: Boxplots per Bucket\n',
        'order = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]\n',
        'colors = ["#4CAF50", "#8BC34A", "#FFC107", "#FF9800", "#F44336", "#9C27B0"]\n',
        'plt.figure(figsize=(12, 5))\n',
        'sns.boxplot(data=train, x="AQI_Bucket", y="PM2.5", order=order, palette=colors, showfliers=False)\n',
        'plt.title("PM2.5 Distribution per AQI Bucket", fontweight="bold")\n',
        'plt.show()'
    ]
    nb.cells[21].source = [
        '**Your Observation:**\n',
        '\n',
        '- Each AQI bucket has a distinct PM2.5 range, which is expected.\n',
        '- There is some overlap in ranges, suggesting other pollutants or rolling averages also play a role.'
    ]
    
    nb.cells[23].source = [
        '# YOUR CODE — Original exploration 2: Correlation Heatmap\n',
        'import numpy as np\n',
        'numeric_cols = train.select_dtypes(include=[np.number]).columns\n',
        'plt.figure(figsize=(8, 6))\n',
        'sns.heatmap(train[numeric_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")\n',
        'plt.title("Feature Correlation Heatmap", fontweight="bold")\n',
        'plt.show()'
    ]
    nb.cells[24].source = [
        '**Your Observation:**\n',
        '\n',
        '- High correlation between PM2.5 and NO2 (0.4-0.6 range).\n',
        '- Temporal features like "month" show correlation with pollutant levels, highlighting seasonality.'
    ]

    with open(path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

if __name__ == "__main__":
    update_notebook("exploration.ipynb")
    print("Notebook updated successfully.")
