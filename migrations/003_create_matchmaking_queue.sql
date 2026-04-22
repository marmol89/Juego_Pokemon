-- Migration: 003_create_matchmaking_queue.sql
-- Creates the matchmaking queue table with RLS policies

-- ============================================================================
-- TABLE: matchmaking_queue
-- ============================================================================
CREATE TABLE IF NOT EXISTS matchmaking_queue (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL,
    rating_diff_max INTEGER DEFAULT 50,
    status VARCHAR(20) NOT NULL DEFAULT 'waiting',
    room_id UUID REFERENCES rooms(id) ON DELETE SET NULL,
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
-- FUNCTION: find_match_candidates(p_rating, p_rating_diff_max)
-- Returns the best matching candidate for a given rating
-- Ordered by smallest rating difference, then earliest entry time
-- ============================================================================
CREATE OR REPLACE FUNCTION find_match_candidates(p_rating INTEGER, p_rating_diff_max INTEGER)
RETURNS TABLE(user_id UUID, rating INTEGER, entered_at TIMESTAMPTZ, id BIGINT) AS $$
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
-- TRIGGER FUNCTION: trigger_find_match()
-- After INSERT on matchmaking_queue, invokes the find-match Edge Function
-- via net.http_request to process the new entry
-- ============================================================================
CREATE OR REPLACE FUNCTION trigger_find_match()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM net.http_request(
        url := current_setting('app.settings.supabase_url', true) || '/functions/v1/find-match',
        method := 'POST',
        headers := '{"Content-Type": "application/json"}'::jsonb,
        body := jsonb_build_object('new_entry_id', NEW.id, 'user_id', NEW.user_id)::jsonb
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGER: on_queue_insert
-- Fires trigger_find_match() after each INSERT on matchmaking_queue
-- ============================================================================
DROP TRIGGER IF EXISTS on_queue_insert ON matchmaking_queue;
CREATE TRIGGER on_queue_insert
    AFTER INSERT ON matchmaking_queue
    FOR EACH ROW EXECUTE FUNCTION trigger_find_match();

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================
ALTER TABLE matchmaking_queue ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only read their own queue entries
DROP POLICY IF EXISTS matchmaking_queue_select_own ON matchmaking_queue;
CREATE POLICY matchmaking_queue_select_own
    ON matchmaking_queue
    FOR SELECT
    USING (auth.uid() = user_id);

-- Policy: Users can only insert if not already in 'waiting' status
-- This prevents duplicate queue entries
DROP POLICY IF EXISTS matchmaking_queue_insert_no_duplicates ON matchmaking_queue;
CREATE POLICY matchmaking_queue_insert_no_duplicates
    ON matchmaking_queue
    FOR INSERT
    WITH CHECK (
        auth.uid() = user_id
        AND NOT EXISTS (
            SELECT 1 FROM matchmaking_queue
            WHERE user_id = auth.uid() AND status = 'waiting'
        )
    );

-- Policy: Users can only update their own entries (for status changes)
DROP POLICY IF EXISTS matchmaking_queue_update_own ON matchmaking_queue;
CREATE POLICY matchmaking_queue_update_own
    ON matchmaking_queue
    FOR UPDATE
    USING (auth.uid() = user_id);

-- Policy: Users can only delete their own entries (to leave queue)
DROP POLICY IF EXISTS matchmaking_queue_delete_own ON matchmaking_queue;
CREATE POLICY matchmaking_queue_delete_own
    ON matchmaking_queue
    FOR DELETE
    USING (auth.uid() = user_id);

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
