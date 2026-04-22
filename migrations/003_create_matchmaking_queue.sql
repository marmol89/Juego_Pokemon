-- Migration: 003_create_matchmaking_queue.sql
-- Creates the matchmaking queue table for rapid matchmaking
-- NOTE: Uses INTEGER for user_id/room_id to match custom auth schema (not Supabase Auth UUID)

-- ============================================================================
-- TABLE: matchmaking_queue
-- ============================================================================
CREATE TABLE IF NOT EXISTS matchmaking_queue (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL,
    rating_diff_max INTEGER DEFAULT 50,
    status VARCHAR(20) NOT NULL DEFAULT 'waiting',
    room_id INTEGER REFERENCES rooms(id) ON DELETE SET NULL,
    entered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT valid_status CHECK (status IN ('waiting', 'matched', 'timeout', 'abandoned'))
);

-- ============================================================================
-- INDEX: idx_matchmaking_status_entered
-- Fast lookup for finding candidates in the queue
-- Partial index only includes 'waiting' entries
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_matchmaking_status_entered
    ON matchmaking_queue(status, entered_at ASC)
    WHERE status = 'waiting';

-- ============================================================================
-- NOTE: Matchmaking logic is handled in Python (MatchmakingDAO.find_match)
-- instead of Edge Functions or DB triggers, for better local development support
-- ============================================================================

-- ============================================================================
-- FUNCTION: find_match_candidates(p_rating, p_rating_diff_max)
-- Returns the best matching candidate for a given rating
-- Ordered by smallest rating difference, then earliest entry time
-- ============================================================================
CREATE OR REPLACE FUNCTION find_match_candidates(p_rating INTEGER, p_rating_diff_max INTEGER)
RETURNS TABLE(user_id INTEGER, rating INTEGER, entered_at TIMESTAMPTZ, id BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT mq.user_id, mq.rating, mq.entered_at, mq.id
    FROM matchmaking_queue mq
    WHERE mq.status = 'waiting'
      AND ABS(mq.rating - p_rating) <= p_rating_diff_max
    ORDER BY ABS(mq.rating - p_rating) ASC, mq.entered_at ASC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- FUNCTION: updated_at_trigger()
-- Auto-updates the updated_at column on row changes
-- ============================================================================
CREATE OR REPLACE FUNCTION updated_at_trigger()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update updated_at on any change
DROP TRIGGER IF EXISTS matchmaking_queue_updated_at ON matchmaking_queue;
CREATE TRIGGER matchmaking_queue_updated_at
    BEFORE UPDATE ON matchmaking_queue
    FOR EACH ROW
    EXECUTE FUNCTION updated_at_trigger();
