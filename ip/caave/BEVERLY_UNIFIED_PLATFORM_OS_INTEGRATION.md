# Beverly & Sons Unified Platform OS — integration register
Status: USER-SUPPLIED PROTOTYPE; integration specification only
Source: uploaded 703-line React + Three.js app, 2026-11-20
Owner: Beverly & Sons Marketing and Consulting LLC
Scope: Extend existing CAAVE Daily Media Engine and Beverly & Sons IP architecture.

## Five interface areas
1. HUB: dashboard navigation for the four application systems, Three.js shader background with instanced GPU cards and stars.
2. WISDOM WARRIOR: six modules: KNOW THE SELF (M.I.N.D., marked complete), AFFIRMING THE NEXT (L.E.G.A.C.Y., marked active), POWER MAP (P.O.W.E.R.), VOICE ACTIVATED (V.O.I.C.E.S.), THE WEALTH WHEEL (W.E.A.L.T.H.), BIAS DECODED (B.I.A.S.). Last four marked locked in supplied prototype. L.E.G.A.C.Y. = Leave a blueprint; Example over words; Grow under pressure; Affirm the next generation; Cultivate wisdom; Yield transformation. Teaching contract: core truth, letter-by-letter real application, 3 actions, spoken affirmation.
3. CALMING OS: five loops SCAN (Self/State/Capacity), FAP-R (Fear/Action/Pattern/Repair), INFLUENCE (Home/Allies/Routines/Messages), SOCIAL NAV (Belonging/Power/Conflict/Culture), REPAIR (Pattern/Response/Restore). SCAN states LOW/MED/HIGH. Preserve source philosophy of recognizing states, regulating responses, adapting and repairing, rather than promising constant calm. Educational coaching only, not clinical care.
4. IP POST ENGINE: five *actual configured* source records (not seven): OPPRESS: The American Cage (06:00), Legacy Code: T.E.A.C.H.I.N.G. (08:00), God in the Mirror (10:00), Family Wealth Structure (12:00), H.H.O.S. (15:00). Output JSON fields hook, lesson, affirmation, poem, hashtags, instagram, tiktok, twitter. Views: Instagram, TikTok, Twitter/X, WhatsApp. Source hours are proposed schedule slots, not actual posts.
5. RECLAMATION: static five-stanza poem player (M.I.N.D., I.M.P.A.C.T., P.O.W.E.R., V.O.I.C.E.S., B.I.A.S.), line-by-line visual recitation, GPU backdrop; no audio playback in supplied implementation.

## Integration relationships
Daily Media Engine 12-stage drafts -> IP source library -> educational module -> platform-specific post drafts -> review queue -> owner-approved publishing -> verified digital storefront.
CAAVE Academy: lessons and framework-specific modules.
CAAVE MUSIC: original poem and spoken-word adaptation, separate rights review.
H.H.O.S.: CALMING learning system.
W.E.A.L.T.H.: financial literacy only, no promises of financial returns.
Beverly Method: consistent editorial tone and character rights.
147 Codex: separate node indexing (Heart + Justice + Middle = Node 77), unaffected.

## Technical issues to resolve
- Source invokes Anthropic directly from the browser with no authentication headers; replace with authenticated server-side AI proxy and server-stored credentials. Do not expose API keys.
- UI labels such as ALL LIVE, LIVE, NFT LOCKED, and IP LOCKED are unverified; do not imply real publishing, blockchain access controls, or legal registration.
- MODULES objects contain status but no access property; active.access renders undefined. Define access explicitly or remove that label.
- Source displays '7 books' but IP_LIBRARY contains five records; align copy to actual inventory.
- The generator sets status done even if JSON parsing fails; validate required schema before marking draft ready.
- Generation is not publishing. Rename LIVE post status to DRAFT READY.
- No persistence, login, consent, checkout, fulfillment, publishing APIs, or NFT access verification is implemented in the supplied component.
- CALMING chat stores a history array but does not pass history to the AI call; implement history server-side with privacy/consent controls.
- Make grid responsive for mobile; the CALMING panel uses fixed '1fr 360px' without a responsive override.
- Add semantic keyboard controls, reduced-motion mode, and WebGL fallback.
- Do not post, mint, sell, charge, or message customers without explicit approval.

## Next build acceptance
Render all five areas in the existing web app, connect only secure server AI routes, preserve original framework names, persist draft outputs, expose review/approval status, and ensure no externally visible change without authorization.
