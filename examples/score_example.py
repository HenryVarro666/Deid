"""Score the synthetic example with the same rule as Accuracy.py, no n2c2 data needed.

    python3 examples/score_example.py

Rule (as in Accuracy.py): a gold PHI string counts as leaked when it appears as a whole
whitespace-separated word in the output; each distinct string counts once; the score is
1 - leaked / number of PHI mentions.
"""
import os
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
CATS = ("NAME", "PROFESSION", "LOCATION", "AGE", "DATE", "CONTACT", "ID")


def load(path):
    root = ET.parse(path).getroot()
    note = root.find("TEXT").text
    phi = [t.get("text") for t in root.find("TAGS") if t.tag in CATS]
    return note, phi


def score(output, phi):
    leaked = set(phi).intersection(output.split())
    return 1 - len(leaked) / len(phi), sorted(leaked)


def read(*parts):
    with open(os.path.join(HERE, *parts), encoding="utf-8") as f:
        return f.read()


note, phi = load(os.path.join(HERE, "notes", "synthetic-001.xml"))
cases = {
    "note returned unchanged": note,
    "prompt + note echoed (what a decoder-only run saves)": read("inputs", "explicit.txt"),
    "explicit, expected output": read("expected", "explicit", "synthetic-001_anonymized.txt"),
    "implicit, expected output": read("expected", "implicit", "synthetic-001_anonymized.txt"),
    "general, expected output": read("expected", "general", "synthetic-001_anonymized.txt"),
}
print(f"{len(phi)} PHI mentions in the synthetic note\n")
for name, text in cases.items():
    s, leaked = score(text, phi)
    print(f"{s:6.3f}  {name}" + (f"   leaked: {', '.join(leaked)}" if leaked else ""))
