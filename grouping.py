import pandas as pd


def counts_and_averages_by_category(
	data: pd.DataFrame, category_column: str, value_column: str
) -> pd.DataFrame:
	"""Calculate the count and average value for each category."""
	return (
		data.groupby(category_column)[value_column]
		.agg(count="count", average="mean")
		.reset_index()
	)
