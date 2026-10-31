# Scenarios for `Ukrainisch::Alltag`

This list decides what goes into `vocab/alltag.tsv` and the grammar rule
cards. Each scenario is a can-do statement in our own wording, in the style of
the CEFR, *Profile Deutsch* and the Ukrainian state standard «Українська мова
як іноземна. Рівні загального володіння А1 – С2». A word or phrase belongs in
the deck if one of these scenarios needs it.

The deck grows level by level: A1 → A2 → B1 first, then B2. A1 and A2 build
the basics that the hospital scenarios rely on. Each scenario has a tag
(`szenario::…`), and every note also gets the level of the first scenario
that needs it (`niveau::a1` … `niveau::b2`), which decides its subdeck
(`Ukrainisch::Alltag::A1` … `::B2`).

"I" is a health worker (doctor, nurse, IPC staff, public-health staff).
"You" is a patient, relative, visitor or colleague. Patients are addressed
formally (Sie / ви).

Status: draft for review. Nothing here has been checked against the official
level descriptors yet.

## A1: basics

| Tag | I can … |
| --- | --- |
| `szenario::kontakt` | greet someone, say who I am and what my job is, ask for a name, say goodbye. |
| `szenario::hoeflichkeit` | say please, thank you and sorry, and make a simple polite request ("Please sit down"). |
| `szenario::verstaendigung` | say that I don't understand, ask someone to repeat, speak slowly or spell something. |
| `szenario::zahlen-zeit` | use numbers, the time, days, dates and simple quantities (temperature, room number, age, date of birth). |
| `szenario::koerper` | name the main body parts and organs, and ask or say where it hurts. |
| `szenario::befinden` | ask how someone is and understand simple answers (pain, cold, hungry, thirsty, tired, better, worse). |
| `szenario::orientierung` | ask for and give the way inside a hospital (ward, room, floor, left, right, lift, toilet). |
| `szenario::personen` | talk about family members and who is visiting. |

## A2: simple routine situations

| Tag | I can … |
| --- | --- |
| `szenario::symptome` | ask about common symptoms and since when (fever, cough, diarrhoea, vomiting, rash), and understand the answers. |
| `szenario::haendehygiene` | tell a patient or visitor, step by step, when and how to disinfect their hands. |
| `szenario::schutzkleidung` | ask someone to put on or take off a mask, gown or gloves, and explain the order. |
| `szenario::isolation` | explain the basic rules of an isolation room: who may come in, what the patient may and may not do. |
| `szenario::probe` | ask for a specimen (urine, stool, swab) and explain in simple words what will happen. |
| `szenario::medikamente` | explain when and how often to take a medicine, and ask about allergies. |
| `szenario::termine` | arrange a time, also on the phone, and take down a name and number. |
| `szenario::kollegen` | have small talk with colleagues about shifts, breaks and the working day. |

## B1: hospital, epidemiology, IPC and AMR

| Tag | I can … |
| --- | --- |
| `szenario::isolation-gruende` | explain why someone is isolated (e.g. colonisation with a resistant organism), that this is not a punishment, and what it means for visitors and for after discharge. |
| `szenario::befund` | explain a test result in plain language (positive, negative, colonised, infected, resistant), and say what happens next. |
| `szenario::antibiotika` | explain that antibiotics don't help against viral infections, why to take them exactly as prescribed, and what side effects to report. |
| `szenario::impfung` | give a vaccination recommendation, answer common worries and say what to do after the vaccination. |
| `szenario::ausbruch` | interview someone in an outbreak investigation: symptoms and onset, places, food, travel, contacts, and when they were where. |
| `szenario::meldung` | report a case or an outbreak to a colleague or the health authority on the phone, and understand follow-up questions. |
| `szenario::schulung` | give a short training to staff (e.g. the moments of hand hygiene) and check that it was understood. |
| `szenario::sorgen` | respond to worries, fear and complaints with empathy, and reassure without promising too much. |
| `szenario::schriftlich` | understand and write short texts: a door sign, a patient information sheet, a short e-mail. |

## B2: discussion, persuasion, professional exchange

| Tag | I can … |
| --- | --- |
| `szenario::risiko` | explain risk and uncertainty: what is known, what isn't, and what the probabilities mean for this person. |
| `szenario::ablehnung` | handle a refusal (of isolation, a test, a vaccination): listen to the reasons, argue my case and look for a solution together. |
| `szenario::sanierung` | counsel a patient on decolonisation and on what colonisation means for them and their household in the long run. |
| `szenario::surveillance` | present and discuss surveillance data (cases, rates, incidence, trends) in a team meeting. |
| `szenario::ausbruchsteam` | take part in an outbreak team meeting: report findings, propose measures, weigh pros and cons. |
| `szenario::visite` | take part in a ward round or infectious diseases consultation on antibiotic therapy (indication, choice, duration, de-escalation). |
| `szenario::oeffentlichkeit` | explain a public-health situation to the public or the press in clear, calm language. |
| `szenario::fachtext` | understand the main points of a guideline or a professional article and summarise them for colleagues. |

Note on `szenario::antibiotika`: the current advice is to take antibiotics
exactly as prescribed, not "always finish the pack". Cards must not teach the
old message.

## Grammar by level

Rule cards follow the same levels. The two editions need different rules:

| Level | German, for Ukrainian speakers | Ukrainian, for German speakers |
| --- | --- | --- |
| A1 | articles and gender; present tense; verb in second position; W- and yes/no questions; Sie form; accusative; negation with *nicht* / *kein*; *können*, *müssen*, *dürfen* | noun gender; present tense, both conjugations; personal pronouns and formal ви; nominative and accusative; questions with чи; no "to be" in the present; possessives; "у мене болить …" |
| A2 | dative; prepositions with dative and accusative; Perfekt; imperative (Sie form); separable verbs; *weil*, *dass*, *wenn*; comparison | all seven cases, including the vocative (пане, пані); past tense with gender agreement; future tense; imperative (ви form: сідайте); треба, можна, не можна; first verbs of motion (йти / їхати); first aspect pairs |
| B1 | Präteritum of common verbs; passive (*Die Probe wird abgenommen*); Konjunktiv II for advice and politeness (*würde*, *könnte*, *sollte*); relative clauses; *um … zu*, *damit*, *obwohl*; *bevor*, *nachdem*, *während*; adjective endings | aspect in all tenses; prefixed verbs of motion; conditional with би; clauses with тому що, щоб, якщо, коли; numerals with nouns in all cases; impersonal constructions and short forms on signs (зачинено) |
| B2 | passive with modal verbs; Konjunktiv I for reported speech; nominal style (*nach Abschluss der Therapie*); participle attributes (*die isolierten Patienten*); two-part connectors (*je … desto*, *sowohl … als auch*); *werden* for assumptions | active and passive participles; adverbial participles (дієприслівники); impersonal passive in -но/-то (зроблено); reported speech; complex connectors (незважаючи на те що, у зв'язку з тим що); formal and official register |
