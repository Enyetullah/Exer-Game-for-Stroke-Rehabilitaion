CREATE SCHEMA IF NOT EXISTS stroke_rehab;

DROP TABLE IF EXISTS stroke_rehab.fixed_game_trials;

CREATE TABLE stroke_rehab.fixed_game_trials (
    session_id TEXT,
    file_name TEXT,
    tester_id TEXT,
    mode TEXT,
    level INTEGER,
    attempt_number INTEGER,
    game_version TEXT,
    "timestamp" DOUBLE PRECISION,
    timestamp_readable TIMESTAMP,
    trial INTEGER,
    ball_x DOUBLE PRECISION,
    cup_x DOUBLE PRECISION,
    endpoint_error DOUBLE PRECISION,
    zone TEXT,
    caught INTEGER,
    dump_success INTEGER,
    success INTEGER,
    difficulty INTEGER,
    game_type TEXT,
    accuracy DOUBLE PRECISION,
    accuracy_percent DOUBLE PRECISION,
    trail_point_count INTEGER,
    trail TEXT,
    mode_label TEXT,
    level_label TEXT,
    attempt_label TEXT,
    success_label TEXT,
    caught_label TEXT,
    dump_success_label TEXT,
    accuracy_available TEXT,
    accuracy_percent_for_analysis DOUBLE PRECISION,
    performance_band TEXT,
    data_quality_issue_count INTEGER,
    data_quality_issues TEXT
);

CREATE INDEX idx_fixed_game_mode
ON stroke_rehab.fixed_game_trials(mode);

CREATE INDEX idx_fixed_game_level
ON stroke_rehab.fixed_game_trials(level);

CREATE INDEX idx_fixed_game_tester
ON stroke_rehab.fixed_game_trials(tester_id);

CREATE INDEX idx_fixed_game_attempt
ON stroke_rehab.fixed_game_trials(attempt_number);

CREATE INDEX idx_fixed_game_session
ON stroke_rehab.fixed_game_trials(session_id);