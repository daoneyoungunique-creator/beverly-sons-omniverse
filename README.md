# BEVERLY & SONS™ OMNIVERSE 518 — Prototype v0.1

Original browser-based 3D game starter. Built with React Three Fiber, Three.js, Vite, Node.js and WebSockets. The optional Supabase email sign-in uses your own project credentials.

## Run locally

1. Install Node.js 20+.
2. From this folder: `npm install`
3. `npm run dev`
4. Open `http://localhost:5173`.
5. For email login, copy `.env.example` values into `client/.env.local` and replace placeholders with your **public** Supabase project URL and publishable key. Configure allowed redirect URLs in Supabase Auth.

## Controls

WASD / arrow keys to move. E near UNITED CONDITIONING™ store at x=-20,z=-4 to equip the Genesis jacket; then E at CAAVE MUSIC™ studio at x=20,z=-4 to complete Mission 001. E near x=0,z=12 to toggle vehicle. Vehicle and avatar are placeholder primitives.

## Multiplayer

Node WebSocket server on port 3001 sends position snapshots. This is a development server only: it currently trusts client movement, uses in-memory state, and does not validate Supabase JWTs. Do **not** treat it as secure public multiplayer hosting or use it for paid economies until server-side authentication, rate limiting, anti-cheat and authoritative state are implemented. For production, host server on a long-running Node provider with HTTPS/WSS reverse proxy; Vercel can host the static frontend, not this persistent socket process.

## Database

`sql/001_game_progress.sql` is a **review-only** schema with row-level security. It has **not** been applied to your existing Supabase project. Current Mission 001 completion uses localStorage only; cloud mission saves and verified ownership remain future work.

## Development limitations

This is a code prototype, not a finished GTA-style game. City is procedural low-poly placeholder geometry; no imported character likenesses, custom 3D clothing meshes, soundtrack, realistic vehicle physics, collision, server-authoritative combat or monetization yet. The named worlds and characters remain design targets. No domain/DNS or live deployment changes have been made.

## Production next steps

1. Add asset pipeline (Blender GLB files), character rigs and animation.
2. Implement Supabase JWT verification on Node server, server-authoritative missions, and persistent cloud saves.
3. Add collision and physics, vehicle controls, touch/mobile controls, accessible settings.
4. Build branded storefront integration and properly licensed CAAVE MUSIC audio.
5. Deploy client to Vercel and Node server to persistent hosting, then configure `game.beverlyandsons.com`.
