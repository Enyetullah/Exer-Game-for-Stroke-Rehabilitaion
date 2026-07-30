# Project Summary

## Project Title

Stroke Rehabilitation Fixed Game Performance Analysis

## Project Purpose

This project analyzes trial-level performance data from a computer-vision stroke rehabilitation exergame. The goal is to evaluate user performance across movement modes, difficulty levels, testers, and repeated attempts.

The project turns raw gameplay session files into analysis-ready datasets, summary tables, charts, SQL queries, and a Power BI dashboard.

## Tools Used

- Python
- PostgreSQL
- SQL
- Power BI
- CSV data processing
- GitHub documentation

## Dataset Overview

The cleaned dataset contains:

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

## Game Modes

The analysis includes three fixed-game movement modes:

- Horizontal
- Vertical
- Diagonal

## Difficulty Levels

Each mode includes five difficulty levels:

- Level 1
- Level 2
- Level 3
- Level 4
- Level 5

## Testers

The project uses anonymous tester identifiers:

- T1
- T2

This protects tester privacy while still allowing performance comparison.

## Data Processing Workflow

### 1. File Inventory

A file inventory was created to document all raw session files and history files.

### 2. Session Metadata

A session metadata file was created to label each session file with:

- tester ID
- game mode
- difficulty level
- attempt number
- game version
- include/exclude status

### 3. Master Trial Dataset

All individual session CSV files were combined into one master trial-level dataset.

Each row in the master dataset represents one trial.

### 4. Data Cleaning and Validation

The dataset was validated for:

- missing session IDs
- missing tester IDs
- invalid game modes
- invalid levels
- invalid attempt numbers
- invalid success values
- level and difficulty mismatches
- mode and game type mismatches
- duplicate session/trial pairs

The validation process found:

- 0 rows with data quality issues
- 0 duplicate session/trial pairs
- 77 rows with missing raw accuracy values

The missing raw accuracy values appeared in failed trials, so an analysis-ready accuracy field was created.

### 5. KPI Summary Tables

Summary tables were created to support dashboard and analysis work.

The summary tables include:

- session-level summary
- mode and level summary
- tester and mode summary
- attempt-level summary

### 6. Python Exploratory Data Analysis

Python was used to calculate key metrics, generate charts, and create an analysis report.

The Python analysis focused on:

- success rate
- average accuracy
- catch rate
- dump success rate
- endpoint error
- tester performance
- mode difficulty
- level difficulty
- repeated-attempt improvement

### 7. SQL Analysis

PostgreSQL was used to validate the imported dataset and answer analysis questions.

The SQL analysis includes queries for:

- overall KPI summary
- success rate by mode
- success rate by level
- tester performance
- attempt improvement
- failure analysis by zone
- hardest mode-level combination
- easiest mode-level combination
- performance ranking

### 8. Power BI Dashboard

A Power BI dashboard was created to visualize the main performance metrics.

The dashboard includes:

- KPI cards
- success rate by mode
- success rate by level
- tester comparison
- attempt comparison
- mode and level matrix
- detailed session/trial table
- filters for tester, mode, level, and attempt

## Key Findings

1. The overall success rate was 80.67%.

2. The highest-performing game mode was vertical, with a success rate of 82.5%.

3. The lowest-performing game mode was diagonal, with a success rate of 78.5%.

4. Level 1 was the easiest level, with a success rate of 94.17%.

5. Level 5 was the hardest level, with a success rate of 64.17%.

6. Tester T1 had a slightly higher success rate than Tester T2.

7. Attempt 2 performed better than Attempt 1.

8. Attempt 1 had a success rate of 77.33%, while Attempt 2 had a success rate of 84.00%.

9. The improvement from Attempt 1 to Attempt 2 was 6.67 percentage points.

## Research Value

This analysis shows how gameplay data from a rehabilitation-focused exergame can be transformed into useful performance metrics.

The project helps evaluate:

- task difficulty
- user performance
- movement-mode differences
- improvement across repeated attempts
- system consistency
- tracking-related trial behavior

## Portfolio Value

This project demonstrates practical data analytics skills, including:

- organizing raw data
- creating metadata
- combining multiple CSV files
- cleaning and validating data
- creating KPI summary tables
- performing exploratory data analysis
- writing SQL analysis queries
- building dashboards
- writing project documentation
- communicating insights clearly

## Final Summary

This project demonstrates an end-to-end data analytics workflow using real application-generated data from a computer-vision rehabilitation game. It shows how raw session logs can be turned into clean datasets, performance metrics, SQL analysis, dashboard visuals, and actionable findings.