-- Enable Row Level Security (RLS) and create policies
-- This migration enables RLS on the core game tables

-- Enable RLS on game tables
-- NOTE: All RLS disabled - project uses custom auth (bcrypt), not Supabase Auth
-- auth.uid() returns UUID which is incompatible with INTEGER user_id in this project
-- Using application-level authorization instead
-- ALTER TABLE rooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE rooms DISABLE ROW LEVEL SECURITY;

-- Policy: Users can only see/modify their own rooms
-- NOTE: auth.uid() returns UUID but user_id is INTEGER (custom auth)
-- Using service role bypass or app-level auth for now
-- CREATE POLICY "users_own_rooms" ON rooms FOR ALL
--     USING (user_id = auth.uid())
--     WITH CHECK (user_id = auth.uid());

-- Disable RLS on remaining tables
ALTER TABLE teams DISABLE ROW LEVEL SECURITY;
ALTER TABLE battles DISABLE ROW LEVEL SECURITY;
ALTER TABLE movements DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_items DISABLE ROW LEVEL SECURITY;
