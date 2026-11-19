-- OPTIONAL migration: review before applying to existing Beverly & Sons Supabase project.
-- Game progress is private to the authenticated account. Server-authoritative validation is needed before competitive rewards.
create table if not exists public.omniverse_player_progress (
 user_id uuid primary key references auth.users(id) on delete cascade,
 display_name text not null default 'Architect',
 mission_001_completed boolean not null default false,
 genesis_jacket_equipped boolean not null default false,
 updated_at timestamptz not null default now()
);
alter table public.omniverse_player_progress enable row level security;
create policy "Players read own progress" on public.omniverse_player_progress for select to authenticated using ((select auth.uid())=user_id);
create policy "Players create own progress" on public.omniverse_player_progress for insert to authenticated with check ((select auth.uid())=user_id);
create policy "Players update own progress" on public.omniverse_player_progress for update to authenticated using ((select auth.uid())=user_id) with check ((select auth.uid())=user_id);
