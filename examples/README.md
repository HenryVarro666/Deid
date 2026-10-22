# Worked example (synthetic)

**Everything in this folder is synthetic.** The note, its names, dates, places and numbers were invented for this repository; it is not an n2c2 note and contains no real patient data. It uses the 2014 i2b2/UTHealth XML format, so the scripts read it the same way they read the real test set.

## The note

[`notes/synthetic-001.xml`](notes/synthetic-001.xml): a short clinic note with ten gold PHI tags in the n2c2 layout (`TEXT` plus `TAGS` with character offsets):

| Tag | TYPE | Text |
|---|---|---|
| DATE | DATE | 2091-03-14 |
| LOCATION | HOSPITAL | NORTH HARBOR MEDICAL CENTER |
| NAME | PATIENT | Delia Moreno |
| ID | MEDICALRECORD | 4471-882 |
| AGE | AGE | 58 |
| NAME | PATIENT | Moreno |
| PROFESSION | PROFESSION | school librarian |
| DATE | DATE | 01/09/2091 |
| CONTACT | PHONE | (555) 013-2847 |
| NAME | DOCTOR | Owen Prasad |

## Input and expected output for each prompt

| Prompt | Input sent to the model | Expected output |
|---|---|---|
| **Explicit**: lists every PHI type and asks for `[redacted]` (`Explicit2.py`) | [`inputs/explicit.txt`](inputs/explicit.txt) | [`expected/explicit/`](expected/explicit/synthetic-001_anonymized.txt): every PHI string replaced by `[redacted]`, all other text unchanged |
| **Implicit**: "Please anonymize the following text" (`Implicit2.py`) | [`inputs/implicit.txt`](inputs/implicit.txt) | [`expected/implicit/`](expected/implicit/synthetic-001_anonymized.txt): the prompt names no format, so a good answer may use typed placeholders such as `[PATIENT]` or `[DATE]` |
| **General**: one question per PHI type, then each answer is replaced in the note (`General2.py`) | [`inputs/general.txt`](inputs/general.txt) (eight questions) | [`expected/general/answers.md`](expected/general/answers.md) for the answers, and [`expected/general/`](expected/general/synthetic-001_anonymized.txt) for the note after replacement |

The expected outputs are written by hand to show what a correct result looks like; they are not model outputs.

## Scoring it

```bash
python3 examples/score_example.py
```

```
10 PHI mentions in the synthetic note

 0.600  note returned unchanged   leaked: 2091-03-14, 4471-882, 58, Moreno
 0.600  prompt + note echoed (what a decoder-only run saves)   leaked: 2091-03-14, 4471-882, 58, Moreno
 1.000  explicit, expected output
 1.000  implicit, expected output
 1.000  general, expected output
```

The first two lines show why the score has a floor. Only single-word PHI can match a whole word in the output, and `01/09/2091.` keeps its full stop, so the untouched note already scores 0.600. A file that echoes the prompt contains the whole note and scores exactly the same, which is what the 2023 LLaMA and Falcon runs saved (see the main [README](../README.md#findings)).

## Running a model on it

Set `input_directory = './examples/notes'` in any generator (for example `Explicit2.py`) and run it. Then point `Accuracy.py` at `original_directory = './examples/notes'` and the new output folder.
