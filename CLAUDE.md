# Ukrainisch — German ⇄ Ukrainian medical Anki cards

## Purpose

Bidirectional Anki cards (German → Ukrainian and Ukrainian → German) for medical
vocabulary, with a focus on:

- Infection prevention and control (IPC; Infektionsprävention / Krankenhaushygiene)
- Microbiology
- Antimicrobial stewardship (Antibiotic Stewardship, ABS)

A second part covers everyday communication from CEFR level A1 to B2, built
up level by level, with a focus on talking with patients, relatives and
colleagues in hospital, epidemiology, IPC and AMR settings (see
`docs/alltag-szenarien.md`).

Every note must produce a card in each direction.

There are two audiences: German speakers learning Ukrainian, and Ukrainian
speakers learning German. Each gets its own edition, generated from the same
word list. Information *about* a language is for learners *of* that language,
so it's written in their language. Notes on Ukrainian (gender, usage) are in
German. Notes on German (usage) are in Ukrainian.

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
  - Code (scripts, tooling) lives in `tools/` and is licensed under MIT
    (`tools/LICENSE`, plus an SPDX header in each file). CC licenses are not
    meant for software.
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
  `add_notes` work with deeper decks, but the deck must already exist. To
  create a deeper deck:
  1. Add a temporary placeholder note to an existing deck.
  2. Move its card with `card_management` → `change_deck`, which creates the
     target deck at any depth.
  3. Delete the placeholder and run `clear_unused_tags` (after checking that
     no other unused tags would be lost).
  Alternatively, create the deck by hand in Anki ("Stapel erstellen").

## Tools

- Python scripts in `tools/` run in the virtual environment `.venv`
  (gitignored). Set it up with `py -m venv .venv`, then
  `.venv\Scripts\python -m pip install -r tools\requirements.txt`.
- `tools/record_audio.py <word list>` records one entry at a time from a TSV
  with an `id` column and a text column (default `de`).
  - It trims silence, normalises loudness and saves `audio/de/<id>.mp3`.
  - Entries that already have a file are skipped. `--redo ID…` re-records.
  - `--list-devices`, `--device` and `--channel` select the input. The user's
    interface is a Steinberg UR22mkII with two inputs.
  - It is interactive, so the user runs it in their own terminal, not Claude.

## Word list format

- One file per deck: `vocab/mikrobiologie.tsv`, `vocab/hygiene.tsv`,
  `vocab/antiinfektiva.tsv`, `vocab/klinik.tsv`, `vocab/alltag.tsv`. Each is UTF-8,
  tab-separated, with a header row. IDs are unique across all files.
- Several values in one cell (e.g. synonyms) are separated by `; `, sources by
  ` | `.
- Columns:
  - `id`: an ASCII slug of the German word, using a-z, 0-9 and `-` (ä → ae,
    ö → oe, ü → ue, ß → ss), e.g. `erreger`, `zentraler-venenkatheter`. It is
    the note GUID and the audio file name, so it never changes once assigned,
    even if the German term is corrected later.
  - `status`: `draft` or `ok`. Only `ok` rows are built, so drafts never reach
    a collection or a published edition. A row can only be `ok` once its
    `review` cell is empty; the build will enforce this.
  - `tags`: hierarchical topic tags, space-separated (`thema::probenmaterial`).
  - `de`: dictionary form; nouns with their article (`der Erreger`).
  - `de_plural`: plural with article, or `–` if there is none.
  - `de_ipa`: optional IPA, taken from Wiktionary (entry URL in `source`).
  - `de_synonyms`, `de_abbr`
  - `de_note`: a note on German, written in Ukrainian.
  - `uk`: dictionary form with stress marks.
  - `uk_gender`: `m`, `f`, `n` or `pl` (plural-only).
  - `uk_synonyms`: standard synonyms in real use.
  - `uk_abbr`
  - `uk_nonstandard`: common non-standard spellings (see "Ukrainian spelling").
  - `uk_note`: a note on Ukrainian, written in German.
  - `en`: the standard clinical English term, a bridge for English-speaking
    peers. It uses British spelling (`faeces`), as WHO and ECDC do. It is shown as a secondary line on the back of every card in both
    editions. It never appears on the front (it would give away cognates) and
    never gets a card direction of its own.
  - `example_de`, `example_uk`: optional example sentences, in our own wording.
  - `source`: references, e.g. Wiktionary entry URLs. Required whenever text is
    taken from Wiktionary.
  - `review`: open questions for reviewers, e.g. unverified stress, English
    wording to confirm, or Ukrainian text Claude wrote that needs a native
    check. It is written in English, the language German and Ukrainian
    reviewers share. It is never built into cards. Whoever resolves a
    question fixes the row and deletes the comment. Anything that can't be
    verified during a session goes here, so it isn't forgotten.
    Questions about Ukrainian words or style always go here, for the
    reviewers, and are not put to the user.
- Computed by the build, never stored in the word list:
  - audio (`audio/de/<id>.mp3`, `audio/uk/<id>.mp3`)
  - the KMU 2010 transliteration
  - Ukrainian without stress marks
  - gender labels in each audience's language
- Optional columns exist from the start even while mostly empty. Adding a field
  to an Anki note type later forces a one-way full sync, and it complicates
  updates for users of a published edition.

## Terminology

- Accuracy matters more than coverage. Use the terms that clinical and
  public-health practice actually uses, not literal translations. If a term
  can't be verified, flag it instead of guessing.
- German references: RKI, KRINKO recommendations, ART (Kommission Antiinfektiva,
  Resistenz und Therapie).
- Ukrainian references: orders and protocols of the МОЗ України, Центр
  громадського здоров'я України, and WHO materials in Ukrainian.
- English references: WHO, ECDC and CDC for infection prevention; EUCAST for
  susceptibility testing.
- Everyday language (`Ukrainisch::Alltag`): the vocabulary selection is
  checked against the Goethe-Institut/ÖSD word lists (A1, B1) for German
  (there is no official list for B2; *Profile Deutsch* covers it), and
  for Ukrainian against the state standard «Українська мова як іноземна.
  Рівні загального володіння А1 – С2» (НКСДМ decision No. 279 of 29 August
  2024, under revision in 2026) and the A1 lexical minimum «1000 і 1 слово»
  (HU Berlin, 2024). These lists are used only to look up single words: the
  scenarios decide what goes in, not the lists. Don't copy the lists, their
  selection or their example sentences, and don't compare our word list
  against them systematically (no coverage scripts, no copies in the repo).
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

## Transliteration

- Cards teach one Latin transliteration: the official Ukrainian system (KMU
  2010, Cabinet of Ministers Resolution No. 55 of 27 January 2010). It is
  ASCII-only, so it can be typed on German and English keyboards.
  - я, ю, є, ї, й → `Ya`, `Yu`, `Ye`, `Yi`, `Y` at the start of a word, and
    `ia`, `iu`, `ie`, `i`, `i` elsewhere.
  - ь and the apostrophe are dropped. зг → `zgh`.
  - Other letters: г `h`, ґ `g`, и `y`, і `i`, ж `zh`, х `kh`, ц `ts`, ч `ch`,
    ш `sh`, щ `shch`.
  - Test cases from the resolution: Zghorany, Znamianka, Feodosiia, Koropie,
    Yurii.
- The transliteration is computed from the Ukrainian field at build time, with
  stress marks removed first. It is never typed by hand. The `latin_translit`
  column of the lab CSV doesn't follow KMU 2010 (about half its rows use the
  older `ya`/`yu` style) and is discarded.
- It is for German speakers learning Ukrainian. Ukrainian speakers learning
  German don't need it.
- It is for writing, not pronunciation: it shows no stress, and г is written
  `h`. Stress marks and audio cover pronunciation.
- The rules are taught with about 40 rule cards in a separate deck
  (`Ukrainisch::Transliteration`). A per-word "type the transliteration" card
  type is not part of the default.
- Learners should *recognise* other systems but not produce them. The primer
  (deck description or README) carries a comparison table:
  - BGN/PCGN (`ya`/`yu`/`ye` in every position, soft sign marked)
  - earlier Ukrainian versions
  - German press transcription (`Kyjiw`, `Charkiw`, `Selenskyj`)
  - scholarly transliteration (`č`, `š`, `ž`, `ja`)
- Personal names are never re-transliterated. Use the spelling the person uses
  themselves.

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
- Everyday communication lives in the deck `Ukrainisch::Alltag`, a sibling of
  `Ukrainisch::Medizin`, with the word list `vocab/alltag.tsv`. It grows level
  by level from A1 to B2 (A1 → A2 → B1 first, then B2). Its content is
  selected from the scenario list in `docs/alltag-szenarien.md` (our own
  can-do statements, ordered by level), not from a general frequency list.
- `Ukrainisch::Alltag` has one subdeck per CEFR level: `::A1`, `::A2`, `::B1`,
  `::B2`. They sort in learning order, so studying the parent deck with the
  new-card gather order "Deck" introduces A1 before A2 and so on, and a
  learner can also study one level on its own.
  - Every row in `vocab/alltag.tsv` carries exactly one level tag
    (`niveau::a1` … `niveau::b2`): the level of the first scenario that needs
    it. The build puts the note in the matching subdeck.
  - The level is a property of the word list, not a field, so adding a level
    later needs no change to the note type (no forced full sync).
  - A note's level should not change once it has been released: re-importing
    a package updates notes but doesn't move existing cards to another deck.
- The word lists in the repo (`vocab/*.tsv`) are the source of truth. A build
  script in `tools/` generates two Anki packages (`.apkg`) from them:
  - an edition for German speakers learning Ukrainian, which the user imports
    into `Ukrainisch::Medizin::*`;
  - an edition for Ukrainian speakers learning German, built for publishing.

  Each edition has its own note type and card templates, and its labels and
  notes are in its audience's language. Every note has a stable ID, which the
  build uses as the note GUID, so importing a rebuilt package updates the
  existing notes and keeps the review history. The MCP server is used for
  checking the result, not for adding notes.
- Ukrainian is stored with stress marks (combining acute, U+0301). They are
  shown in the edition for German speakers and removed in the edition for
  Ukrainian speakers.
- Ukrainian stress is taken from Wiktionary. When Wiktionary has no entry, it
  is taken from the *Словник української мови* (1970–80) via slovnyk.ua. If
  slovnyk.ua has no stress for the word, goroh.pp.ua
  (`https://goroh.pp.ua/Тлумачення/<word>`) is used. The source is always
  cited in `source`. Words with no stress source at all get no stress mark and
  a `review` comment.
- The euphonic preposition follows the orthography: `із` between two
  consonants (`мазо́к із но́са`).
- `de_plural` is `–` when the plural isn't used in the card's sense, even if
  Wiktionary lists one (`Blute`, `Urine`; `Stühle` only means chairs).
- Grammatical gender is colour-coded in both languages and both editions, with
  one colour scheme for masculine, feminine, neuter and plural-only. German
  gender comes from the article, Ukrainian gender from `uk_gender`. It is hard
  for learners in both directions, and the two languages often disagree (`das
  Blut` vs. `кров`, f), so the same colours make such clashes visible. Each
  colour is paired with a text label, so the information never depends on
  colour alone.
- German audio is recorded by the user with `tools/record_audio.py` and saved
  as `audio/de/<ID>.mp3`. Nouns are recorded with their article ("die
  Blutkultur"). Ukrainian audio will follow later; the same script can record
  it (`--column uk --out audio/uk`).

## Open decisions

When a decision is made, move it to "Decisions" above.

- Tag vocabulary: which `thema::` tags, and whether to add source or status
  tags? The pilot uses `thema::probenmaterial` and `thema::medizinprodukt`.
  `Ukrainisch::Alltag` uses `niveau::` tags (see "Decisions"); proposed in
  addition: a scenario tag (`szenario::isolation`, …) matching
  `docs/alltag-szenarien.md`.
- Grammar: the vocabulary is shared, but each audience needs different grammar
  (Ukrainian cases, aspect and verbs of motion for German speakers; German
  articles, word order, Perfekt and Sie form for Ukrainian speakers). Proposed:
  rule cards with their own note type per edition, like the transliteration
  rule cards, kept outside `vocab/*.tsv`, with the same level subdecks
  (A1 … B2) so grammar and vocabulary advance together. Format and deck name
  still open.
- Phrases in `vocab/alltag.tsv`: proposed that a row may hold a whole phrase
  (`Bitte desinfizieren Sie sich die Hände.`), with `de_plural` and
  `uk_gender` empty, and that phrases addressed to patients use the formal
  address (Sie / ви).
- Overlap with `Ukrainisch::Anfänger`: the edition for German speakers sits
  next to that course, which already covers much of A1. Build the A1 notes into
  that edition anyway (they can be suspended by tag), or leave out what the
  course already teaches?
- Conventions used for `vocab/alltag.tsv`, not yet confirmed by the user:
  - Every polysyllabic Ukrainian word in `uk`, `uk_synonyms` and `uk_note`
    has its stress checked against the stress sources in "Decisions". For an
    inflected form in a phrase (`почува́юся`), `source` cites the entry of its
    lemma.
  - Phrases and notes in Ukrainian that Claude wrote get a `review` comment
    asking for a native check, even when every word's stress is confirmed.
- Ukrainian audio: a native speaker (same script) or text-to-speech?
- Should the recordings be published in the repo? `audio/` is gitignored until
  this is decided.
- Later, optionally: a trilingual glossary (German, English, Ukrainian as a
  web page or PDF) generated from the same word list, for colleagues who
  don't use Anki.
