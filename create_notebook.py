import nbformat as nbf
import os

# Create a new notebook
nb = nbf.v4.new_notebook()

# Create markdown cell
markdown = """\
# Market Sentiment Analysis

This dashboard shows the current market sentiment indicators and what's already priced into the market."""

code = """\
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Sample market sentiment data
dates = pd.date_range(start='2024-01-01', periods=100)
data = pd.DataFrame({
    'Date': dates,
    'VIX': np.random.normal(20, 5, 100),  # Volatility Index
    'Put_Call_Ratio': np.random.normal(1.0, 0.2, 100),  # Put/Call Ratio
    'Market_Sentiment': np.random.normal(50, 10, 100)  # Sentiment Index (0-100)
})

# Create a figure with subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))

# Plot VIX
sns.lineplot(data=data, x='Date', y='VIX', ax=ax1)
ax1.set_title('VIX Index')
ax1.set_ylabel('VIX Level')

# Plot Put/Call Ratio
sns.lineplot(data=data, x='Date', y='Put_Call_Ratio', ax=ax2)
ax2.set_title('Put/Call Ratio')
ax2.set_ylabel('Ratio')

# Plot Market Sentiment
sns.lineplot(data=data, x='Date', y='Market_Sentiment', ax=ax3)
ax3.set_title('Market Sentiment Index')
ax3.set_ylabel('Sentiment (0-100)')

plt.tight_layout()
plt.show()"""

# Add cells to the notebook
nb['cells'] = [
    nbf.v4.new_markdown_cell(markdown),
    nbf.v4.new_code_cell(code)
]

# Ensure the notebooks directory exists
os.makedirs('docs/notebooks', exist_ok=True)

# Write the notebook to a file
with open('docs/notebooks/dashboard1.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f) 