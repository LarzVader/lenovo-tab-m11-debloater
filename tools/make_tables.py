#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the app tables from packages.json into README.md and README.de.md.

Run this after every change to packages.json:  python3 tools/make_tables.py
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READMES = (("en", "README.md"), ("de", "README.de.md"))
WORDS = {
    "en": {"app": "App", "what": "What it is", "effect": "If removed",
           "pre": "Preselected", "tested": "Tested", "yes": "yes", "no": "–"},
    "de": {"app": "App", "what": "Was es ist", "effect": "Wenn entfernt",
           "pre": "Vorausgewählt", "tested": "Getestet", "yes": "ja", "no": "–"},
}
MARKERS = re.compile(r"(<!-- PACKAGES:START -->\n).*?(<!-- PACKAGES:END -->)", re.S)


def cell(text):
    return text.replace("|", "\\|")


def tables(catalog, lang):
    words = WORDS[lang]
    lines = []
    for category in catalog["categories"]:
        lines += ["### " + category["name"][lang], "", category["note"][lang], ""]
        lines.append("| %s | %s | %s | %s | %s |" % (
            words["app"], words["what"], words["effect"], words["pre"], words["tested"]))
        lines.append("|---|---|---|:-:|:-:|")
        for item in category["items"]:
            app = "**%s**<br>%s<br>id: `%s`" % (
                cell(item["name"][lang]),
                "<br>".join("`%s`" % p for p in item["packages"]),
                item["id"])
            lines.append("| %s | %s | %s | %s | %s |" % (
                app, cell(item["what"][lang]), cell(item["effect"][lang]),
                words["yes"] if item.get("recommended") else words["no"],
                words["yes"] if item.get("tested") else words["no"]))
        lines.append("")
    return "\n".join(lines)


def main():
    with open(os.path.join(ROOT, "packages.json"), encoding="utf-8") as handle:
        catalog = json.load(handle)
    for lang, name in READMES:
        path = os.path.join(ROOT, name)
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        if not MARKERS.search(text):
            raise SystemExit("%s: markers not found" % name)
        new = MARKERS.sub(lambda m: m.group(1) + "\n" + tables(catalog, lang) + "\n" + m.group(2),
                          text)
        if new != text:
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(new)
            print("updated " + name)
        else:
            print("unchanged " + name)


if __name__ == "__main__":
    main()
