# Translation resources and know-how (German · Ukrainian · English)

A summary of the sources, standards, conventions and pitfalls collected while
building this project, written so it can be reused in other German,
Ukrainian and English vocabulary or translation projects. Project-specific
rules live in `CLAUDE.md`; this document keeps what is transferable.

## 1. Dictionaries and lexical sources

### Overview

| Source | Languages | Best for | Licence of its text |
| --- | --- | --- | --- |
| [English Wiktionary](https://en.wiktionary.org/) | Ukrainian, English | Ukrainian stress, IPA, genitive and nominative plural, verb aspect partners, inflection tables; English plurals, verb forms, British IPA | CC BY-SA 4.0 |
| [German Wiktionary](https://de.wiktionary.org/) | German | Plural, IPA, full noun and verb tables | CC BY-SA 4.0 |
| [slovnyk.ua](https://slovnyk.ua/) | Ukrainian | Stress from the *Словник української мови* in 11 volumes (1970–80), for lemmas | dictionary content; use facts only |
| [goroh.pp.ua](https://goroh.pp.ua/) | Ukrainian | Definitions with stress (*Тлумачення*), complete inflection tables with stress (*Словозміна*) | use facts only |
| [e2u.org.ua](https://e2u.org.ua/) | Ukrainian | A second check for orthography and stress | use facts only |
| [DWDS](https://www.dwds.de/) | German | Forms, usage, frequency | use facts only |
| [NHS](https://www.nhs.uk/) | English | The everyday words patients actually use | use facts only |

"Use facts only" means taking words, forms and stress marks, never copying
definitions or example sentences.

### English Wiktionary (Ukrainian and English entries)

- Pages: `https://en.wiktionary.org/wiki/<word>`. Read the section under
  `id="Ukrainian"` or `id="English"`, up to the next `<h2>`.
- **Stressed headword:** `<strong class="Cyrl headword" lang="uk">лі́кар</strong>`.
  Stress is a combining acute (U+0301) after the vowel.
- **Inflected forms with stress:** `<span class="Cyrl form-of lang-uk …">`.
  Pages for inflected forms (e.g. *розумі́ю*) exist too, so stress in a
  phrase can often be confirmed form by form.
- **Ukrainian noun headword line:** "genitive о́ка, nominative plural о́чі, …".
- **Ukrainian verb headword line:** "impf (perfective кашляну́ти)" or
  "pf (imperfective хворі́ти or захво́рювати)".
- **IPA:** `<span class="IPA">`. For English, take the one after "Received
  Pronunciation" for British pronunciation.
- **English headword line:** "(plural teeth)", "(uncountable)", "(simple past
  ate, past participle eaten)". Regular verbs read "simple past and past
  participle coughed", so a naive "simple past (\w+)" pattern returns "and".
- **Inflection tables** (`class="inflection-table"`):
  - Each form has its transliteration glued to it (*сні́даюsnídaju*), so keep
    only the Cyrillic part.
  - Strip footnote digits (*допомо́ги1*).
  - Adjective tables merge the masculine and neuter cells and split the
    accusative into animate and inanimate rows.
  - An adjective table also starts with a "singular / plural" header, so
    check for gender columns before treating it as a noun table.

### German Wiktionary

- Raw wikitext: `https://de.wiktionary.org/w/index.php?action=raw&title=<Wort>`.
- **Use only the German section** (`== … ({{Sprache|Deutsch}}) ==`). A page can
  hold French or Czech entries too, with their own IPA and references.
- **IPA:** `{{IPA}} {{Lautschrift|…}}`.
- **Nouns:** the `Deutsch Substantiv Übersicht` template has fields
  `|Genus=`, `|Nominativ Singular=`, `|Genitiv Plural=` and so on.
  - Variants are numbered (`Genus 1`, `Genitiv Singular 1`), and some
    fields carry a `*`.
  - Plural-only nouns have `Genus=0` and `—` in the singular.
- **Verbs:** `Präsens_ich`, `Präsens_du`, `Präsens_er, sie, es`,
  `Präteritum_ich`, `Partizip II`, `Hilfsverb`, `Imperativ Singular`,
  `Konjunktiv II_ich`. Separable verbs give *steckt an*, *steckte an*.
- **Redirects** (`#WEITERLEITUNG [[…]]`) and **form-of pages**
  (`{{Grundformverweis Dekl|Windpocke}}`) point to the lemma; follow them,
  but only from the German section.
- Adjectival nouns (*der Angehörige*) use a different template.

### slovnyk.ua

- URL: `https://slovnyk.ua/index.php?swrd=<слово>`.
- The stressed vowel is marked as `<span class="nagolos">І</span>` inside
  `<b>` headwords.
- Two marks in one word mean two permitted stresses (*бо́ляче́*).
- Lemmas only, no inflected forms.

### goroh.pp.ua

- Definitions with stress: `https://goroh.pp.ua/Тлумачення/<слово>`.
- Inflection: `https://goroh.pp.ua/Словозміна/<слово>`. The tables have the
  rows *називний … кличний*. Noun columns are *однина / множина*; adjective
  columns are *чол. р. / жін. р. / сер. р. / множина*.
- **Pitfalls:**
  - **A page lists several lexemes**: related or similar words (*тра́вень* shows
    *травни́й*, *сні́дати* shows *сніда́нок*), capitalised proper nouns with
    odd stress, and old unstressed spellings. Use only the table whose base
    form matches the word exactly, including its stress (*леге́ні* is not
    *ле́гені*).
  - **The first variant is not always standard:** an archaic form first
    (*ві́чі* before *о́чі*), the short form first (*говорі́м* before
    *говорі́мо*), and for *біль* the colloquial feminine table (*бі́лі*)
    before the standard masculine one (*бо́лю*). Cross-check the genitive
    with Wiktionary's headword line.
  - **Two stress marks** in a form mean both stresses are permitted
    (*ро́ки́*).
  - Adjective tables have no vocative (it equals the nominative).
  - Many derived adjectives (*головни́й*, *шлунко́вий*) have no entry; fall
    back to Wiktionary.

### Reachability and polite access

- Send a descriptive User-Agent with a project URL (no personal data), pace
  requests at about 1.5–2 s, back off on HTTP 429, and cache every page.
- The Wiktionary API (`api.php`, `action=raw` on en.wiktionary) hit rate
  limits quickly; plain HTML pages worked.
- From a cloud sandbox, `sum.in.ua` and `www.drlz.com.ua` reset the
  connection (the sites themselves, not the allow-list). The State Register
  (drlz) still has to be checked by hand.
- Allow-list used for this work: `en.wiktionary.org`, `de.wiktionary.org`,
  `slovnyk.ua`, `goroh.pp.ua`, `e2u.org.ua`, `www.dwds.de`, `www.nhs.uk`,
  plus package managers (PyPI).

## 2. Terminology authorities (medical, IPC, AMR)

| Language | Sources |
| --- | --- |
| German | Robert Koch-Institut (RKI), KRINKO recommendations, ART (Kommission Antiinfektiva, Resistenz und Therapie) |
| Ukrainian | Orders and protocols of the МОЗ України, Центр громадського здоров'я України (phc.org.ua), WHO materials in Ukrainian; drug names: Ukrainian INN (МНН) spelling in the *Державний реєстр лікарських засобів України* |
| English | WHO, ECDC and CDC for infection prevention; EUCAST for susceptibility testing; NHS for patient language |

- Use the term clinical and public-health practice actually uses, not a
  literal translation. If a term can't be verified, flag it instead of
  guessing.

### Specialist sources for IPC and AMR (searched in November 2026)

Entries marked "not checked here" are well-known sources that were not
looked up in that search; everything else was found and its details
confirmed. None of them has been used for word-list rows yet.

The most valuable sources are **parallel definitions**: documents in each
language that define the same things, e.g. the same types of
healthcare-associated infection (HAI). Equivalent terms can be read off side
by side, instead of translating word by word.

| Topic | German | Ukrainian | English |
| --- | --- | --- | --- |
| HAI definitions and surveillance | KISS definitions of the NRZ (e-book, edition 06/2017; replaced the CDC definitions in KISS from 2017; summary in Epidemiologisches Bulletin 23/2017, edoc.rki.de) | Public Health Center (phc.org.ua): programme for HAI surveillance, document on routine surveillance of ІПНМД | ECDC point prevalence survey protocol 6.1 (PPS 2022–2023), with HAI and antimicrobial-use definitions and code lists; CDC NHSN definitions (not checked here) |
| IPC organisation, hand hygiene | KRINKO recommendations (RKI); HAND-KISS protocol of Aktion Saubere Hände | Наказ МОЗ від 03.08.2021 № 1614 (registered with the Ministry of Justice under № 1318/36940; amended in April 2023), with the instruction on hand hygiene and the regulations for the infection control department (ВІК) | WHO guidelines on hand hygiene, WHO core components for IPC (not checked here) |
| Antibiotic stewardship | S3 guideline "Strategien zur Sicherung rationaler Antibiotika-Anwendung im Krankenhaus" (AWMF 092-001, update 2018, marked as expired and under revision); ART statements (not checked here) | Наказ МОЗ від 23.08.2023 № 1513 (standard for the rational use of antibacterial and antifungal drugs, uses WHO AWaRe); Наказ МОЗ від 09.09.2026 № 1328 (standards for primary care; check whether it replaces № 1513) | WHO AWaRe classification and antibiotic book (CC BY-NC-SA: for checking terms only) |
| Susceptibility testing | EUCAST (whether a German version exists: not checked) | no Ukrainian EUCAST translation found; EUCAST has translation pages for other languages | EUCAST breakpoint tables and definitions (S, I, R) |

- National translations of the ECDC protocol (e.g. Italian on epicentro.iss.it)
  show how other countries rendered the same definitions.
- No official Ukrainian MeSH was found; only the Russian MeSH (Moscow) is
  documented.
- Not tested yet: Wikidata labels (CC0) as a licence-free source of term
  equivalents for diseases and organisms.
- Copyright: Ukrainian official acts (laws, orders) are generally not
  protected, but guidelines, KRINKO recommendations and WHO texts are. Use them
  to check terms; write definitions and examples in your own words.
- WHO publications are usually CC BY-NC-SA 3.0 IGO: fine for checking a
  term, but not for copying sentences into a CC BY-SA project.

## 3. Language-learning standards (CEFR)

| Language | Standard or list | Note |
| --- | --- | --- |
| all | CEFR A1–C2 | The shared backbone for levels |
| German | Goethe-Institut/ÖSD word lists (A1, B1); *Profile Deutsch* (A1–C2) | No official B2 word list |
| German, medical | telc Deutsch B1·B2 Pflege; telc Deutsch B2·C1 Medizin; *Fachsprachprüfung* of the medical chambers (C1) | Scenario-based, no word lists |
| Ukrainian | State standard «Українська мова як іноземна. Рівні загального володіння А1 – С2» (НКСДМ decision No. 279, 29 Aug 2024; under revision in 2026) | Can-do descriptions and grammar per level |
| Ukrainian | «1000 і 1 слово» (HU Berlin, 2024) | A1 lexical minimum only |
| English | *English Vocabulary Profile* | Learner levels per word and sense |

- **Use these lists for single-word lookups only.** Copying a list, its
  selection or its example sentences can infringe copyright or database
  rights; comparing a word list against them systematically comes close to
  that.
- What worked better: our own **scenario list** of can-do statements per level
  (e.g. "explain the rules of an isolation room"), with vocabulary chosen
  because a scenario needs it.

## 4. Orthography and conventions

### Ukrainian

- **Orthography:** standard is the *Український правопис* of 2019. Avoid
  Russisms and calques from Russian.
- **Stress:** combining acute U+0301 after the vowel. Never use precomposed
  look-alikes or Latin letters (a Latin *i* in *пацiєнт* slipped in once).
  One-syllable words get no mark.
- **Apostrophe:** ASCII `'` (U+0027) only. Mixing it with `’` (U+2019) or `ʼ`
  (U+02BC) breaks searching.
- **правило дев'ятки:** in loanwords, after д, т, з, с, ц, ж, ч, ш, р, write
  и before a consonant (*цефтазидим*, *рифампіцин*, *триметоприм*).
- **Euphony:** у / в alternate (*учо́ра* / *вчо́ра*), and so do з / із / зі
  (*мазо́к із но́са* between two consonants).
- **Transliteration:** the official KMU 2010 system (Cabinet of Ministers
  Resolution No. 55, 27 January 2010).
  - It is ASCII-only.
  - Word-initial я, ю, є, ї, й give `Ya`, `Yu`, `Ye`, `Yi`, `Y`; elsewhere
    they give `ia`, `iu`, `ie`, `i`, `i`.
  - ь and the apostrophe are dropped, and зг becomes `zgh`.
  - Test cases from the resolution: Zghorany, Znamianka, Feodosiia, Koropie,
    Yurii.
  - Other systems to recognise: BGN/PCGN, German press transcription (*Kyjiw*),
    scholarly (*č, š, ž, ja*).
  - Personal names keep the spelling the person uses.
- **Feminine forms:** *лі́карка*, *переклада́чка*, *ро́дичка* are standard and
  in real use.
- **Polite address:** formal *ви* with patients. The vocative is used for
  address: *па́не Іва́не*, *па́не Петре́нку*; *па́ні* does not decline.

### German

- Nouns are given with their article. The plural is given with its article,
  or as `–` if it isn't used in that sense (*Blut*, *Urin*; *Stühle* only
  means chairs).
- Job titles: *Pflegefachfrau / Pflegefachmann* since 2020 (Pflegeberufegesetz);
  *Krankenschwester / Krankenpfleger* remain valid, protected titles.

### English

- British spelling (*faeces*, *oesophagus*, *centimetre*), as WHO and ECDC
  use it. US forms (*feces*, *elevator*, *acetaminophen*) are accepted
  synonyms, not mistakes.
- Clinical register in medical lists (*pharynx*), plain English for patient
  communication (*throat*, *flu*, *womb*, *belly button*).

### Cultural and structural traps worth a note on the card

- **Floor numbering:**
  - German and British English count from the ground floor (*Erdgeschoss* /
    *ground floor*, then *1. Stock* / *first floor*).
  - Ukrainian and American English count from the first floor (*пе́рший
    по́верх* / *first floor*, then *дру́гий по́верх* / *second floor*).
- **Half hours:** German and Ukrainian count towards the next hour (*halb neun*,
  *пів на дев'я́ту*); English counts from the previous one (*half past
  eight*).
- **One word, two concepts:**
  - Ukrainian *рука́* means both arm and hand, and *нога́* both leg and foot;
    *чолові́к* means both man and husband.
  - German *Hals* means both throat (*го́рло*) and neck (*ши́я*); *Frau*
    means both woman and wife.
- **Gender clashes**: *das Kind* / *дити́на* (f), *das Mädchen* / *ді́вчинка*
  (f), *der Mensch* / *люди́на* (f), *die Treppe* / *схо́ди* (pl), *das Obst*
  / *фру́кти* (pl).
- **Number clashes**: *die Lunge* / *леге́ні* (pl) / *lungs*; *das Haar* /
  *воло́сся* (collective) / *hair* (uncountable).
- **Words that differ only in stress:**
  - *о́рган* (organ) / *орга́н* (instrument);
  - *я́сна* (gums) / *ясна́* (bright);
  - *за́мок* (castle) / *замо́к* (lock).
- **Homograph on the German side:** *nüchtern* means both fasting and sober.

## 5. Grammar facts that drove data decisions

- **Accusative follows animacy:**
  - inanimate nouns take the nominative form (*о́чі*, *пе́рші допомо́ги*);
  - animate nouns take the genitive form (*лі́каря*, *діте́й*);
  - adjectives in a phrase follow their head noun;
  - a substantivised adjective such as the month *лю́тий* is inanimate.
- **Verbs come in aspect pairs:** *ка́шляти* (impf) – *кашляну́ти* (pf),
  *захворі́ти* (pf) – *хворі́ти* / *захво́рювати* (impf). Perfective verbs have
  a simple future (*захворі́ю*) instead of a present tense.
- **The 1st and 2nd person singular show stress shifts** a learner can't
  predict (*говорю́, гово́риш*). Dictionaries list them for that reason.
- **The genitive singular shows the declension class** and stress shifts
  (*о́ко → о́ка*, *біль → бо́лю*, *пупо́к → пупка́*).
- **Numbers and nouns:** 1 рік, 2–4 ро́ки, 5+ ро́ків (genitive plural).
- **Clock times:** о + ordinal in the locative (*о во́сьмій*); *годи́ні* is
  optional.

## 6. Licensing know-how

- **Single terms and their equivalents** can be taken from any source.
- **Wiktionary text** (CC BY-SA 4.0) may be adapted; record the entry URL and
  say if the text was changed.
- **NonCommercial sources** (e.g. WHO, CC BY-NC-SA) can't go into a CC BY-SA
  project; write your own wording instead.
- **Curated word lists:** don't copy them wholesale, because their selection
  may be protected (database rights).
- **Books** (e.g. a picture book given as a present): take single words,
  never sentences or labelled pictures.
- **Voice recordings:** a speaker must agree in writing before their voice is
  published, because CC BY-SA can't be withdrawn once shared. "For personal
  use only" can later be upgraded to publication; the reverse is impossible.
- **Code** is better placed under MIT (or similar) than under a CC licence.

## 7. Working method that proved itself

- **Verify everything Claude writes against a source.** In this project the
  automated checks caught eight wrong stress marks in Claude's own drafts:

  | Wrong | Right |
  | --- | --- |
  | перекла́дач | переклада́ч |
  | говори́те | гово́рите |
  | нарі́во (not a word) | налі́во |
  | боля́че | бо́ляче / боляче́ |
  | пле́че | плече́ |
  | восьми́й | во́сьмий |
  | натщесе́рце | натще́серце |
  | позаду́ | поза́ду |

  If no source confirms a stress, drop the mark and ask a reviewer rather
  than guess.
- **Use two sources and surface disagreements.** Compare goroh with
  Wiktionary, and send real conflicts to a reviewer (*чолові́ки* vs.
  *чоловіки́*) instead of choosing silently.
- **Match exactly, including stress.** Matching on spelling alone pulls in the
  wrong lexeme.
- **Keep a review column** in English (the reviewers' shared language). Start
  each item with `UK:`, `DE:` or `EN:`, so each reviewer sees only their own
  questions. Native-speaker questions go there, not to the project owner.
- **Mark everything Claude wrote in Ukrainian** (phrases, notes) for a native
  check, even when all stress is confirmed.
- **Data model:**
  - Give each entry a stable ID that never changes.
  - Use one headword per language, with alternatives as synonyms.
  - Disambiguate shared headwords with a hint in parentheses (*der Hals
    (innen)*), which is not spoken in recordings.
  - Name notes per language pair (`uk_note_de`: on Ukrainian, written in
    German).
  - Add every field you'll need before the first release: in Anki, adding a
    field later forces a full sync for every user.
- **Inflection in Anki:**
  - key forms become separate form cards;
  - full paradigms are shown as a reference table only;
  - cases are trained in context (cloze);
  - complete paradigms are drilled only for a few model words per type.

## 8. Audio and native-speaker review

- **Text-to-speech for Ukrainian is risky**, because stress isn't predictable
  from spelling. Words that differ only in stress, rare medical words and
  words with two permitted stresses go wrong. Publish TTS audio only after a
  native speaker has listened to every file. English TTS is far more
  reliable, but the same rule applies.
- **A browser recorder** (here `tools/recorder/`) lowers the effort for
  helpers to a link: no installation, one entry per screen, export as a zip.
  - **Settings:** switch off echo cancellation, noise suppression and
    automatic gain; record WAV; process later (trim, normalise, MP3).
  - **Checks after each take:** clipping, a too quiet voice, background noise
    (the gap between speech and the quietest frames), takes over 10 s.
  - **Review while recording:** show Ukrainian without stress marks. A
    different stress in the recording then points to an error in the data.
  - **Outdated takes:** store the text each take was made for, and refuse
    takes whose text has changed since.
- **Recording tips for helpers:** a quiet room with soft furnishings, the
  microphone about 20 cm away and always the same distance, a test take
  first, natural speed.
