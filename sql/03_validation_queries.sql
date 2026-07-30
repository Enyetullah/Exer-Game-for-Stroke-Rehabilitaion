-- 1. Check total rows
SELECT COUNT(*) AS total_rows
FROM stroke_rehab.fixed_game_trials;

-- Expected: 600


-- 2. Check total sessions
SELECT COUNT(DISTINCT session_id) AS total_sessions
FROM stroke_rehab.fixed_game_trials;

-- Expected: 60


-- 3. Check rows by mode
SELECT
    mode,
    COUNT(*) AS total_rows
FROM stroke_rehab.fixed_game_trials
GROUP BY mode
ORDER BY mode;

-- Expected:
-- diagonal   200
-- horizontal 200
-- vertical   200


-- 4. Check rows by tester
SELECT
    tester_id,
    COUNT(*) AS total_rows
FROM stroke_rehab.fixed_game_trials
GROUP BY tester_id
ORDER BY tester_id;

-- Expected:
-- T1 300
-- T2 300


-- 5. Check success and failure counts
SELECT
    success_label,
    COUNT(*) AS total_trials
FROM stroke_rehab.fixed_game_trials
GROUP BY success_label
ORDER BY success_label;

-- Expected:
-- Failure 116
-- Success 484


-- 6. Check for duplicate session/trial pairs
SELECT
    session_id,
    trial,
    COUNT(*) AS duplicate_count
FROM stroke_rehab.fixed_game_trials
GROUP BY session_id, trial
HAVING COUNT(*) > 1;

-- Expected: no rows


-- 7. Check data quality issues
SELECT
    COUNT(*) AS rows_with_issues
FROM stroke_rehab.fixed_game_trials
WHERE data_quality_issue_count > 0;

-- Expected: 0


-- 8. Check missing raw accuracy
SELECT
    accuracy_available,
    COUNT(*) AS total_rows
FROM stroke_rehab.fixed_game_trials
GROUP BY accuracy_available
ORDER BY accuracy_available;

-- Expected:
-- no  77
-- yes 523