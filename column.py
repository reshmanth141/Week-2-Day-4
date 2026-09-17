"""Create calculated columns from existing mark columns."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def add_calculated_columns(
	data: pd.DataFrame,
	mark_columns: Iterable[str],
	maximum_marks: float | None = None,
) -> pd.DataFrame:
	"""Return a copy of *data* with total marks and percentage columns.

	``maximum_marks`` is the total possible marks for all mark columns.  If it
	is omitted, the percentage is calculated against the number of mark
	columns (assuming each column is out of 100).
	"""
	columns = list(mark_columns)
	missing = [column for column in columns if column not in data.columns]
	if missing:
		raise KeyError(f"Missing mark columns: {', '.join(missing)}")
	if not columns:
		raise ValueError("At least one mark column is required")

	result = data.copy()
	result["total_marks"] = result[columns].sum(axis=1)

	maximum = maximum_marks if maximum_marks is not None else len(columns) * 100
	if maximum <= 0:
		raise ValueError("maximum_marks must be greater than zero")
	result["percentage"] = result["total_marks"] / maximum * 100
	return result


if __name__ == "__main__":
	# Example: replace these names with the columns in your input file.
	marks = pd.DataFrame(
		{"name": ["Asha", "Ben"], "maths": [85, 72], "science": [90, 78]}
	)
	print(add_calculated_columns(marks, ["maths", "science"]))
