#!/usr/bin/env python3
# coding: utf-8

# finds nodes not in use

import os
from glob import glob
import re
from collections import Counter

script_paths = [
    y for x in os.walk("scripts_src/") for y in glob(os.path.join(x[0], "*.ssl"))
]

for script_path in script_paths:
    script_nodes = []
    with open(script_path) as fscript:
        script_text = fscript.read()
        script_text = re.sub(r"procedure Node\w+?;", "", script_text)
        lines = re.sub(r"/\*.+?\*/", "", script_text, flags=re.DOTALL).split("\n")
        for line in lines:
            if line.lstrip().startswith("//"):
                continue
            script_nodes.extend(
                re.findall(
                    r"Node\w+",
                    line,
                )
            )
    counted_nodes = Counter(script_nodes)
    for node in list(counted_nodes):
        if counted_nodes[node] > 1:
            del counted_nodes[node]
    if (counted_nodes):
        print(script_path)
    for node in counted_nodes:
        print(node, ':', counted_nodes[node])
