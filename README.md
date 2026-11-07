# Diwali Together

A mobile-first, browser-based Diwali neighbourhood for friends. **All application HTML, CSS, Firebase integration, multiplayer logic and gameplay are in `index.html`.** Models, sounds and their manifest are separate. No build step is needed for hosting.

## What's included

- Google and anonymous Firebase login; mandatory display name, optional self-described gender and independently chosen avatar.
- Four original festive GLB avatars: saffron/peacock kurtas and rose/indigo lehengas. Named character labels and 13 articulated transform joints: hips, spine, neck, shoulders, elbows, hips/legs, knees and feet. Slow walk/run blend, smooth turn and brief planting pose. These are stylized procedural characters, not motion-captured photorealistic humans.
- Decorated 3D neighbourhood with havelis, balconies, marigolds, string lights, diyas, rangoli, stalls and a gateway.
- Up to eight player records per invite-code room, movement interpolation, disconnect cleanup and reconnection.
- Shared pickup transactions and local inventory; six firework types: rocket, chakri, anar, phuljhadi, ladi and aerial flower burst.
- Seeded shared effect events; visible bottles/rockets, cones, chakri discs, sparkler wires and ladi models. Rockets show a 0.65-second fuse phase, rise visibly and burst at event age 3.0 seconds. Ring, chrysanthemum and willow-like patterns, fading trails, pooled smoke, flash lighting and positional sound. Seven original **synthesized**, layered audio assets, not field recordings.
- Room chat, recipient-protected direct messages, a local mute list, length limits and rule-enforced message cooldowns.
- Touch joystick, Walk/Run toggle, desktop Shift to run, upward/downward free-look, a Sky button and automatic tracking of your own rocket. Two additional areas: Lantern Garden and Festival Square, with collision-aware paths, pool, trees, benches, pavilion and sweet stalls. Graphics/volume settings, fullscreen and solo exploration remain available.

## Phone setup — required before online play

### Upgrading from the first version

**Publish the updated `database.rules.json` again before using the expanded map.** Coordinates now allow x ±18 and z ±40; old rules will reject positions/events outside the original street. Firestore profile rules are unchanged. Refresh/reload all players so models and gameplay use the same version.

### 1. Publish the website

For GitHub Pages: repository **Settings → Pages → Deploy from a branch → main → /(root) → Save**. Wait for GitHub to display the live URL. Alternatively import this repository into Vercel as an **Other/static** project, with no build command and the repository root as output.

Publish `index.html` **and the entire `assets/` folder**. A single pasted HTML file without its assets is not the complete game. Firebase rules and developer test files are not browser scripts.

### 2. Firebase Authentication

Project: `diwali-game-320ec`.

Google and Anonymous must be enabled (your screenshot already shows both enabled). Under **Authentication → Settings → Authorized domains**, add the final hosting hostname. For GitHub Pages on this account, use `bjendermisra-ops.github.io` (hostname only; no `https://` or `/diwali/`). For Vercel, add the actual deployed hostname shown by Vercel.

Google sign-in uses a popup. Open the game in Chrome. Embedded Android WebViews may reject Google OAuth; use an external browser for sign-in or implement native Android Google sign-in before packaging as an APK.

### 3. Realtime Database rules — essential

Open **Realtime Database → Rules**. Replace the rules with the complete contents of [`database.rules.json`](database.rules.json), then **Publish**.

This game uses the configured database URL ending `diwali-game-320ec-default-rtdb.firebaseio.com`. It stores room metadata, eight fixed player slots, pickup claims, the latest event/message per slot, and per-sender direct-message mailboxes.

Do not use `".read": true` / `".write": true`. Do not paste Firestore rules into this editor.

### 4. Cloud Firestore rules — essential

Create the default Firestore database if it is not already created. Open **Firestore Database → Rules**, paste [`firestore.rules`](firestore.rules), and **Publish**.

Profiles are stored at `profiles/{uid}`. Users can only access their own profile document. Their chosen public name, gender choice and avatar are copied into their room player record. No email address is stored in the public room data.

**No manual collections, indexes, Storage buckets or uploads are needed.** The game creates records as players use it. Models and sound files are served from GitHub/Vercel, not Firebase Storage.

### 5. Real-device acceptance test

1. On phone A, open the live HTTPS site, use Guest, save a profile and create a room.
2. Share the invite to phone B. Save a different profile and join the same code.
3. Verify both name labels and both movement directions; test touch camera and joystick.
4. Collect from a stall simultaneously: only one player should receive its pack; it restocks in 12 seconds.
5. Launch all six effects from each phone and compare timing/positional sound.
6. Send a room message, then a direct message. Use a third account to verify it cannot read another recipient's inbox.
7. Disconnect/reconnect phone B, test background/resume, leave and rejoin.
8. Test Google login on the actual authorized hostname and test low graphics on an older phone.

## Controls

- Phone: left joystick moves; drag the scene to look; approach a stall and tap Pick up; tap an inventory item, then the round action button.
- Desktop: WASD/arrows walk; hold Shift to run. Drag upward to look at the sky, V toggles sky view, E picks up, Space uses selected firework, 1–6 selects, wheel adjusts camera distance. On mobile, choose Walk or Run and use joystick distance for speed. Moving/dragging cancels automatic rocket tracking.
- Chat keyboard focus stops keyboard movement. Escape closes panels.

## Asset replacement

Edit [`assets/manifest.json`](assets/manifest.json). Put your licensed GLB files in `assets/models/` and sound files in `assets/audio/`, then update the file paths. Keep the avatar IDs (`amber`, `peacock`, `rose`, `indigo`) unless you also update the profile and database rules.

Included GLBs face +Z in glTF space, measure about 2.1 units tall, and have transform nodes `ArmL/R`, `ElbowL/R`, `LegL/R`, `KneeL/R`, `FootL/R`, `Hips`, `Spine`, `Neck` for the procedural animation. Arbitrary replacement rigs need animation mapping and scale/orientation adjustments; they are not automatically interchangeable. Models have PBR materials. Animation and rendering use Babylon.js.

The original model/audio source generator is [`tools/build_assets.py`](tools/build_assets.py). Run from the repository root with Python 3 and ffmpeg. No paid/licensed third-party character artwork is bundled.

## Architecture and limits

This is a **Firebase-only friends-room implementation**, chosen to keep the game in one HTML file without another server. It does not include the previously discussed Colyseus server. RTDB handles approximately seven movement updates/second while moving, plus a heartbeat every five seconds. Rendering interpolates between these updates; real network latency is still present.

- Rules validate ownership, fields, coordinate bounds, room slots and event/chat cooldowns. Transactions arbitrate pickups.
- Inventory and movement simulation are client-controlled. A modified client can cheat. This is not a competitive authoritative game server; add one before introducing competitive scores, purchases or valuable items.
- Rooms are invite-code access, not account-whitelisted private spaces. Anyone signed in who knows a code can inspect the room's player list and join if a slot is free. Room chat/effects require membership.
- Direct-message mailboxes are recipient-readable only, but are **not end-to-end encrypted**. Firebase administrators can access them. Local mute hides messages on this device, not server-side blocking.
- Each sender/slot retains its latest message only; the browser keeps at most 80 messages for the current session. This is not a permanent chat archive. Rooms/mailboxes have no scheduled expiry yet; delete unused rooms/mailboxes from the console or add an admin cleanup job.
- Eight slot records are enforced; stale slots can be reclaimed after 30 seconds. One person may sign in on more than one device. There is no one-person-one-slot identity guarantee.
- No voice chat, push notifications, report moderation dashboard or user-uploaded media is implemented.
- Firebase usage is not guaranteed free. Monitor RTDB download traffic/connection usage and Firestore reads/writes. Authenticated abuse still needs operational monitoring. App Check is not configured because a site-specific provider registration is required; register and test it before enforcement.
- WebGL is required. Test real Android devices for frame rate and sound; a static code check is not a device-performance guarantee.

## Development and tests

Only the developer tests use npm; the hosted game does not need npm or a build.

```sh
npm ci
npm run check
npm run test:scene
npm run test:rules
npm run dev
```

Rules tests use a **dummy project (`demo-diwali`) and explicit localhost emulator endpoints** and refuse any other test destination. No production database data is needed. Java is required for the emulators. `firebase.local.json` is the local-only test configuration.

To deploy rules yourself with an authenticated Firebase CLI (optional; phone console copy/paste is enough):

```sh
firebase deploy --only database,firestore:rules --project diwali-game-320ec
```

The public Firebase web configuration is intentionally in the client. It is not an Admin SDK credential. Never put a service-account key in this repository.

See [VALIDATION.md](VALIDATION.md) for the checks actually performed on this version and remaining verification.
