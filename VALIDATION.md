# Validation — 7 November 2026

## Completed

- `npm run check`: inline JavaScript syntax, all referenced DOM IDs, rules JSON, four GLB files and seven Ogg sound assets passed.
- `npm run test:scene`: Babylon.js NullEngine constructed the complete world and ran frame/effect logic. All six firework paths exercised. Invalid effect coordinates rejected. Particle count stayed within its configured budget.
- All four GLB assets loaded through the actual Babylon glTF loader; each instantiated with its four animated limb joints and expected bounding height.
- Static world geometry batching reduced the environment from 660 to 47 meshes before characters/effects. This is a draw-structure improvement, not a measured phone frame-rate claim.
- Browser preview opened and caught an insecure-local-origin `crypto.randomUUID` incompatibility. Replaced it with cryptographic random bytes, also usable on the local preview origin.

## Not verified / blockers

- Cloud browser reported **WebGL not supported**. Actual GPU visuals, responsive gameplay interaction, sound perception and Android performance could not be visually tested there. The game now gives a clear graphics support error instead of a silent blank screen. Headless tests are not equivalent to rendering tests.
- Firebase emulator integration tests were written for nine access/concurrency cases, but execution was interrupted by automatic approval review, which classified a connection as possible live Firebase access. The test harness now explicitly pins `127.0.0.1:9000` / `127.0.0.1:8080`, refuses other endpoint variables, and uses dummy project `demo-diwali`. These tests are included but **are not recorded as passed**.
- No Firebase production rules, authorized-domain configuration or hosting settings were changed. The supplied public web configuration does not grant administrative access to those settings.
- Live Google login, guest profile creation, two-device room sync, reconnect, pickup races and private chat must be acceptance-tested after the Firebase rules and hosting domain are configured, following README.md.

Do not describe this version as production-certified, cheat-proof, perfectly synchronized or tested on all Android phones.

## Movement and fireworks update — 7 November 2026

Passed `npm run check` and expanded `npm run test:scene`:

- All four regenerated GLBs load with 13 animated transform joints. Tests check actual foot displacement in world space, bent knees and elbows, avoiding the prior quaternion/Euler conflict.
- The real frame loop runs in solo mode: run displacement exceeds slow-walk displacement by more than 2.5×.
- Camera math looks nearly straight up and also down.
- Running is blocked by the street buildings; the expanded plaza is reachable.
- A visible rocket shell rises before the burst, has not exploded at 2.9 seconds, and switches to burst at 3.01 seconds. Its prop cleans up after its lifetime.
- Static scenery batches to 57 meshes before dynamic characters, props and particles.

Browser rendering was attempted again; the cloud Chrome instance still reports WebGL unavailable. No claim is made that actual GPU visuals, Android FPS, perceived audio realism or two-device production Firebase sync were verified. Firebase emulator tests were not retried after the earlier automatic approval rejection.

Expanded-world RTDB rules must be published by the Firebase project administrator. No live Firebase settings were changed.
