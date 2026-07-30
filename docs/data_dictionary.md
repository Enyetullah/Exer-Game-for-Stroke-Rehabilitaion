# Data Dictionary

This document describes the main fields used in the stroke rehabilitation fixed-game analysis dataset.

## Dataset

Main cleaned dataset:

`data/processed/fixed_game_trial_results_cleaned.csv`

Each row represents one trial from the fixed-game version of the stroke rehabilitation exergame.

## Column Definitions

| Column | Description |
|---|---|
| session_id | Unique identifier for each session file. |
| file_name | Original raw CSV file name. |
| tester_id | Anonymous tester identifier. Example: T1 or T2. |
| mode | Game movement mode. Values include horizontal, vertical, and diagonal. |
| level | Difficulty level from 1 to 5. |
| attempt_number | Attempt number for the same tester, mode, and level. |
| game_version | Version of the game used in the analysis. |
| timestamp | Raw timestamp recorded during the trial. |
| timestamp_readable | Human-readable timestamp created during preprocessing. |
| trial | Trial number within the session. |
| ball_x | Ball x-coordinate recorded during the trial. |
| cup_x | Cup x-coordinate recorded during the trial. |
| endpoint_error | Absolute difference between ball_x and cup_x. |
| zone | Target zone used during the trial. |
| caught | Indicates whether the ball was caught. 1 = yes, 0 = no. |
| dump_success | Indicates whether the dump action was successful. 1 = yes, 0 = no. |
| success | Overall trial result. 1 = success, 0 = failure. |
| difficulty | Difficulty value recorded by the game. |
| game_type | Fixed-game type, such as horizontal_fixed, vertical_fixed, or diagonal_fixed. |
| accuracy | Raw accuracy value when available. |
| accuracy_percent | Raw accuracy value converted to a percentage. |
| trail_point_count | Number of recorded movement trail points for the trial. |
| trail | Raw movement trail coordinate string. |
| mode_label | Clean display label for the movement mode. |
| level_label | Clean display label for the difficulty level. |
| attempt_label | Clean display label for the attempt number. |
| success_label | Text label showing Success or Failure. |
| caught_label | Text label showing whether the ball was caught. |
| dump_success_label | Text label showing whether the dump action was successful. |
| accuracy_available | Indicates whether raw accuracy was available. |
| accuracy_percent_for_analysis | Analysis-ready accuracy value. Failed trials with missing raw accuracy are treated as 0. |
| performance_band | Categorized performance level based on success and accuracy. |
| data_quality_issue_count | Number of detected data quality issues for the row. |
| data_quality_issues | Description of detected data quality issues, if any. |

## Notes

The field `accuracy_percent_for_analysis` is used for dashboard and analysis purposes. Some failed trials had missing raw accuracy values. Instead of allowing those failed trials to be ignored in averages, missing accuracy values for failed trials were treated as 0.

This makes the analysis more honest because failed trials are still counted in the overall performance metrics.