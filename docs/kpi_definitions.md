# KPI Definitions

This document defines the key performance indicators used in the stroke rehabilitation fixed-game analysis.

## Total Trials

The total number of trial-level records in the cleaned dataset.

Formula:

```text
Total Trials = Count of all trial rows
```

## Total Sessions

The number of unique session files analyzed.

Formula:

```text
Total Sessions = Count of distinct session_id values
```

## Total Testers

The number of anonymous testers included in the analysis.

Formula:

```text
Total Testers = Count of distinct tester_id values
```

## Total Game Modes

The number of movement modes included in the analysis.

Formula:

```text
Total Game Modes = Count of distinct mode values
```

## Successful Trials

The number of trials where the user successfully completed the task.

Formula:

```text
Successful Trials = Count of rows where success = 1
```

## Failed Trials

The number of trials where the user did not successfully complete the task.

Formula:

```text
Failed Trials = Count of rows where success = 0
```

or:

```text
Failed Trials = Total Trials - Successful Trials
```

## Success Rate

The percentage of trials completed successfully.

Formula:

```text
Success Rate = Successful Trials / Total Trials
```

Example:

```text
Success Rate = 484 / 600 = 80.67%
```

## Failure Rate

The percentage of trials that failed.

Formula:

```text
Failure Rate = Failed Trials / Total Trials
```

Example:

```text
Failure Rate = 116 / 600 = 19.33%
```

## Catch Rate

The percentage of trials where the ball was caught.

Formula:

```text
Catch Rate = Caught Trials / Total Trials
```

## Dump Success Rate

The percentage of trials where the dump action was successful.

Formula:

```text
Dump Success Rate = Dump Successful Trials / Total Trials
```

## Average Accuracy

The average value of `accuracy_percent_for_analysis`.

Formula:

```text
Average Accuracy = Average of accuracy_percent_for_analysis
```

Important note:

Some failed trials had missing raw accuracy values. For analysis and dashboard purposes, those missing failed-trial accuracy values were treated as 0 in `accuracy_percent_for_analysis`.

This prevents failed trials from being ignored in average accuracy calculations.

## Raw Average Accuracy

The average of the original `accuracy_percent` field.

This only uses trials where raw accuracy was available.

## Average Endpoint Error

The average distance between the ball x-coordinate and the cup x-coordinate.

Formula:

```text
Endpoint Error = ABS(ball_x - cup_x)
```

A lower endpoint error generally means the ball and cup positions were closer together.

## Average Trail Point Count

The average number of recorded movement trail points per trial.

Formula:

```text
Average Trail Point Count = Average of trail_point_count
```

This helps describe how much movement tracking data was recorded during each trial.

## Performance Band

A category created from trial success and accuracy.

Example categories:

```text
Excellent
Strong
Moderate
Needs Improvement
Low Accuracy
Failed Trial
Unknown
```

## Attempt Improvement

The change in success rate between Attempt 1 and Attempt 2.

Formula:

```text
Attempt Improvement = Attempt 2 Success Rate - Attempt 1 Success Rate
```

Example:

```text
Attempt Improvement = 84.00% - 77.33% = 6.67 percentage points
```

## Mode-Level Difficulty

A comparison of success rate and accuracy across each game mode and level.

This helps identify which movement tasks were easiest or hardest.