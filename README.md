# BEVERLY & SONS™ OMNIVERSE: THE GAME

**Prototype v0.1 — original open-world action RPG concept**

A connected game universe bringing together CAAVE™, UNITED CONDITIONING™, RADICALIZED™, Wisdom Warriors™, H.H.O.S.™, and NI^TOR×IVE RU÷INS™. The experience is envisioned around street-level action, custom vehicles, fashion, music, business ownership, character-driven missions, and supernatural combat.

> **Project status:** This is a visual game concept and browser-based starter prototype—not a finished or production-ready game. The playable milestone is intended to explore one city district, character switching, driving, a clothing store, and an introductory mission.

## The world and campaign

The core campaign, **The 27 Laws**, begins in Albany and Troy. Players build their crew and businesses, unlock CAAVE City, and eventually discover portals to Vesper City and the Ruins.

The connected worlds and characters are design targets. City environments, characters, and gameplay in the current starter are placeholders; the repository does not yet contain the complete campaign or finished assets.

## Playable character storylines

- **Dequan Beverly — The Architect:** a central storyline about building the crew and shaping the connected world.
- **Mara Vale:** leads the RADICALIZED resistance.
- **Geb-Ra’em:** commands mythic powers.
- **DEE-Z:** brings comedy and entertainment missions.

Character switching and these individual storylines remain planned production features unless implemented in the prototype.

## Brands and experiences

- **UNITED CONDITIONING™** is the signature in-game fashion brand. The prototype's introductory mission uses a placeholder store interaction to equip a Genesis jacket.
- **CAAVE MUSIC™** provides the envisioned original soundtrack and interactive recording studio. The prototype's introductory mission uses a placeholder studio interaction.
- Custom vehicles, business ownership, interactive music, and supernatural combat are part of the larger concept; they are not represented as finished systems in this starter.

## Prototype technology

The browser starter is intended to use React Three Fiber, Three.js, Vite, Node.js, and WebSockets. The city is procedural low-poly placeholder geometry, and the avatar and vehicle are placeholder primitives. There are no imported character likenesses, custom clothing meshes, soundtrack, realistic vehicle physics, collision, server-authoritative combat, or monetization in the current concept starter.

## Run locally

1. Install Node.js 20 or newer.
2. From the project folder, run `npm install`.
3. Run `npm run dev`.
4. Open `http://localhost:5173`.
5. For optional email login, copy `.env.example` values into `client/.env.local`, replace the placeholders with your **public** Supabase project URL and publishable key, and configure allowed redirect URLs in Supabase Auth.

The original starter description refers to a React entry point at `/src/main.jsx`. Verify that the application source, package scripts, and dependencies are present in the repository before expecting these commands to run; this README does not claim that a complete playable application is already implemented.

## Controls described for the starter

- **WASD / arrow keys:** move.
- **E near UNITED CONDITIONING™** at `x=-20,z=-4`: equip the Genesis jacket.
- **E near CAAVE MUSIC™** at `x=20,z=-4`: complete Mission 001.
- **E near `x=0,z=12`:** toggle the placeholder vehicle.

These are the prototype's intended starter interactions, not a claim that the full game systems are production-ready.

## Multiplayer and security

The described development WebSocket server runs on port `3001` and sends position snapshots. It trusts client movement, uses in-memory state, and does not validate Supabase JWTs. **Do not treat it as secure public multiplayer hosting or use it for paid economies.** Production multiplayer requires server-side authentication, rate limiting, anti-cheat protections, authoritative state, and persistent storage. For production, host the server on a long-running Node provider behind an HTTPS/WSS reverse proxy; Vercel can host a static frontend but not this persistent socket process.

## Database and account status

`sql/001_game_progress.sql` is described as a review-only schema with row-level security; it has not been applied to an existing Supabase project. Mission 001 completion is described as localStorage-only. Cloud mission saves and verified ownership remain future work. Supabase credentials must be configured by the project owner and public client keys should never be confused with service-role secrets.

## Suggested production milestones

1. Confirm the application source and build scripts, then deliver a playable slice of one city district and an introductory mission.
2. Add Blender GLB asset pipelines, character rigs, animations, and character switching.
3. Implement collision and physics, driving, and touch/mobile controls with accessible settings.
4. Implement Supabase JWT verification on the Node server, server-authoritative missions, and persistent cloud saves.
5. Build the UNITED CONDITIONING™ storefront integration and add properly licensed CAAVE MUSIC audio.
6. Deploy the client to Vercel and the Node server to persistent hosting; configure `game.beverlyandsons.com` only when deployment and DNS are ready.

No domain/DNS or live deployment changes are implied by this concept or README.
