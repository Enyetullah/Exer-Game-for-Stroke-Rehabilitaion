from pathlib import Path
import csv
from collections import defaultdict


# This assumes this file is inside:
# D:\ExerGame V 2.0\src\creation_files\
# parents[2] goes back to:
# D:\ExerGame V 2.0
project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "data" / "processed" / "fixed_game_trial_results_cleaned.csv"

session_summary_path = project_root / "data" / "processed" / "fixed_game_session_summary.csv"
mode_level_summary_path = project_root / "data" / "processed" / "fixed_game_mode_level_summary.csv"
tester_mode_summary_path = project_root / "data" / "processed" / "fixed_game_tester_mode_summary.csv"
attempt_summary_path = project_root / "data" / "processed" / "fixed_game_attempt_summary.csv"


def is_blank(value):
    return value is None or str(value).strip() == ""


def safe_float(value):
    try:
        if is_blank(value):
            return None
        return float(value)
    except ValueError:
        return None


def safe_int(value):
    try:
        if is_blank(value):
            return None
        return int(float(value))
    except ValueError:
        return None


def average(values):
    clean_values = [value for value in values if value is not None]
    if len(clean_values) == 0:
        return ""
    return round(sum(clean_values) / len(clean_values), 2)


def percent(numerator, denominator):
    if denominator == 0:
        return ""
    return round((numerator / denominator) * 100, 2)


def summarize_group(rows, group_values):
    total_trials = len(rows)

    successful_trials = sum(1 for row in rows if safe_int(row.get("success")) == 1)
    failed_trials = sum(1 for row in rows if safe_int(row.get("success")) == 0)

    caught_trials = sum(1 for row in rows if safe_int(row.get("caught")) == 1)
    dump_success_trials = sum(1 for row in rows if safe_int(row.get("dump_success")) == 1)

    missing_accuracy_trials = sum(1 for row in rows if row.get("accuracy_available") == "no")

    accuracy_values = [
        safe_float(row.get("accuracy_percent_for_analysis"))
        for row in rows
    ]

    raw_accuracy_values = [
        safe_float(row.get("accuracy_percent"))
        for row in rows
    ]

    endpoint_error_values = [
        safe_float(row.get("endpoint_error"))
        for row in rows
    ]

    trail_point_values = [
        safe_float(row.get("trail_point_count"))
        for row in rows
    ]

    summary = dict(group_values)

    summary.update({
        "total_trials": total_trials,
        "successful_trials": successful_trials,
        "failed_trials": failed_trials,
        "success_rate_percent": percent(successful_trials, total_trials),
        "failure_rate_percent": percent(failed_trials, total_trials),

        "caught_trials": caught_trials,
        "catch_rate_percent": percent(caught_trials, total_trials),

        "dump_success_trials": dump_success_trials,
        "dump_success_rate_percent": percent(dump_success_trials, total_trials),

        "avg_accuracy_percent_for_analysis": average(accuracy_values),
        "avg_raw_accuracy_percent": average(raw_accuracy_values),
        "missing_accuracy_trials": missing_accuracy_trials,

        "avg_endpoint_error": average(endpoint_error_values),
        "avg_trail_point_count": average(trail_point_values)
    })

    return summary


def create_summary(rows, group_columns, output_path):
    grouped_rows = defaultdict(list)

    for row in rows:
        key = tuple(row.get(column, "") for column in group_columns)
        grouped_rows[key].append(row)

    summary_rows = []

    for key, group_rows in grouped_rows.items():
        group_values = {
            group_columns[index]: key[index]
            for index in range(len(group_columns))
        }

        summary_rows.append(summarize_group(group_rows, group_values))

    summary_rows = sorted(
        summary_rows,
        key=lambda row: tuple(row.get(column, "") for column in group_columns)
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if summary_rows:
        fieldnames = list(summary_rows[0].keys())

        with open(output_path, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(summary_rows)

    print(f"Created: {output_path}")
    print(f"Rows written: {len(summary_rows)}")
    print()


if not input_path.exists():
    print(f"ERROR: Cleaned input file not found: {input_path}")
    raise SystemExit


with open(input_path, "r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)


print("Creating KPI summary tables...")
print(f"Input rows read: {len(rows)}")
print()

# One row per session/test file
create_summary(
    rows,
    ["session_id", "tester_id", "mode", "level", "attempt_number"],
    session_summary_path
)

# One row per mode and level
create_summary(
    rows,
    ["mode", "level"],
    mode_level_summary_path
)

# One row per tester and mode
create_summary(
    rows,
    ["tester_id", "mode"],
    tester_mode_summary_path
)

# One row per tester, mode, level, and attempt
create_summary(
    rows,
    ["tester_id", "mode", "level", "attempt_number"],
    attempt_summary_path
)

print("Phase 5 completed successfully.")