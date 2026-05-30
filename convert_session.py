#!/usr/bin/env python3
# Converts undercut-f1 format to f1-dash simulator format.
# undercut-f1: subscribe.txt (full JSON object) + live.txt (one message per line)
# f1-dash:     single .jsonl where line 1 = {"I":"1","R":{...}} and rest = {"M":[{...}]}

import json
import sys

subscribe_path = sys.argv[1]
live_path      = sys.argv[2]

with open(subscribe_path) as f:
    subscribe = json.load(f)

print(json.dumps({"I": "1", "R": subscribe}))

with open(live_path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            print(json.dumps({"M": [msg]}))
        except json.JSONDecodeError:
            continue
