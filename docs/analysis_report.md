# Stroke Rehabilitation Fixed Game Performance Analysis Report

## Project Overview

This analysis evaluates performance data from a fixed-game stroke rehabilitation exergame. The dataset includes trial-level results from two testers across horizontal, vertical, and diagonal game modes. Each tester completed multiple levels and repeated attempts, allowing performance to be compared by tester, mode, level, and attempt.

## Dataset Summary

| Metric | Value |
|---|---:|
| Total Trial Rows | 600 |
| Total Sessions | 60 |
| Total Testers | 2 |
| Total Game Modes | 3 |
| Successful Trials | 484 |
| Failed Trials | 116 |
| Overall Success Rate | 80.67% |
| Overall Failure Rate | 19.33% |
| Overall Catch Rate | 87.17% |
| Overall Dump Success Rate | 80.67% |
| Average Accuracy for Analysis | 68.64% |
| Average Endpoint Error | 53.62 |
| Average Trail Point Count | 85.61 |

## Mode-Level Performance

| mode       |   total_trials |   success_rate_percent |   avg_accuracy_percent |   catch_rate_percent |   dump_success_rate_percent |   avg_endpoint_error |
|:-----------|---------------:|-----------------------:|-----------------------:|---------------------:|----------------------------:|---------------------:|
| diagonal   |            200 |                   78.5 |                  68.15 |                 86   |                        78.5 |                61.4  |
| horizontal |            200 |                   81   |                  68.73 |                 86.5 |                        81   |                68.69 |
| vertical   |            200 |                   82.5 |                  69.04 |                 89   |                        82.5 |                30.76 |

## Level-Level Performance

|   level |   total_trials |   success_rate_percent |   avg_accuracy_percent |
|--------:|---------------:|-----------------------:|-----------------------:|
|       1 |            120 |                  94.17 |                  80.12 |
|       2 |            120 |                  90    |                  78.85 |
|       3 |            120 |                  84.17 |                  70.05 |
|       4 |            120 |                  70.83 |                  60.41 |
|       5 |            120 |                  64.17 |                  53.78 |

## Tester-Level Performance

| tester_id   |   total_trials |   success_rate_percent |   avg_accuracy_percent |   catch_rate_percent |   dump_success_rate_percent |
|:------------|---------------:|-----------------------:|-----------------------:|---------------------:|----------------------------:|
| T1          |            300 |                  81.67 |                  69.99 |                87    |                       81.67 |
| T2          |            300 |                  79.67 |                  67.3  |                87.33 |                       79.67 |

## Attempt-Level Performance

|   attempt_number |   total_trials |   success_rate_percent |   avg_accuracy_percent |
|-----------------:|---------------:|-----------------------:|-----------------------:|
|                1 |            300 |                  77.33 |                  67.36 |
|                2 |            300 |                  84    |                  69.92 |

## Key Findings

1. The highest-performing game mode was **vertical**, with a success rate of **82.5%**.

2. The lowest-performing game mode was **diagonal**, with a success rate of **78.5%**.

3. The easiest level based on success rate was **Level 1**, with a success rate of **94.17%**.

4. The hardest level based on success rate was **Level 5**, with a success rate of **64.17%**.

5. The strongest tester based on success rate was **T1**, with a success rate of **81.67%**.

6. The hardest mode-level combination was **diagonal Level 4**, with a success rate of **60.0%**.

7. Attempt 1 success rate was **77.33%**, while Attempt 2 success rate was **84.0%**. The change from Attempt 1 to Attempt 2 was **6.67 percentage points**.

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
