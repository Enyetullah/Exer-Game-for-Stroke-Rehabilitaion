from pathlib import Path
import csv

# This finds the main project folder.
# Since this file is inside src/creation_files,
# parents[2] goes back to: D:\ExerGame V 2.0
project_root = Path(__file__).resolve().parents[2]

raw_data_path = project_root / "data" / "raw"
output_path = project_root / "data" / "metadata" / "file_inventory.csv"

records = []

if not raw_data_path.exists():
    print(f"ERROR: Raw data folder not found: {raw_data_path}")
    print("Make sure your folders look like this:")
    print("data/raw/horizontal")
    print("data/raw/vertical")
    print("data/raw/diagonal")
else:
    for mode_folder in raw_data_path.iterdir():
        if mode_folder.is_dir():
            mode = mode_folder.name

            for file in mode_folder.iterdir():
                if file.is_file():
                    if file.suffix.lower() == ".csv":
                        notes = "raw session file"
                    elif file.suffix.lower() == ".json":
                        notes = "history file"
                    else:
                        notes = "other file"

                    records.append({
                        "file_name": file.name,
                        "mode": mode,
                        "file_type": file.suffix.replace(".", ""),
                        "relative_path": str(file.relative_to(project_root)),
                        "notes": notes
                    })

    records = sorted(records, key=lambda x: (x["mode"], x["file_type"], x["file_name"]))

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["file_name", "mode", "file_type", "relative_path", "notes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(records)

    print(f"File inventory created successfully: {output_path}")
    print(f"Total files found: {len(records)}")