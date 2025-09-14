import os
import pandas as pd
import json
from collections import defaultdict

# ---- Configuration ----
data_dir = "data"  # folder where all user folders are stored
testers = ["Enyet(tester)", "Thirta(tester)"]  # replace with your actual tester folder names
max_trials = 10  # trials per session

# ---- Data storage ----
average_scores = defaultdict(lambda: defaultdict(dict))

# ---- Process each tester ----
for tester in testers:
    tester_path = os.path.join(data_dir, tester)
    if not os.path.isdir(tester_path):
        continue

    for filename in os.listdir(tester_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(tester_path, filename)
            df = pd.read_csv(filepath)

            if df.empty or "success" not in df.columns or "difficulty" not in df.columns or "game_type" not in df.columns:
                continue

            game_type = df["game_type"].iloc[0]
            level = int(df["difficulty"].iloc[0])
            success_count = df["success"].sum()

            if level not in average_scores[game_type]:
                average_scores[game_type][level] = {"total_success": 0, "session_count": 0}

            average_scores[game_type][level]["total_success"] += success_count
            average_scores[game_type][level]["session_count"] += 1

# ---- Final formatting ----
for game_type in average_scores:
    for level in average_scores[game_type]:
        data = average_scores[game_type][level]
        avg = data["total_success"] / data["session_count"]
        average_scores[game_type][level] = round(avg, 2)

# ---- Save as JSON ----
benchmark_path = os.path.join("D:/TruScholars Project/data/testAverage", "healthy_benchmarks.json")
with open(benchmark_path, "w") as f:
    json.dump(average_scores, f, indent=4)

print("✅ Benchmarks for all game modes saved to healthy_benchmarks.json.")
