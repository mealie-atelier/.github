# Repository map

This document describes the intended public repository boundaries. It is a planning document, not a statement that a package or feature is already implemented.

## Current public repositories

| Repository | Intended responsibility | Current state |
| --- | --- | --- |
| [`mealie-atelier/.github`](https://github.com/mealie-atelier/.github) | Organization profile, shared community guidance, and brand files | Public profile and brand files are published |
| [`mealie-atelier-cards`](https://github.com/mealie-atelier/mealie-atelier-cards) | Home Assistant custom cards and their editor | Starter README only; no application source or release |
| [`mealie-atelier-bridge`](https://github.com/mealie-atelier/mealie-atelier-bridge) | Optional Home Assistant integration and kitchen workflows | Starter README only; no integration source or release |

## Recommended product boundaries

Keep the optional Home Assistant bridge separate from the recipe experience. This lets people use the standalone product without Home Assistant and lets HA users install only the integration or cards they need.

The standalone web app and its PWA should have an independently deployable and versioned web release. The public demo should also deploy independently from the live app and use only fictional, bundled data. That does not require another repository: a single `mealie-atelier-web` repository can contain the standalone app and a separately built demo, with separate deployment jobs and URLs. This keeps source and release workflows together without making the demo depend on production data.

Keep the cards in their existing repository unless implementation work proves that they must share substantial runtime code with the web app. If runtime code is shared, extract a small versioned package or keep it in the web repository as a workspace package; do not copy the same component implementation across repositories.

## Proposed steady state

1. `.github` — organization profile, shared support/security guidance, brand sources and credits.
2. `mealie-atelier-web` — standalone app, PWA, demo fixtures, demo generator and separate web/demo deployment workflows.
3. `mealie-atelier-cards` — Home Assistant cards, visual editor, card-specific documentation and HACS metadata.
4. `mealie-atelier-bridge` — optional Home Assistant integration, integration-specific documentation and HACS metadata.

Do not create `mealie-atelier-web` until its canonical source boundary and initial maintainer workflow are agreed. The existing preview archive is planning material only and is not an approved source to copy into a public repository.

## Release and maintenance rules

- Version and publish Web, Demo, Cards and Bridge independently, with explicit compatibility notes for each package.
- Generate the demo from reviewed, genuinely cookable recipes. Include at least one recipe with step-level photography as well as cover photography, so the cooking flow proves that instructional images and text work together. Do not use household recipe exports, signed image URLs, credentials, browser state, or real shopping data.
- Pin shared design tokens and language resources to a single source. Build reproducible outputs; never edit generated bundles by hand.
- Use separate CI jobs for app tests, demo generation, card builds, integration checks, accessibility checks and release packaging.
- Publish a release only after its own tests and compatibility gates pass. One package's green checks must not imply that another package passed.
- Keep public repositories English for maintainers; translate all end-user screens and guides into German and English.

## Decisions still required before the first release

- Confirm the maintainer identity and add `CODEOWNERS` to repositories that contain source.
- Choose and apply a license separately to every code repository. Brand identity and photography need explicit asset terms; the current attribution file is not a reuse license.
- Set supported Home Assistant and Mealie versions, versioning policy, release channels and support expectations.
- Decide the final public deployment URLs for the web app and demo, then configure repository descriptions, manifests and docs with those exact URLs.
- Publish source only from a canonical checkout and record the source revision used for each release archive.
