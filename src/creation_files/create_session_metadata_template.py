from pathlib import Path
import csv

# This assumes this file is inside:
# D:\ExerGame V 2.0\src\creation_files\
# parents[2] goes back to:
# D:\ExerGame V 2.0
project_root = Path(__file__).resolve().parents[2]

inventory_path = project_root / "data" / "metadata" / "file_inventory.csv"
output_path = project_root / "data" / "metadata" / "session_metadata.csv"

records = []

if not inventory_path.exists():
    print(f"ERROR: file_inventory.csv not found at: {inventory_path}")
else:
    with open(inventory_path, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            file_type = row["file_type"].lower()

            # Only session CSV files should go into session metadata.
            # JSON history files are not individual session files.
            if file_type == "csv":
                file_name = row["file_name"]
                session_id = file_name.replace(".csv", "")

                records.append({
                    "session_id": session_id,
                    "file_name": file_name,
                    "relative_path": row["relative_path"],
                    "tester_id": "",
                    "mode": row["mode"],
                    "level": "",
                    "attempt_number": "",
                    "game_version": "fixed",
                    "include_in_analysis": "yes",
                    "notes": ""
                })

    records = sorted(records, key=lambda x: (x["mode"], x["file_name"]))

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as outfile:
        fieldnames = [
            "session_id",
            "file_name",
            "relative_path",
            "tester_id",
            "mode",
            "level",
            "attempt_number",
            "game_version",
            "include_in_analysis",
            "notes"
        ]

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Session metadata template created successfully: {output_path}")
    print(f"Total session CSV files added: {len(records)}")