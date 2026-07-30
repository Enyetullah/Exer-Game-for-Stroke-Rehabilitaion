from pathlib import Path
import csv
from datetime import datetime


# This assumes this file is inside:
# D:\ExerGame V 2.0\src\creation_files\
# parents[2] goes back to:
# D:\ExerGame V 2.0
project_root = Path(__file__).resolve().parents[2]

metadata_path = project_root / "data" / "metadata" / "session_metadata.csv"
output_path = project_root / "data" / "processed" / "fixed_game_trial_results.csv"


def safe_float(value):
    try:
        if value is None or value == "":
            return ""
        return float(value)
    except ValueError:
        return ""


def safe_int(value):
    try:
        if value is None or value == "":
            return ""
        return int(float(value))
    except ValueError:
        return ""


def count_trail_points(trail_value):
    if trail_value is None or trail_value.strip() == "":
        return 0

    points = trail_value.split(";")
    points = [point for point in points if point.strip() != ""]
    return len(points)


def convert_timestamp(timestamp_value):
    try:
        timestamp_float = float(timestamp_value)
        return datetime.fromtimestamp(timestamp_float).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ""


records = []
missing_files = []
total_files_read = 0

if not metadata_path.exists():
    print(f"ERROR: Metadata file not found: {metadata_path}")
else:
    with open(metadata_path, "r", encoding="utf-8") as metadata_file:
        metadata_reader = csv.DictReader(metadata_file)

        for metadata_row in metadata_reader:
            include_value = metadata_row["include_in_analysis"].strip().lower()

            if include_value != "yes":
                continue

            relative_path = metadata_row["relative_path"]
            session_file_path = project_root / relative_path

            if not session_file_path.exists():
                missing_files.append(str(session_file_path))
                continue

            total_files_read += 1

            with open(session_file_path, "r", encoding="utf-8") as session_file:
                session_reader = csv.DictReader(session_file)

                for trial_row in session_reader:
                    ball_x = safe_float(trial_row.get("ball_x", ""))
                    cup_x = safe_float(trial_row.get("cup_x", ""))

                    if ball_x != "" and cup_x != "":
                        endpoint_error = abs(ball_x - cup_x)
                    else:
                        endpoint_error = ""

                    accuracy = safe_float(trial_row.get("accuracy", ""))

                    if accuracy != "":
                        accuracy_percent = accuracy * 100
                    else:
                        accuracy_percent = ""

                    record = {
                        "session_id": metadata_row["session_id"],
                        "file_name": metadata_row["file_name"],
                        "tester_id": metadata_row["tester_id"],
                        "mode": metadata_row["mode"],
                        "level": metadata_row["level"],
                        "attempt_number": metadata_row["attempt_number"],
                        "game_version": metadata_row["game_version"],

                        "timestamp": trial_row.get("timestamp", ""),
                        "timestamp_readable": convert_timestamp(trial_row.get("timestamp", "")),
                        "trial": trial_row.get("trial", ""),
                        "ball_x": trial_row.get("ball_x", ""),
                        "cup_x": trial_row.get("cup_x", ""),
                        "endpoint_error": endpoint_error,
                        "zone": trial_row.get("zone", ""),
                        "caught": trial_row.get("caught", ""),
                        "dump_success": trial_row.get("dump_success", ""),
                        "success": trial_row.get("success", ""),
                        "difficulty": trial_row.get("difficulty", ""),
                        "game_type": trial_row.get("game_type", ""),
                        "accuracy": accuracy,
                        "accuracy_percent": accuracy_percent,
                        "trail_point_count": count_trail_points(trial_row.get("trail", "")),
                        "trail": trial_row.get("trail", "")
                    }

                    records.append(record)


output_path.parent.mkdir(parents=True, exist_ok=True)

fieldnames = [
    "session_id",
    "file_name",
    "tester_id",
    "mode",
    "level",
    "attempt_number",
    "game_version",
    "timestamp",
    "timestamp_readable",
    "trial",
    "ball_x",
    "cup_x",
    "endpoint_error",
    "zone",
    "caught",
    "dump_success",
    "success",
    "difficulty",
    "game_type",
    "accuracy",
    "accuracy_percent",
    "trail_point_count",
    "trail"
]

with open(output_path, "w", newline="", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print("Master trial-level dataset created successfully.")
print(f"Output file: {output_path}")
print(f"Session files read: {total_files_read}")
print(f"Total trial rows created: {len(records)}")

if missing_files:
    print()
    print("WARNING: Some files were listed in metadata but were not found:")
    for file in missing_files:
        print(file)
else:
    print("No missing files found.")