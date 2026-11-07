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
