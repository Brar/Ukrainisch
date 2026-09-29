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
- `tmp/` is a local, gitignored folder where the user drops material for Claude
  to look at (documents, screenshots, word lists, exports). Treat what's there
  as input, not as repository content. Its files may be under incompatible
  licenses, so the sourcing rules above apply before any text from them goes
  into a note or a committed file.

## Anki access

- Anki is reached through the AnkiMCP add-on (AnkiWeb code `124672614`,
  <https://github.com/ankimcp/anki-mcp-server-addon>), which runs an MCP server
  inside Anki desktop at `http://127.0.0.1:3141/` (HTTP transport).
- It is registered in Claude Code as the server `anki` at **user scope**
  (`~/.claude.json`), so there is no `.mcp.json` in this directory.
- Anki must be open for the tools to work. If the `anki` tools are missing,
  start Anki and run `/mcp` to reconnect.
- The add-on's `create_deck` tool refuses names with more than two levels
  (`A::B`). This is an arbitrary check in that tool only. `add_note` and
  `add_notes` work with deeper decks, but the deck must already exist. Create
  three-level decks by hand in Anki ("Stapel erstellen" in the German UI).

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

## Ukrainian spelling

- Main form: the standard spelling under the 2019 orthography (*Український
  правопис*). Drug names use the Ukrainian INN (МНН) spelling in the
  *Державний реєстр лікарських засобів України*.
- Synonyms that are in real clinical use also go on the card (e.g.
  `мокротиння` / `харкотиння`, `випорожнення` / `кал`).
- Common non-standard *spellings* (e.g. from lab exports, such as
  `Цефтазідім`) may be noted on the card as non-standard, but are never the
  answer.
- Discard everything else: keyboard or encoding damage (`мякі`, `м"які`),
  capitalisation variants, inflected forms (cards use the dictionary form) and
  word-order variants.
- Apostrophe: ASCII `'` (U+0027), as in the existing course deck. Don't use
  `’` (U+2019) or `ʼ` (U+02BC); mixing them breaks searches in Anki.
- Check borrowed words against the *правило дев'ятки*: after д, т, з, с, ц,
  ж, ч, ш, р, write и (not і) before a consonant (`цефтазидим`, `рифампіцин`,
  `триметоприм`). Drug names should still be confirmed in the State Register.

## Decisions

- Medical cards live under the deck `Ukrainisch::Medizin`, a sibling of
  `Ukrainisch::Anfänger`. `Ukrainisch::Anfänger` is an imported beginner course
  (740 notes, note type `Basic-a9aca`, German → Ukrainian only, tags `урок-N`)
  and must not be changed.
- Below `Ukrainisch::Medizin` there is exactly one level of topic subdecks,
  one per topic that is studied on its own:
  - `Ukrainisch::Medizin::Mikrobiologie`: specimens, organisms, lab results
  - `Ukrainisch::Medizin::Hygiene`: infection prevention and control
  - `Ukrainisch::Medizin::Antiinfektiva`: drug names, antimicrobial stewardship
  - `Ukrainisch::Medizin::Klinik`: departments, general clinical terms, forms

  Finer or overlapping topics are handled with hierarchical tags (e.g.
  `thema::probenmaterial`), and a note can carry several of them. Each note
  goes in exactly one deck, the topic it belongs to most.

## Open decisions

When a decision is made, move it to "Decisions" above.

- Note type and fields: built-in "Basic (and reversed card)", or a custom type
  with extra fields (German article/plural, Ukrainian gender, verb aspect pair,
  abbreviation, example sentence, source)?
- Stress marks on Ukrainian words (combining acute, U+0301)?
- Tag vocabulary: which `thema::` tags, and whether to add source or status
  tags?
- Audio / TTS?
- Source of truth: Anki only, or also version-controlled word lists (e.g. TSV)
  in this directory?
