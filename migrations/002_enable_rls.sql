-- Enable Row Level Security (RLS) and create policies
-- This migration enables RLS on the core game tables

-- Enable RLS on game tables
ALTER TABLE rooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE battles ENABLE ROW LEVEL SECURITY;
ALTER TABLE movements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_items ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see/modify their own rooms
-- NOTE: auth.uid() returns UUID but user_id is INTEGER (custom auth)
-- Using service role bypass or app-level auth for now
-- CREATE POLICY "users_own_rooms" ON rooms FOR ALL
--     USING (user_id = auth.uid())
--     WITH CHECK (user_id = auth.uid());

-- Policy: Users can only see/modify their own teams
-- NOTE: Using custom auth, auth.uid() not applicable
-- CREATE POLICY "users_own_teams" ON teams FOR ALL
--     USING (user_id = auth.uid())
--     WITH CHECK (user_id = auth.uid());

-- Policy: Users can only see/modify battles they participated in
-- NOTE: Using custom auth, auth.uid() not applicable
-- CREATE POLICY "users_own_battles" ON battles FOR ALL
--     USING (winner_id = auth.uid() OR loser_id = auth.uid())
--     WITH CHECK (winner_id = auth.uid() OR loser_id = auth.uid());

-- Policy: Users can only see/modify movements in their battles
-- NOTE: Using custom auth, auth.uid() not applicable
-- CREATE POLICY "users_own_movements" ON movements FOR ALL
--     USING ( EXISTS (
--         SELECT 1 FROM rooms
--         WHERE rooms.id = movements.room_id
--         AND (rooms.user_id = auth.uid() OR rooms.enemigo_id = auth.uid())
--     ))
--     WITH CHECK ( EXISTS (
--         SELECT 1 FROM rooms
--         WHERE rooms.id = movements.room_id
--         AND (rooms.user_id = auth.uid() OR rooms.enemigo_id = auth.uid())
--     ));

-- Policy: Users can only see/modify their own user_items
-- NOTE: Using custom auth, auth.uid() not applicable
-- CREATE POLICY "users_own_user_items" ON user_items FOR ALL
--     USING (user_id = auth.uid())
--     WITH CHECK (user_id = auth.uid());
