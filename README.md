# Ukrainisch

[Anki](https://apps.ankiweb.net/) cards for medical vocabulary in German,
Ukrainian and English, in four editions:

- German → Ukrainian, for German speakers learning Ukrainian
- Ukrainian → German, for Ukrainian speakers learning German
- Ukrainian → English, for Ukrainian speakers learning English
- English → Ukrainian, for English speakers learning Ukrainian

Every note is studied in both directions of its edition's language pair.

## Focus areas

- Infection prevention and control (Infektionsprävention und Krankenhaushygiene)
- Microbiology
- Antimicrobial stewardship (Antibiotic Stewardship, ABS)
- Everyday communication from CEFR level A1 to B2, focused on hospital,
  epidemiology, IPC and AMR settings

## Terminology sources

The goal is the terminology used in clinical and public-health practice, not
literal translations. Terms are checked against:

- **German:** Robert Koch-Institut (RKI), KRINKO recommendations, and the ART
  commission (Kommission Antiinfektiva, Resistenz und Therapie)
- **Ukrainian:** orders and protocols of the Ministry of Health of Ukraine
  (МОЗ України), the Public Health Center of Ukraine (Центр громадського
  здоров'я України), and WHO materials in Ukrainian
- **English:** WHO, ECDC and CDC; EUCAST for susceptibility testing; NHS
  patient information for everyday words

Ukrainian follows the current standard orthography (2019). English uses
British spelling, as WHO and ECDC do.

## Status

Early setup; no cards published yet.

## How the cards are made

The word lists in [`vocab/`](vocab/) are the source of truth: one
tab-separated file per deck, edited with the help of
[Claude Code](https://claude.com/claude-code). A build script in
[`tools/`](tools/) will generate two Anki packages (`.apkg`) from them, one for
German speakers learning Ukrainian and one for Ukrainian speakers learning
German. Every note has a stable ID, so importing a rebuilt package updates the
existing cards and keeps their review history. The
[AnkiMCP add-on](https://github.com/ankimcp/anki-mcp-server-addon) is used to
check the result in Anki. Audio is recorded with
[`tools/record_audio.py`](tools/record_audio.py) or, without installing
anything, with the browser recorder in [`tools/recorder/`](tools/recorder/)
and imported with [`tools/import_recordings.py`](tools/import_recordings.py).

## Disclaimer

These cards are a language-learning aid. They are not a clinical reference.
Always follow current guidelines and local protocols when making clinical
decisions.

## License

© 2026 Brar Piening. Licensed under
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/);
see [LICENSE](LICENSE).

Suggested attribution: *"Ukrainisch" by Brar Piening,
<https://github.com/Brar/Ukrainisch>, licensed under CC BY-SA 4.0.*

Where a note adapts text from [Wiktionary](https://www.wiktionary.org/) (CC
BY-SA 4.0), it links to the Wiktionary entry it draws on.

The scripts in [`tools/`](tools/) are licensed under the MIT License; see
[tools/LICENSE](tools/LICENSE).
