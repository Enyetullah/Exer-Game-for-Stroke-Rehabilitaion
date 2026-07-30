from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# This assumes this file is inside:
# D:\ExerGame V 2.0\src\creation_files\
# parents[2] goes back to:
# D:\ExerGame V 2.0
project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "data" / "processed" / "fixed_game_trial_results_cleaned.csv"

charts_folder = project_root / "dashboard" / "screenshots"
report_path = project_root / "docs" / "analysis_report.md"

charts_folder.mkdir(parents=True, exist_ok=True)
report_path.parent.mkdir(parents=True, exist_ok=True)


def save_bar_chart(data, x_col, y_col, title, xlabel, ylabel, output_file):
    plt.figure(figsize=(9, 5))
    plt.bar(data[x_col].astype(str), data[y_col])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()


def save_line_chart(data, x_col, y_col, title, xlabel, ylabel, output_file):
    plt.figure(figsize=(9, 5))
    plt.plot(data[x_col].astype(str), data[y_col], marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()


if not input_path.exists():
    print(f"ERROR: Input file not found: {input_path}")
    raise SystemExit


df = pd.read_csv(input_path)

# Convert important columns to numeric
numeric_columns = [
    "level",
    "attempt_number",
    "trial",
    "caught",
    "dump_success",
    "success",
    "accuracy_percent_for_analysis",
    "endpoint_error",
    "trail_point_count"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")


# =========================
# Overall KPIs
# =========================

total_trials = len(df)
total_sessions = df["session_id"].nunique()
total_testers = df["tester_id"].nunique()
total_modes = df["mode"].nunique()

successful_trials = int(df["success"].sum())
failed_trials = total_trials - successful_trials

overall_success_rate = round(df["success"].mean() * 100, 2)
overall_failure_rate = round(100 - overall_success_rate, 2)
overall_catch_rate = round(df["caught"].mean() * 100, 2)
overall_dump_success_rate = round(df["dump_success"].mean() * 100, 2)
overall_avg_accuracy = round(df["accuracy_percent_for_analysis"].mean(), 2)
overall_avg_endpoint_error = round(df["endpoint_error"].mean(), 2)
overall_avg_trail_points = round(df["trail_point_count"].mean(), 2)


# =========================
# Grouped summaries
# =========================

mode_summary = (
    df.groupby("mode")
    .agg(
        total_trials=("trial", "count"),
        success_rate_percent=("success", lambda x: round(x.mean() * 100, 2)),
        avg_accuracy_percent=("accuracy_percent_for_analysis", lambda x: round(x.mean(), 2)),
        catch_rate_percent=("caught", lambda x: round(x.mean() * 100, 2)),
        dump_success_rate_percent=("dump_success", lambda x: round(x.mean() * 100, 2)),
        avg_endpoint_error=("endpoint_error", lambda x: round(x.mean(), 2))
    )
    .reset_index()
)

level_summary = (
    df.groupby("level")
    .agg(
        total_trials=("trial", "count"),
        success_rate_percent=("success", lambda x: round(x.mean() * 100, 2)),
        avg_accuracy_percent=("accuracy_percent_for_analysis", lambda x: round(x.mean(), 2))
    )
    .reset_index()
    .sort_values("level")
)

tester_summary = (
    df.groupby("tester_id")
    .agg(
        total_trials=("trial", "count"),
        success_rate_percent=("success", lambda x: round(x.mean() * 100, 2)),
        avg_accuracy_percent=("accuracy_percent_for_analysis", lambda x: round(x.mean(), 2)),
        catch_rate_percent=("caught", lambda x: round(x.mean() * 100, 2)),
        dump_success_rate_percent=("dump_success", lambda x: round(x.mean() * 100, 2))
    )
    .reset_index()
)

attempt_summary = (
    df.groupby("attempt_number")
    .agg(
        total_trials=("trial", "count"),
        success_rate_percent=("success", lambda x: round(x.mean() * 100, 2)),
        avg_accuracy_percent=("accuracy_percent_for_analysis", lambda x: round(x.mean(), 2))
    )
    .reset_index()
    .sort_values("attempt_number")
)

mode_level_summary = (
    df.groupby(["mode", "level"])
    .agg(
        total_trials=("trial", "count"),
        success_rate_percent=("success", lambda x: round(x.mean() * 100, 2)),
        avg_accuracy_percent=("accuracy_percent_for_analysis", lambda x: round(x.mean(), 2))
    )
    .reset_index()
    .sort_values(["mode", "level"])
)


# =========================
# Save charts
# =========================

save_bar_chart(
    mode_summary.sort_values("success_rate_percent", ascending=False),
    "mode",
    "success_rate_percent",
    "Success Rate by Game Mode",
    "Game Mode",
    "Success Rate (%)",
    charts_folder / "success_rate_by_mode.png"
)

save_bar_chart(
    mode_summary.sort_values("avg_accuracy_percent", ascending=False),
    "mode",
    "avg_accuracy_percent",
    "Average Accuracy by Game Mode",
    "Game Mode",
    "Average Accuracy (%)",
    charts_folder / "average_accuracy_by_mode.png"
)

save_line_chart(
    level_summary,
    "level",
    "success_rate_percent",
    "Success Rate by Level",
    "Level",
    "Success Rate (%)",
    charts_folder / "success_rate_by_level.png"
)

save_bar_chart(
    tester_summary.sort_values("success_rate_percent", ascending=False),
    "tester_id",
    "success_rate_percent",
    "Success Rate by Tester",
    "Tester",
    "Success Rate (%)",
    charts_folder / "success_rate_by_tester.png"
)

save_line_chart(
    attempt_summary,
    "attempt_number",
    "success_rate_percent",
    "Success Rate by Attempt",
    "Attempt Number",
    "Success Rate (%)",
    charts_folder / "attempt_success_rate.png"
)


# =========================
# Create automatic insights
# =========================

best_mode = mode_summary.sort_values("success_rate_percent", ascending=False).iloc[0]
lowest_mode = mode_summary.sort_values("success_rate_percent", ascending=True).iloc[0]

best_level = level_summary.sort_values("success_rate_percent", ascending=False).iloc[0]
lowest_level = level_summary.sort_values("success_rate_percent", ascending=True).iloc[0]

best_tester = tester_summary.sort_values("success_rate_percent", ascending=False).iloc[0]

hardest_mode_level = mode_level_summary.sort_values("success_rate_percent", ascending=True).iloc[0]

if len(attempt_summary) >= 2:
    attempt_1_rate = attempt_summary.loc[attempt_summary["attempt_number"] == 1, "success_rate_percent"].iloc[0]
    attempt_2_rate = attempt_summary.loc[attempt_summary["attempt_number"] == 2, "success_rate_percent"].iloc[0]
    attempt_change = round(attempt_2_rate - attempt_1_rate, 2)
else:
    attempt_1_rate = ""
    attempt_2_rate = ""
    attempt_change = ""


# =========================
# Create Markdown report
# =========================

report = f"""# Stroke Rehabilitation Fixed Game Performance Analysis Report

## Project Overview

This analysis evaluates performance data from a fixed-game stroke rehabilitation exergame. The dataset includes trial-level results from two testers across horizontal, vertical, and diagonal game modes. Each tester completed multiple levels and repeated attempts, allowing performance to be compared by tester, mode, level, and attempt.

## Dataset Summary

| Metric | Value |
|---|---:|
| Total Trial Rows | {total_trials} |
| Total Sessions | {total_sessions} |
| Total Testers | {total_testers} |
| Total Game Modes | {total_modes} |
| Successful Trials | {successful_trials} |
| Failed Trials | {failed_trials} |
| Overall Success Rate | {overall_success_rate}% |
| Overall Failure Rate | {overall_failure_rate}% |
| Overall Catch Rate | {overall_catch_rate}% |
| Overall Dump Success Rate | {overall_dump_success_rate}% |
| Average Accuracy for Analysis | {overall_avg_accuracy}% |
| Average Endpoint Error | {overall_avg_endpoint_error} |
| Average Trail Point Count | {overall_avg_trail_points} |

## Mode-Level Performance

{mode_summary.to_markdown(index=False)}

## Level-Level Performance

{level_summary.to_markdown(index=False)}

## Tester-Level Performance

{tester_summary.to_markdown(index=False)}

## Attempt-Level Performance

{attempt_summary.to_markdown(index=False)}

## Key Findings

1. The highest-performing game mode was **{best_mode["mode"]}**, with a success rate of **{best_mode["success_rate_percent"]}%**.

2. The lowest-performing game mode was **{lowest_mode["mode"]}**, with a success rate of **{lowest_mode["success_rate_percent"]}%**.

3. The easiest level based on success rate was **Level {int(best_level["level"])}**, with a success rate of **{best_level["success_rate_percent"]}%**.

4. The hardest level based on success rate was **Level {int(lowest_level["level"])}**, with a success rate of **{lowest_level["success_rate_percent"]}%**.

5. The strongest tester based on success rate was **{best_tester["tester_id"]}**, with a success rate of **{best_tester["success_rate_percent"]}%**.

6. The hardest mode-level combination was **{hardest_mode_level["mode"]} Level {int(hardest_mode_level["level"])}**, with a success rate of **{hardest_mode_level["success_rate_percent"]}%**.

7. Attempt 1 success rate was **{attempt_1_rate}%**, while Attempt 2 success rate was **{attempt_2_rate}%**. The change from Attempt 1 to Attempt 2 was **{attempt_change} percentage points**.

## Interpretation

The fixed-game data shows how performance changes across game mode, difficulty level, tester, and repeated attempts. Success rate and average accuracy provide the main performance indicators, while catch rate, dump-success rate, endpoint error, and trail point count provide additional context about gameplay behavior and system tracking.

The analysis also separates raw accuracy from analysis-ready accuracy. Failed trials with missing accuracy were treated as 0 in the `accuracy_percent_for_analysis` field. This prevents failed trials from being ignored in dashboard averages and gives a more honest view of overall performance.

## Recommendations

1. Focus future testing on the mode-level combinations with the lowest success rates because those areas likely represent the most difficult movement tasks.

2. Continue tracking success rate, average accuracy, endpoint error, and trail point count because these metrics help evaluate both user performance and system consistency.

3. Use repeated attempts to measure short-term improvement. If success rates increase from Attempt 1 to Attempt 2, the game may be useful for tracking practice-based improvement.

4. Review trials with missing raw accuracy or failed outcomes to determine whether failures are caused by user performance, tracking limitations, or task difficulty.

## Dashboard Suggestions

The following visuals should be included in the final Power BI or Tableau dashboard:

- KPI cards for total trials, total sessions, success rate, average accuracy, catch rate, and dump-success rate
- Bar chart showing success rate by game mode
- Line chart showing success rate by level
- Bar chart comparing tester performance
- Chart comparing Attempt 1 vs Attempt 2
- Table showing mode-level performance
- Filters for tester, mode, level, and attempt number

## Generated Charts

The following charts were created and saved in the dashboard screenshots folder:

- success_rate_by_mode.png
- average_accuracy_by_mode.png
- success_rate_by_level.png
- success_rate_by_tester.png
- attempt_success_rate.png
"""

with open(report_path, "w", encoding="utf-8") as outfile:
    outfile.write(report)


print("Phase 6 completed successfully.")
print(f"Input rows analyzed: {total_trials}")
print(f"Analysis report created: {report_path}")
print(f"Charts folder: {charts_folder}")
print()
print("Charts created:")
print("- success_rate_by_mode.png")
print("- average_accuracy_by_mode.png")
print("- success_rate_by_level.png")
print("- success_rate_by_tester.png")
print("- attempt_success_rate.png")