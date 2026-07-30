from pathlib import Path
import csv
from collections import Counter


# This assumes this file is inside:
# D:\ExerGame V 2.0\src\creation_files\
# parents[2] goes back to:
# D:\ExerGame V 2.0
project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "data" / "processed" / "fixed_game_trial_results.csv"
cleaned_output_path = project_root / "data" / "processed" / "fixed_game_trial_results_cleaned.csv"
issues_output_path = project_root / "data" / "processed" / "data_quality_issues.csv"
report_output_path = project_root / "data" / "processed" / "data_quality_report.txt"


def is_blank(value):
    return value is None or str(value).strip() == ""


def safe_int(value):
    try:
        if is_blank(value):
            return None
        return int(float(value))
    except ValueError:
        return None


def safe_float(value):
    try:
        if is_blank(value):
            return None
        return float(value)
    except ValueError:
        return None


def make_label(value, prefix):
    if value is None:
        return "Unknown"
    return f"{prefix} {value}"


def success_label(value):
    if value == 1:
        return "Success"
    if value == 0:
        return "Failure"
    return "Unknown"


def yes_no_label(value):
    if value == 1:
        return "Yes"
    if value == 0:
        return "No"
    return "Unknown"


def performance_band(success, accuracy_percent_for_analysis):
    if success == 0:
        return "Failed Trial"

    if accuracy_percent_for_analysis is None:
        return "Unknown"

    if accuracy_percent_for_analysis >= 90:
        return "Excellent"
    elif accuracy_percent_for_analysis >= 80:
        return "Strong"
    elif accuracy_percent_for_analysis >= 70:
        return "Moderate"
    elif accuracy_percent_for_analysis >= 60:
        return "Needs Improvement"
    else:
        return "Low Accuracy"


if not input_path.exists():
    print(f"ERROR: Input file not found: {input_path}")
    raise SystemExit


with open(input_path, "r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)


cleaned_rows = []
issue_rows = []

for row in rows:
    issues = []

    session_id = row.get("session_id", "")
    tester_id = row.get("tester_id", "")
    mode = row.get("mode", "")
    game_type = row.get("game_type", "")

    level = safe_int(row.get("level", ""))
    attempt_number = safe_int(row.get("attempt_number", ""))
    trial = safe_int(row.get("trial", ""))
    difficulty = safe_int(row.get("difficulty", ""))

    caught = safe_int(row.get("caught", ""))
    dump_success = safe_int(row.get("dump_success", ""))
    success = safe_int(row.get("success", ""))

    accuracy = safe_float(row.get("accuracy", ""))
    accuracy_percent = safe_float(row.get("accuracy_percent", ""))
    endpoint_error = safe_float(row.get("endpoint_error", ""))
    trail_point_count = safe_int(row.get("trail_point_count", ""))
    trail = row.get("trail", "")

    # Basic required-field checks
    if is_blank(session_id):
        issues.append("missing_session_id")

    if is_blank(tester_id):
        issues.append("missing_tester_id")

    if is_blank(mode):
        issues.append("missing_mode")

    if level is None:
        issues.append("missing_level")

    if attempt_number is None:
        issues.append("missing_attempt_number")

    if trial is None:
        issues.append("missing_trial")

    # Valid value checks
    if mode not in ["horizontal", "vertical", "diagonal"]:
        issues.append("invalid_mode")

    if tester_id not in ["T1", "T2"]:
        issues.append("invalid_tester_id")

    if level not in [1, 2, 3, 4, 5]:
        issues.append("invalid_level")

    if attempt_number not in [1, 2]:
        issues.append("invalid_attempt_number")

    if trial is not None and trial < 1:
        issues.append("invalid_trial_number")

    if caught not in [0, 1]:
        issues.append("invalid_caught_value")

    if dump_success not in [0, 1]:
        issues.append("invalid_dump_success_value")

    if success not in [0, 1]:
        issues.append("invalid_success_value")

    # Level and difficulty should match
    if level is not None and difficulty is not None and level != difficulty:
        issues.append("level_difficulty_mismatch")

    # Game type should match mode
    expected_game_type = f"{mode}_fixed"
    if not is_blank(mode) and game_type != expected_game_type:
        issues.append("mode_game_type_mismatch")

    # Accuracy should be between 0 and 1 when available
    if accuracy is not None and not (0 <= accuracy <= 1):
        issues.append("accuracy_out_of_range")

    # Accuracy percent should be between 0 and 100 when available
    if accuracy_percent is not None and not (0 <= accuracy_percent <= 100):
        issues.append("accuracy_percent_out_of_range")

    # Endpoint error should not be negative
    if endpoint_error is not None and endpoint_error < 0:
        issues.append("negative_endpoint_error")

    # Trail point count should not be negative
    if trail_point_count is not None and trail_point_count < 0:
        issues.append("negative_trail_point_count")

    # If the trial succeeded, accuracy and trail should usually exist
    if success == 1 and accuracy_percent is None:
        issues.append("successful_trial_missing_accuracy")

    if success == 1 and is_blank(trail):
        issues.append("successful_trial_missing_trail")

    # Create analysis-friendly accuracy field
    # Important:
    # - Raw accuracy can be blank for failed trials.
    # - For dashboard analysis, failed trials should count as 0 accuracy
    #   in an overall performance score.
    if accuracy_percent is not None:
        accuracy_percent_for_analysis = accuracy_percent
    elif success == 0:
        accuracy_percent_for_analysis = 0
    else:
        accuracy_percent_for_analysis = None

    row["mode_label"] = mode.capitalize() if not is_blank(mode) else "Unknown"
    row["level_label"] = make_label(level, "Level")
    row["attempt_label"] = make_label(attempt_number, "Attempt")
    row["success_label"] = success_label(success)
    row["caught_label"] = yes_no_label(caught)
    row["dump_success_label"] = yes_no_label(dump_success)

    row["accuracy_available"] = "yes" if accuracy_percent is not None else "no"
    row["accuracy_percent_for_analysis"] = "" if accuracy_percent_for_analysis is None else round(accuracy_percent_for_analysis, 2)
    row["performance_band"] = performance_band(success, accuracy_percent_for_analysis)

    row["data_quality_issue_count"] = len(issues)
    row["data_quality_issues"] = "; ".join(issues)

    cleaned_rows.append(row)

    if issues:
        issue_rows.append(row)


# Check duplicate session/trial combinations
session_trial_pairs = []
for row in cleaned_rows:
    session_trial_pairs.append((row["session_id"], row["trial"]))

duplicate_pairs = [
    pair for pair, count in Counter(session_trial_pairs).items()
    if count > 1
]


# Write cleaned file
cleaned_output_path.parent.mkdir(parents=True, exist_ok=True)

fieldnames = list(cleaned_rows[0].keys())

with open(cleaned_output_path, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cleaned_rows)


# Write issue file
with open(issues_output_path, "w", newline="", encoding="utf-8") as issuefile:
    writer = csv.DictWriter(issuefile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(issue_rows)


# Summary numbers
total_rows = len(cleaned_rows)
total_sessions = len(set(row["session_id"] for row in cleaned_rows))
total_testers = len(set(row["tester_id"] for row in cleaned_rows))
total_modes = len(set(row["mode"] for row in cleaned_rows))

mode_counts = Counter(row["mode"] for row in cleaned_rows)
tester_counts = Counter(row["tester_id"] for row in cleaned_rows)
success_counts = Counter(row["success_label"] for row in cleaned_rows)
missing_accuracy_count = sum(1 for row in cleaned_rows if row["accuracy_available"] == "no")
issue_count = len(issue_rows)

report_lines = []

report_lines.append("Stroke Rehabilitation Fixed Game Data Quality Report")
report_lines.append("=" * 60)
report_lines.append("")
report_lines.append(f"Input file: {input_path}")
report_lines.append(f"Cleaned output file: {cleaned_output_path}")
report_lines.append(f"Issues output file: {issues_output_path}")
report_lines.append("")
report_lines.append("Dataset Overview")
report_lines.append("-" * 60)
report_lines.append(f"Total trial rows: {total_rows}")
report_lines.append(f"Total sessions: {total_sessions}")
report_lines.append(f"Total testers: {total_testers}")
report_lines.append(f"Total modes: {total_modes}")
report_lines.append("")
report_lines.append("Rows by Mode")
report_lines.append("-" * 60)
for key, value in sorted(mode_counts.items()):
    report_lines.append(f"{key}: {value}")

report_lines.append("")
report_lines.append("Rows by Tester")
report_lines.append("-" * 60)
for key, value in sorted(tester_counts.items()):
    report_lines.append(f"{key}: {value}")

report_lines.append("")
report_lines.append("Success / Failure Counts")
report_lines.append("-" * 60)
for key, value in sorted(success_counts.items()):
    report_lines.append(f"{key}: {value}")

report_lines.append("")
report_lines.append("Data Quality Checks")
report_lines.append("-" * 60)
report_lines.append(f"Rows missing raw accuracy: {missing_accuracy_count}")
report_lines.append(f"Rows with data quality issues: {issue_count}")
report_lines.append(f"Duplicate session_id + trial pairs: {len(duplicate_pairs)}")

if duplicate_pairs:
    report_lines.append("")
    report_lines.append("Duplicate session/trial pairs:")
    for pair in duplicate_pairs:
        report_lines.append(str(pair))

report_lines.append("")
report_lines.append("Important Note")
report_lines.append("-" * 60)
report_lines.append(
    "Missing raw accuracy is acceptable for failed trials where caught = 0, "
    "dump_success = 0, and success = 0. For dashboard analysis, the cleaned file "
    "adds accuracy_percent_for_analysis, which treats failed trials with missing "
    "accuracy as 0."
)

with open(report_output_path, "w", encoding="utf-8") as reportfile:
    reportfile.write("\n".join(report_lines))


print("Phase 4 completed successfully.")
print(f"Rows read: {total_rows}")
print(f"Sessions found: {total_sessions}")
print(f"Modes found: {total_modes}")
print(f"Rows missing raw accuracy: {missing_accuracy_count}")
print(f"Rows with data quality issues: {issue_count}")
print(f"Duplicate session_id + trial pairs: {len(duplicate_pairs)}")
print()
print(f"Cleaned file created: {cleaned_output_path}")
print(f"Issue file created: {issues_output_path}")
print(f"Report created: {report_output_path}")