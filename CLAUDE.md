# Ukrainisch — German ⇄ Ukrainian medical Anki cards

## Purpose

Bidirectional Anki cards (German → Ukrainian and Ukrainian → German) for medical
vocabulary, with a focus on:

- Infection prevention and control (IPC; Infektionsprävention / Krankenhaushygiene)
- Microbiology
- Antimicrobial stewardship (Antibiotic Stewardship, ABS)

Every note must produce a card in each direction.

## Repository and licensing

- Public repository: <https://github.com/Brar/Ukrainisch> (default branch `main`).
- `LICENSE` is the official CC BY-SA 4.0 legal code in plain text, copied
  unchanged from creativecommons.org. Keep it that way. GitHub's license
  detection (licensee) needs at least 98% similarity, and a Markdown
  reformatting of the same text scored only 95%.
- Content is licensed under CC BY-SA 4.0. Everything committed here must be
  releasable under CC BY-SA 4.0:
  - Terms and their equivalents are fine to take from any source.
  - Text from Wiktionary (CC BY-SA 4.0) may be adapted. Any note that uses it
    must record the URL of the Wiktionary entry, and must say so if the text
    was changed.
  - Text from NonCommercial sources can't be used, because NC is incompatible
    with ShareAlike. This includes WHO publications (usually CC BY-NC-SA 3.0
    IGO). They can still be used to check which term is correct, but example
    sentences, definitions and explanations must then be our own wording.
  - If code (scripts, tooling) is ever added, license it separately under a
    software license (e.g. MIT). CC licenses are not meant for software.
- Any published deck (AnkiWeb, `.apkg`) must carry the CC BY-SA 4.0 notice and
  attribution in its description.
- Never commit `*.colpkg` (full collection exports that include personal review
  history). It is already in `.gitignore`.

## Anki access

- Anki is reached through the AnkiMCP add-on (AnkiWeb code `124672614`,
  <https://github.com/ankimcp/anki-mcp-server-addon>), which runs an MCP server
  inside Anki desktop at `http://127.0.0.1:3141/` (HTTP transport).
- It is registered in Claude Code as the server `anki` at **user scope**
  (`~/.claude.json`), so there is no `.mcp.json` in this directory.
- Anki must be open for the tools to work. If the `anki` tools are missing,
  start Anki and run `/mcp` to reconnect.

## Terminology

- Accuracy matters more than coverage. Use the terms that clinical and
  public-health practice actually uses, not literal translations. If a term
  can't be verified, flag it instead of guessing.
- German references: RKI, KRINKO recommendations, ART (Kommission Antiinfektiva,
  Resistenz und Therapie).
- Ukrainian references: orders and protocols of the МОЗ України, Центр
  громадського здоров'я України, and WHO materials in Ukrainian.
- Use standard modern Ukrainian (2019 orthography). Avoid Russisms and calques
  from Russian.

## Open decisions

Record each decision here once it's made, and remove it from this list.

- Deck structure: one deck, or subdecks per topic?
- Note type and fields: built-in "Basic (and reversed card)", or a custom type
  with extra fields (German article/plural, Ukrainian gender, verb aspect pair,
  abbreviation, example sentence, source)?
- Stress marks on Ukrainian words (combining acute, U+0301)?
- Tagging scheme (by topic, by source, by status)?
- Audio / TTS?
- Source of truth: Anki only, or also version-controlled word lists (e.g. TSV)
  in this directory?
