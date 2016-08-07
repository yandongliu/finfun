import json
import sys

for l in sys.stdin:
    obj = json.loads(l.strip().split('\t')[1])
    print(len(obj))
    for o in obj:
        print(o['Date'])
