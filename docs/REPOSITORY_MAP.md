# Repository map

This documents the current public repository boundaries and release responsibilities.

## Current repositories

| Repository | Responsibility | Release boundary |
| --- | --- | --- |
| [`mealie-atelier/.github`](https://github.com/mealie-atelier/.github) | Organization profile, shared community files, and brand source assets | No product runtime or release artifact |
| [`mealie-atelier-cards`](https://github.com/mealie-atelier/mealie-atelier-cards) | Home Assistant cards, optional standalone Web app/PWA, and fictional-data demo | Cards, Web app, and demo have independent manual release boundaries |
| [`mealie-atelier-bridge`](https://github.com/mealie-atelier/mealie-atelier-bridge) | Optional Home Assistant integration and server-side kitchen capabilities | Independent HACS integration release |

The standalone app and public demo intentionally live in the Cards repository for now. This keeps the current design system and app source together without creating a third product repository. They remain independently deployable and usable without Home Assistant. Revisit the repository split only if ownership, deployment, or release cadence creates real maintenance friction.

## Release and maintenance rules

- Keep the standalone Web app useful without Home Assistant. HA cards and the Bridge are optional capabilities.
- Release Cards, Web app, demo, and Bridge independently; passing one package check does not imply another artifact is ready.
- Keep demo data fictional, reviewed, bilingual, and independent of household exports, API tokens, or live services.
- Generate bundles, demo pages, and icons from their source; never hand-edit generated build output. Brand SVGs are self-contained and use square-edged artwork; see `brand/README.md` for the manual macOS export steps.
- Keep maintainer-facing source, comments, and repository documentation in English. Translate end-user UI and setup guidance into German and English.
- Record the source revision used for each public package. Do not force-push or rewrite existing repository history.

## Current implementation boundary

- `mealie-atelier-cards`: root contains the HACS card package, `web/` contains the standalone app, and `demo/` contains reviewed fixtures and the public showcase generator/output.
- `mealie-atelier-bridge`: root contains `custom_components/mealie_atelier`, its translations, tests, and HACS metadata.
- `.github`: organization-level community profile and brand files only.

See each product repository's README and release checklist for actual implementation and verification status. Live-service and physical-device acceptance are separate release gates.

## Corrections log

- 2026-10-28 — Recorded the owner’s policy for manual maintenance and disabled GitHub Actions organization-wide along with automatic Dependabot update PRs in current product repositories.
- 2026-10-28 — Replaced rounded icon and preview treatments with square-edged, self-contained pasta artwork; kept the source and every product export in sync.
