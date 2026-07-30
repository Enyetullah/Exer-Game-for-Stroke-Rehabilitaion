-- ============================================================
-- Stroke Rehabilitation Fixed Game SQL Analysis
-- Fixed PostgreSQL Version
-- ============================================================


-- 1. Overall KPI summary
SELECT
    COUNT(*) AS total_trials,
    COUNT(DISTINCT session_id) AS total_sessions,
    COUNT(DISTINCT tester_id) AS total_testers,
    COUNT(DISTINCT mode) AS total_modes,
    SUM(success) AS successful_trials,
    COUNT(*) - SUM(success) AS failed_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND((AVG(caught) * 100)::NUMERIC, 2) AS catch_rate_percent,
    ROUND((AVG(dump_success) * 100)::NUMERIC, 2) AS dump_success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent,
    ROUND(AVG(endpoint_error)::NUMERIC, 2) AS avg_endpoint_error,
    ROUND(AVG(trail_point_count)::NUMERIC, 2) AS avg_trail_point_count
FROM stroke_rehab.fixed_game_trials;


-- 2. Success rate by game mode
SELECT
    mode,
    COUNT(*) AS total_trials,
    SUM(success) AS successful_trials,
    COUNT(*) - SUM(success) AS failed_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent,
    ROUND((AVG(caught) * 100)::NUMERIC, 2) AS catch_rate_percent,
    ROUND((AVG(dump_success) * 100)::NUMERIC, 2) AS dump_success_rate_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY mode
ORDER BY success_rate_percent DESC;


-- 3. Success rate by level
SELECT
    level,
    COUNT(*) AS total_trials,
    SUM(success) AS successful_trials,
    COUNT(*) - SUM(success) AS failed_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY level
ORDER BY level;


-- 4. Success rate by tester
SELECT
    tester_id,
    COUNT(*) AS total_trials,
    SUM(success) AS successful_trials,
    COUNT(*) - SUM(success) AS failed_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent,
    ROUND((AVG(caught) * 100)::NUMERIC, 2) AS catch_rate_percent,
    ROUND((AVG(dump_success) * 100)::NUMERIC, 2) AS dump_success_rate_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY tester_id
ORDER BY success_rate_percent DESC;


-- 5. Success rate by attempt
SELECT
    attempt_number,
    COUNT(*) AS total_trials,
    SUM(success) AS successful_trials,
    COUNT(*) - SUM(success) AS failed_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY attempt_number
ORDER BY attempt_number;


-- 6. Mode and level difficulty analysis
SELECT
    mode,
    level,
    COUNT(*) AS total_trials,
    SUM(success) AS successful_trials,
    COUNT(*) - SUM(success) AS failed_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent,
    ROUND(AVG(endpoint_error)::NUMERIC, 2) AS avg_endpoint_error
FROM stroke_rehab.fixed_game_trials
GROUP BY mode, level
ORDER BY success_rate_percent ASC;


-- 7. Hardest mode-level combination
SELECT
    mode,
    level,
    COUNT(*) AS total_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY mode, level
ORDER BY success_rate_percent ASC
LIMIT 1;


-- 8. Best mode-level combination
SELECT
    mode,
    level,
    COUNT(*) AS total_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY mode, level
ORDER BY success_rate_percent DESC
LIMIT 1;


-- 9. Failure analysis by zone
SELECT
    zone,
    COUNT(*) AS total_trials,
    SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) AS failed_trials,
    ROUND(
        (SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100),
        2
    ) AS failure_rate_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY zone
ORDER BY failure_rate_percent DESC;


-- 10. Catch vs dump-success breakdown
SELECT
    caught_label,
    dump_success_label,
    success_label,
    COUNT(*) AS total_trials
FROM stroke_rehab.fixed_game_trials
GROUP BY caught_label, dump_success_label, success_label
ORDER BY total_trials DESC;


-- 11. Tester performance by mode
SELECT
    tester_id,
    mode,
    COUNT(*) AS total_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY tester_id, mode
ORDER BY tester_id, success_rate_percent DESC;


-- 12. Tester performance by level
SELECT
    tester_id,
    level,
    COUNT(*) AS total_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY tester_id, level
ORDER BY tester_id, level;


-- 13. Attempt improvement by mode
SELECT
    mode,
    attempt_number,
    COUNT(*) AS total_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY mode, attempt_number
ORDER BY mode, attempt_number;


-- 14. Attempt improvement by tester
SELECT
    tester_id,
    attempt_number,
    COUNT(*) AS total_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent
FROM stroke_rehab.fixed_game_trials
GROUP BY tester_id, attempt_number
ORDER BY tester_id, attempt_number;


-- 15. Performance band distribution
SELECT
    performance_band,
    COUNT(*) AS total_trials,
    ROUND(
        (COUNT(*)::NUMERIC / SUM(COUNT(*)) OVER () * 100),
        2
    ) AS percentage_of_trials
FROM stroke_rehab.fixed_game_trials
GROUP BY performance_band
ORDER BY total_trials DESC;


-- 16. Session-level performance summary
SELECT
    session_id,
    tester_id,
    mode,
    level,
    attempt_number,
    COUNT(*) AS total_trials,
    SUM(success) AS successful_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    ROUND(AVG(accuracy_percent_for_analysis)::NUMERIC, 2) AS avg_accuracy_percent,
    ROUND(AVG(endpoint_error)::NUMERIC, 2) AS avg_endpoint_error
FROM stroke_rehab.fixed_game_trials
GROUP BY session_id, tester_id, mode, level, attempt_number
ORDER BY tester_id, mode, level, attempt_number;


-- 17. Rank levels from hardest to easiest
SELECT
    level,
    COUNT(*) AS total_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    RANK() OVER (ORDER BY AVG(success) ASC) AS difficulty_rank
FROM stroke_rehab.fixed_game_trials
GROUP BY level
ORDER BY difficulty_rank;


-- 18. Rank game modes from best to worst
SELECT
    mode,
    COUNT(*) AS total_trials,
    ROUND((AVG(success) * 100)::NUMERIC, 2) AS success_rate_percent,
    RANK() OVER (ORDER BY AVG(success) DESC) AS performance_rank
FROM stroke_rehab.fixed_game_trials
GROUP BY mode
ORDER BY performance_rank;