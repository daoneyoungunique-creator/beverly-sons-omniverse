# Next steps — simple owner checklist

## 1. Upload game source to GitHub
Open https://github.com/daoneyoungunique-creator/beverly-sons-omniverse and choose Add file > Upload files. Unzip the game package first, then upload the contents of the beverly-omniverse folder, including the client and server folders. Do not upload .env files or credentials.

## 2. Verify code builds
Run npm install and npm run dev on a computer with Node.js 20+. Open localhost:5173. The game is a development prototype, not a public multiplayer production server.

## 3. Deploy in two pieces
Deploy the client on Vercel and the persistent Node WebSocket server on a service supporting long-running Node processes. Configure the client's websocket URL to the server's secure wss:// address. Do not deploy the WebSocket process as a Vercel serverless function.

## 4. Secure player accounts
Before public multiplayer or purchases, implement Supabase JWT verification on the WebSocket server, server-authoritative movement/mission validation, rate limiting, and RLS policies for saved progress. Do not apply the review-only SQL until the security model is reviewed.

## 5. Domain
Only after the game is deployed and tested, configure game.beverlyandsons.com in Vercel and DNS. Do not replace the existing storefront.
