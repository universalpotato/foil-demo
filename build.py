"""Build index.html from template.html, game.json and lists.json.

    python build.py
    FOIL_API=https://host python build.py  # API on another host
    FOIL_CONTACT=... python build.py       # adds a Contact section
"""
import json
import os
import re

game = json.load(open("game.json"))
# drop PayMana steps
game["frames"] = [f for f in game["frames"] if f["kind"] != "PayMana"]


def names(s: str) -> str:  # CARDNAME/NICKNAME -> card name
    def one(line: str) -> str:
        m = re.search(r"ability of (.+?)#\d+ \(", line)
        if m:
            line = line.replace("CARDNAME", m.group(1)).replace("NICKNAME", m.group(1).split(",")[0])
        return line

    return "\n".join(one(x) for x in s.split("\n"))


for f in game["frames"]:
    f["opts"] = [names(o) for o in f["opts"]]
    if "text" in f:
        f["text"] = names(f["text"])

embed = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
page = open("template.html").read()
for mark, value in (("/*GAME*/", embed(game)), ("/*LISTS*/", embed(json.load(open("lists.json"))))):
    assert page.count(mark) == 1
    page = page.replace(mark, value)
contact = os.environ.get("FOIL_CONTACT", "")
assert page.count("<!--CONTACT-->") == 1
page = page.replace("<!--CONTACT-->", f"<h2>Contact</h2>\n<p>{contact}</p>" if contact else "")
assert page.count('const API = "";') == 1
page = page.replace('const API = "";', "const API = " + json.dumps(os.environ.get("FOIL_API", "")) + ";")
head, rest = page.split("</style>", 1)
shell = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
         '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
         '<style>:root{color-scheme:light;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}'
         'body{margin:0;font:14px system-ui,-apple-system,"Segoe UI",sans-serif}img{max-width:100%}'
         '[hidden]{display:none!important}</style>\n')
open("index.html", "w").write(shell + head + "</style>\n</head>\n<body>\n" + rest + "\n</body>\n</html>\n")
print("index.html written")
