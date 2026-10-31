# Ukrainisch — German ⇄ Ukrainian ⇄ English medical Anki cards

## Purpose

Anki cards for medical vocabulary in German, Ukrainian and English, with a
focus on:

- Infection prevention and control (IPC; Infektionsprävention / Krankenhaushygiene)
- Microbiology
- Antimicrobial stewardship (Antibiotic Stewardship, ABS)

A second part covers everyday communication from CEFR level A1 to B2, built
up level by level, with a focus on talking with patients, relatives and
colleagues in hospital, epidemiology, IPC and AMR settings (see
`docs/alltag-szenarien.md`).

All three languages are first-class: each has its own headword, synonyms,
IPA, example and audio in the word list. There are four editions, all
generated from the same word lists, and each note produces a card in both
directions of its edition's language pair:

| Edition | Audience |
| --- | --- |
| German → Ukrainian | German speakers learning Ukrainian (the user's own collection) |
| Ukrainian → German | Ukrainian speakers learning German |
| Ukrainian → English | Ukrainian speakers learning English |
| English → Ukrainian | English speakers learning Ukrainian (e.g. international colleagues) |

There is no German ⇄ English edition unless someone asks for one.

Information *about* a language is for learners *of* that language, so it's
written in their language. Notes are therefore written per language pair:
`<about>_note_<written in>`. `de_note_uk` is a note on German, in Ukrainian;
`uk_note_de` is a note on Ukrainian, in German; `uk_note_en` is a note on
Ukrainian, in English; `en_note_uk` is a note on English, in Ukrainian. A note
column exists only for pairs that have an edition.

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
- `tools/recorder/index.html` is a browser page for checking and recording in
  one go, for people who don't install anything (e.g. Ukrainian friends on a
  phone).
  - It loads `vocab/*.tsv` from the same site, so it must be served over HTTPS
    from the repository: GitHub Pages (Settings → Pages → Deploy from branch
    `main`, folder `/`) gives
    <https://brar.github.io/Ukrainisch/tools/recorder/>. Opened as a local
    file, it can't fetch the lists; they can then be opened with the file
    picker on the page instead.
  - The reader chooses a language, a topic (word list · level · scenario or
    `thema::` tag) and a part of at most 20 entries. By default only open
    entries are shown; "show finished entries too" allows re-checking and
    re-recording.
  - Per entry it shows the main form, synonyms, the note and example written
    in the reader's language, and the open review items for that language
    (`UK:` for Ukrainian readers, `DE:` for German readers, `EN:` for English
    readers, items without a prefix for everyone, and earlier readers'
    comments). The reader
    confirms ("all correct") or writes a correction, and records.
  - Ukrainian is shown without stress marks by default, so the reader isn't
    steered by our marks; a different stress in the recording points to a
    possible error.
  - Quality: browser processing (echo cancellation, noise suppression,
    automatic gain) is switched off and takes are stored as uncompressed WAV.
    After each take the page warns about clipping, a too quiet voice,
    background noise and takes longer than 10 s.
  - A take or check remembers the text it was made for. If the entry's text
    changes later, the take is marked as outdated and must be recorded again.
  - Everything stays in the browser (IndexedDB) until it is exported as a zip
    with WAV files and `manifest.tsv`. Nothing is uploaded.
  - The interface is in German, Ukrainian and English, and so is the choice of
    recording language. The Ukrainian interface text was written by Claude
    and still needs a native check.
- `tools/import_recordings.py <zip>…` imports such a zip:
  - takes are processed like `record_audio.py` and saved as
    `audio/<lang>/<id>.mp3` (existing files are kept unless `--overwrite`);
  - a confirmation removes the review items the reader was shown from the
    `review` column, and a comment is added to it as
    `Reader <name> (<lang>): …`;
  - takes and checks whose text no longer matches the word list are skipped;
  - at the end it lists draft rows without open review items, whose status
    can now be set to `ok`.
  The review item format is shared with the page: items start with `UK:`,
  `DE:`, `EN:`, `Build:` or `Reader <name> (<lang>):`.
- `tools/audio_processing.py` holds the shared processing (trim silence,
  normalise loudness, MP3), so both ways of recording sound the same.

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
  - `de_plural`: plural with article, or `–` if there is none. For a
    plural-only noun it repeats the headword (`die Eltern` in both `de` and
    `de_plural`); the build reads this as plural-only for the gender colour.
    `–` never means plural-only, so `die Hygiene` with `–` stays feminine.
  - `de_ipa`: optional IPA, taken from Wiktionary (entry URL in `source`).
  - `de_synonyms`, `de_abbr`
  - `de_verb_forms`: for verbs, the principal parts: 3rd person singular
    present, preterite, perfect (`hustet, hustete, hat gehustet`). Taken from
    Wiktionary.
  - `de_paradigm`: the full paradigm as a reference table, filled
    automatically from Wiktionary. Nouns: `N der Arzt / die Ärzte; G des
    Arztes / der Ärzte; D dem Arzt / den Ärzten; A den Arzt / die Ärzte`
    (singular / plural). Verbs: `pres huste, hustest, hustet; past hustete;
    perf hat gehustet; imp huste / hustet; subj2 hustete`.
  - `de_note_uk`: a note on German, written in Ukrainian.
  - `uk`: dictionary form with stress marks.
  - `uk_gender`: `m`, `f`, `n` or `pl` (plural-only).
  - `uk_plural`: nominative plural with stress marks, for nouns. Same rules as
    `de_plural`: `–` if the plural isn't used in the card's sense; for a
    plural-only noun it repeats the headword. Taken from Wiktionary.
  - `uk_genitive`: genitive singular with stress marks, for nouns (genitive
    plural for plural-only nouns); it shows the declension class and stress
    shifts. Multi-word terms are declined as a phrase (adjectives agree, a
    complement such as `із зі́ва` stays). Taken from goroh.pp.ua.
  - `uk_ipa`: optional IPA, taken from Wiktionary (entry URL in `source`).
  - `uk_aspect`: for verbs, the aspect of the headword (`impf`, `pf` or
    `biasp`), then a colon and its aspect partner(s) with stress marks,
    separated by `, `: `impf: кашляну́ти`, `pf: захво́рювати, хворі́ти`. Just
    `impf` if there is no partner. Taken from Wiktionary. The build shows the
    labels in the audience's language.
  - `uk_present`: for verbs, 1st and 2nd person singular of the present tense
    (of the simple future for perfective verbs), with stress marks:
    `говорю́, гово́риш`. It shows the conjugation class and stress shifts.
    Taken from goroh.pp.ua.
  - `uk_paradigm`: the full paradigm as a reference table, filled
    automatically from goroh.pp.ua (first variant of each form only). Nouns:
    `N о́ко / о́чі; G о́ка / оче́й; D …; A …; I …; L …; V …` (singular / plural;
    plural only for plural-only nouns). Verbs: `pres говорю́, гово́риш,
    гово́рить / гово́римо, гово́рите, гово́рять; past говори́в, говори́ла,
    говори́ло, говори́ли; imp говори́ / говорі́ть` (`fut` instead of `pres` for
    perfective verbs).
  - `uk_synonyms`: standard synonyms in real use.
  - `uk_abbr`
  - `uk_nonstandard`: common non-standard spellings (see "Ukrainian spelling").
  - `uk_note_de`: a note on Ukrainian, written in German.
  - `uk_note_en`: a note on Ukrainian, written in English.
  - `en`: the English headword, a real answer that can be learned (no
    explanations in it; those go in a note or a hint in parentheses). Nouns
    without an article. British spelling (`faeces`, `oesophagus`), as WHO and
    ECDC use it. In the editions with English it is the language learned. In
    the German ⇄ Ukrainian editions it is shown as a secondary line on the
    back of the card, as a bridge for English-speaking peers; it never appears
    on the front there (it would give away cognates).
    Both roles use the same cell, so `en` holds the standard term colleagues
    use: the clinical term in the medical lists (`pharynx`), plain everyday
    English in `Ukrainisch::Alltag` (`throat`). The other register goes into
    `en_synonyms`, not into the headword.
  - `en_plural`: plural, for nouns. Same rules as `de_plural`: `–` if the
    plural isn't used in the card's sense; for a plural-only or plural-form
    headword (`lungs`, `stairs`) it repeats the headword. Taken from
    Wiktionary.
  - `en_ipa`: optional British (Received Pronunciation) IPA, taken from
    Wiktionary (entry URL in `source`).
  - `en_verb_forms`: for verbs, simple past and past participle
    (`ate, eaten`; `coughed, coughed`). Taken from Wiktionary.
  - `en_synonyms`: synonyms in real use, including the US form where it
    differs (`diarrhea`, `acetaminophen`), so it is accepted but not taught as
    the main form.
  - `en_abbr`
  - `en_note_uk`: a note on English, written in Ukrainian.
  - `example_de`, `example_uk`, `example_en`: optional example sentences, in
    our own wording.
  - `source`: references, e.g. Wiktionary entry URLs. Required whenever text is
    taken from Wiktionary.
  - `review`: open questions for reviewers, e.g. unverified stress, English
    wording to confirm, or Ukrainian text Claude wrote that needs a native
    check. It is written in English, the language all reviewers share. Each
    item starts with the language its reviewer needs: `UK:`, `DE:` or `EN:`
    (general items have no prefix; `Build:` items are for the build). It is never built into cards. Whoever resolves a
    question fixes the row and deletes the comment. Anything that can't be
    verified during a session goes here, so it isn't forgotten.
    Questions about Ukrainian words or style always go here, for the
    reviewers, and are not put to the user.
- Computed by the build, never stored in the word list:
  - audio (`audio/de/<id>.mp3`, `audio/uk/<id>.mp3`, `audio/en/<id>.mp3`)
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
  susceptibility testing; NHS patient information for the everyday words
  patients use. Use British English; US variants go into `en_synonyms` or a
  note.
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
  The same applies to English learner lists (e.g. the *English Vocabulary
  Profile*): single-word lookups only.
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
- It is for German and English speakers learning Ukrainian. Ukrainian
  speakers learning German or English don't need it.
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
  script in `tools/` generates one Anki package (`.apkg`) per edition (see
  "Purpose"): German → Ukrainian (which the user also imports into
  `Ukrainisch::*`), Ukrainian → German, Ukrainian → English and English →
  Ukrainian.

  All four editions are published. None is only for private use. The deck
  names of the published editions are still open.

  Each edition has its own note type and card templates, and its labels and
  notes are in its audience's language. Every note has a stable ID, which the
  build uses as the note GUID, so importing a rebuilt package updates the
  existing notes and keeps the review history. The MCP server is used for
  checking the result, not for adding notes.
- Ukrainian is stored with stress marks (combining acute, U+0301). They are
  shown in the editions for learners of Ukrainian (German → Ukrainian,
  English → Ukrainian) and removed in the editions for Ukrainian speakers.
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
- When two notes share a headword, a short hint in parentheses tells them
  apart: `der Hals (innen)` (`го́рло`) and `der Hals (außen)` (`ши́я`). The
  hint is shown on the card but not spoken in the recording.
- Inflection is trained in Anki, not only looked up:
  - Form cards: extra card templates in each edition's note type ask for
    the key forms (`uk_plural`, `uk_genitive`, `uk_present`, `uk_aspect`,
    `de_plural`, `de_verb_forms`, `en_plural`, `en_verb_forms`). Anki only
    creates a card when the field is filled. They go to their own subdeck
    via a deck override, so they can be suspended or started later.
  - Paradigms (`de_paradigm`, `uk_paradigm`) are shown as a reference table
    on the back of the card. They are never drilled form by form, which
    would mean thousands of near-identical cards.
  - Cases and their use are trained in context (cloze cards in the grammar
    module); complete paradigms are drilled only for a few model words per
    declension or conjugation type.
- Grammatical gender is colour-coded for German and Ukrainian in every edition
  that shows them (English has no grammatical gender), with
  one colour scheme for masculine, feminine, neuter and plural-only. German
  gender comes from the article, Ukrainian gender from `uk_gender`. It is hard
  for learners in both directions, and the two languages often disagree (`das
  Blut` vs. `кров`, f), so the same colours make such clashes visible. Each
  colour is paired with a text label, so the information never depends on
  colour alone.
- German audio is recorded by the user with `tools/record_audio.py` and saved
  as `audio/de/<ID>.mp3`. Nouns are recorded with their article ("die
  Blutkultur"). Ukrainian and English audio will follow later; the same script
  can record them (`--column uk --out audio/uk`, `--column en --out
  audio/en`).
- Audio is switched on or off per language and per package: German, Ukrainian
  and English audio each have their own switch in the build. A package for the
  user's own collection includes all recordings there are. A package for
  publishing includes a language's audio only when every speaker of it has
  agreed in writing to publication under CC BY-SA 4.0. Otherwise that package
  ships without audio for that language.
- No audio with a wrong pronunciation is published. Text-to-speech is never
  used without a native speaker listening to every file, and files that fail
  that check are dropped.

## Open decisions

When a decision is made, move it to "Decisions" above.

- Tag vocabulary: which `thema::` tags, and whether to add source or status
  tags? The pilot uses `thema::probenmaterial` and `thema::medizinprodukt`.
  `Ukrainisch::Alltag` uses `niveau::` tags (see "Decisions"); proposed in
  addition: a scenario tag (`szenario::isolation`, …) matching
  `docs/alltag-szenarien.md`.
  Children's words (for paediatrics) carry `register::kindersprache`, and
  their notes name the word adults use.
- Grammar module: the vocabulary is shared, but each audience needs different
  grammar (Ukrainian cases, aspect and verbs of motion for German and English
  speakers; German articles, word order, Perfekt and Sie form, and English
  tenses, for Ukrainian speakers). Proposed: rule cards plus cloze cards that
  practise each rule in a phrase from our scenarios (`У ме́не боли́ть
  {{голова́}}`), and full paradigms for a few model words per declension or
  conjugation type, with their own note type per edition, kept outside
  `vocab/*.tsv`, in the same level subdecks (A1 … B2) so grammar and
  vocabulary advance together. Format and deck name still open.
- Phrases in `vocab/alltag.tsv`: proposed that a row may hold a whole phrase
  (`Bitte desinfizieren Sie sich die Hände.`), with `de_plural` and
  `uk_gender` empty, and that phrases addressed to patients use the formal
  address (Sie / ви).
- Overlap with `Ukrainisch::Anfänger`: the edition for German speakers sits
  next to that course, which already covers much of A1. Build the A1 notes into
  that edition anyway (they can be suspended by tag), or leave out what the
  course already teaches?
- Conventions used for `vocab/alltag.tsv`, not yet confirmed by the user:
  - Every polysyllabic Ukrainian word in `uk`, `uk_synonyms`, `de_note_uk`
    and `en_note_uk`
    has its stress checked against the stress sources in "Decisions". For an
    inflected form in a phrase (`почува́юся`), `source` cites the entry of its
    lemma.
  - Phrases and notes in Ukrainian that Claude wrote get a `review` comment
    asking for a native check, even when every word's stress is confirmed.
- Ukrainian audio: recorded by Ukrainian friends (with the browser recorder
  `tools/recorder/`). Do they agree to publication (then it
  goes into the public packages), or is it for the user's own collection only?
  Text-to-speech with a native listening check remains a fallback.
- English audio: a native speaker, or text-to-speech with a listening check by
  a native or very good English speaker (English TTS is much more reliable
  than Ukrainian, but the rule against wrong pronunciations still applies)?
- English content: the `en` cells have had a first cleanup pass (one learnable
  headword, alternatives and US forms in `en_synonyms`, abbreviations in
  `en_abbr`; `uk_note_en` translated from `uk_note_de`). Still open: `en_ipa`,
  `en_note_uk` and `example_en` are empty, and the English in the word lists
  has not been checked by a native or very good English speaker yet (the
  `EN:` items in `review` are the explicit questions).
- Should the recordings be published, in the repo and in the public packages?
  This applies to the user's own German recordings as well. `audio/` is
  gitignored until this is decided.
- Later, optionally: a trilingual glossary (German, English, Ukrainian as a
  web page or PDF) generated from the same word list, for colleagues who
  don't use Anki.
