"""Create and practice handling missing values in a pandas dataset."""

import numpy as np
import pandas as pd


# Create a dataset with missing numeric and text values.
data = pd.DataFrame(
	{
		"name": ["Alice", "Bob", "Charlie", "Diana", "Evan"],
		"age": [25, np.nan, 31, 28, np.nan],
		"city": ["New York", "London", np.nan, "Paris", "London"],
		"score": [88.5, 92.0, np.nan, 79.5, 85.0],
	}
)

print("Original dataset:\n", data)

# Identify missing values and count them in each column.
print("\nMissing-value mask:\n", data.isna())
print("\nMissing values per column:\n", data.isna().sum())

# Fill numeric values with their column median and city with a label.
filled = data.copy()
filled["age"] = filled["age"].fillna(filled["age"].median())
filled["score"] = filled["score"].fillna(filled["score"].median())
filled["city"] = filled["city"].fillna("Unknown")
print("\nAfter filling missing values:\n", filled)

# Drop rows or columns containing missing values.
print("\nRows with no missing values:\n", data.dropna())
print("\nColumns with no missing values:\n", data.dropna(axis="columns"))
