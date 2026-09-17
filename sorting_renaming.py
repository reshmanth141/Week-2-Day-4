"""Rename columns and sort CSV records by one or more columns."""

import argparse
import csv
from functools import cmp_to_key
from pathlib import Path


def rename_columns(fieldnames, renames):
	"""Return field names with the supplied old-name: new-name mappings applied."""
	return [renames.get(name, name) for name in fieldnames]


def sort_records(records, columns):
	"""Sort records by (column, ascending) pairs, in priority order."""
	def compare(left, right):
		for column, ascending in columns:
			a, b = left.get(column, ""), right.get(column, "")
			if a == b:
				continue
			try:
				result = -1 if float(a) < float(b) else 1
			except (TypeError, ValueError):
				result = -1 if a.casefold() < b.casefold() else 1
			return result if ascending else -result
		return 0

	return sorted(records, key=cmp_to_key(compare))


def process_csv(input_path, output_path, renames=None, sort_columns=None):
	renames = renames or {}
	sort_columns = sort_columns or []

	with open(input_path, newline="", encoding="utf-8-sig") as source:
		reader = csv.DictReader(source)
		if not reader.fieldnames:
			raise ValueError("The input CSV has no header row.")
		old_fields = reader.fieldnames
		records = list(reader)

	# Rename keys before sorting so sort specifications use the output names.
	fields = rename_columns(old_fields, renames)
	renamed_records = [
		{renames.get(key, key): value for key, value in record.items()}
		for record in records
	]
	records = sort_records(renamed_records, sort_columns)

	with open(output_path, "w", newline="", encoding="utf-8") as destination:
		writer = csv.DictWriter(destination, fieldnames=fields)
		writer.writeheader()
		writer.writerows(records)


def main():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("input", type=Path, help="Input CSV file")
	parser.add_argument("output", type=Path, help="Output CSV file")
	parser.add_argument(
		"--rename", action="append", default=[], metavar="OLD=NEW",
		help="Rename a column; may be supplied more than once",
	)
	parser.add_argument(
		"--sort", action="append", default=[], metavar="COLUMN[:desc]",
		help="Sort column (ascending by default); may be repeated",
	)
	args = parser.parse_args()

	renames = {}
	for item in args.rename:
		if "=" not in item:
			parser.error("--rename must use OLD=NEW")
		old, new = item.split("=", 1)
		renames[old] = new

	sort_columns = []
	for item in args.sort:
		parts = item.rsplit(":", 1)
		descending = len(parts) == 2 and parts[1].lower() == "desc"
		if len(parts) == 2 and parts[1].lower() not in {"asc", "desc"}:
			parser.error("sort direction must be asc or desc")
		sort_columns.append((parts[0], not descending))

	process_csv(args.input, args.output, renames, sort_columns)


if __name__ == "__main__":
	main()
