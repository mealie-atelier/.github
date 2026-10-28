# Website documentation plan

## Current site context

[Alles Automatisch](https://alles-automatisch.de/) already has a German-first Home Assistant learning area at [`/lernen`](https://alles-automatisch.de/lernen). Its existing navigation groups guides under “Geräte verbinden”, “Dashboards & Energie”, “Smartphone & App”, and other practical topics. The site also has a support page at [`/unterstuetzen`](https://alles-automatisch.de/unterstuetzen).

The current site is centered on Home Assistant guides. Mealie Atelier also includes a planned standalone recipe experience, so the documentation should have its own product overview and then link into the existing learning categories. The site currently exposes no visible language switch or English documentation route; verify the CMS language setup before promising English pages.

## Recommended information architecture

1. `/mealie-atelier/` — product overview, current release status, deployment choices, privacy summary, live demo and support.
2. `/mealie-atelier/standalone/` — web app/PWA setup, reverse proxy, accounts, read-only mode, data storage, backup and restore.
3. `/mealie-atelier/home-assistant/` — beginner setup path, HACS or manual installation, API credentials, permissions, dashboard resources, update and removal.
4. `/mealie-atelier/karten/` — card catalog, editors, responsive behavior, data source, recipe photos, planning and shopping behavior.
5. `/mealie-atelier/bridge/` — optional integration setup, exposed entities/actions, shopping-list services, duplicate handling and failure recovery.
6. `/mealie-atelier/troubleshooting/` — connection, permissions, blank cards, stale resources, pagination, media, HTTPS and safe log sharing.
7. `/mealie-atelier/releases/` — version history, compatibility, migration notes and known limits.
8. `/mealie-atelier/demo/` — separately deployed bilingual showcase with clearly fictional recipes and browser-only changes.
9. English equivalents — publish only after a verified language routing and translation workflow exists in the CMS.

Add an entry to **Lernen → Geräte verbinden** for the Bridge and to **Lernen → Dashboards & Energie** for the cards. Link the standalone path from the Atelier overview so visitors do not need Home Assistant. Avoid duplicating generic Mealie setup; link to the primary Mealie API and installation documentation.

## Beginner-to-expert reading path

- **New to Mealie:** explain what the user needs before starting, how to find their Mealie address, and what an API token is in plain language.
- **New to Home Assistant:** offer a no-terminal path where supported, show each screen and expected result, and put the manual path in a clearly separated advanced section.
- **Experienced users:** provide exact URLs, version constraints, YAML/resource snippets, permission scopes, backup/rollback steps and troubleshooting signals.
- **Security-minded users:** state exactly what data leaves the browser/HA instance, where tokens are stored, what optional third-party services do, and which features fail closed.

Every installation guide should distinguish required from optional steps, show a successful result, include update and removal instructions, and link to known limitations. Do not use preview screenshots as proof of live compatibility.

## Demo, SEO and visual quality

- Deploy the demo independently from the standalone production app. Use ten reviewed, genuinely cookable bilingual recipes written for the showcase and locally bundled food photography with documented licenses/credits.
- Keep changes in the demo session only; do not call Mealie or Home Assistant and do not claim changes were saved to a server.
- Provide semantic page content outside the interactive shell so search engines and assistive technology can understand the product and recipe examples.
- Use a distinct title and meta description for the product overview, setup guides, troubleshooting and demo. Add `HowTo` structured data only to a genuinely step-by-step installation page.
- Ensure the demo is keyboard-operable, responsive, safe under reduced motion, and still understandable if JavaScript or a remote image fails.
- Show credits near the demo and keep the support link optional and low pressure. Never gate functionality behind a donation prompt.

## Publish gate

Do not publish installation instructions until canonical repositories, code, releases, supported versions, privacy behavior and support destinations are confirmed. Before publishing, verify every link, screenshot alt text, mobile layout, keyboard path, reduced-motion behavior, contrast/focus states, canonical URL and structured data on the live site.

## Current blocker

The WordPress.com connector surfaced in plugin discovery but is not installed, and its scope does not confirm that it can edit `alles-automatisch.de`. No site page was changed from this workspace. The web app and demo source/release URLs are also not established. Prepare the final page copy and screenshots only against a canonical source checkout and a confirmed CMS publishing path.
