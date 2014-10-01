# Aggregator simulating default EMR aggregator for
# LongValueSum operator.

import operator

counts = {}
import sys
for line in sys.stdin:
    if len(line)<len("LongValueSum:"):
        continue
    l = line.strip()[len("LongValueSum:"):]
    parts = l.split("\t")
    if len(parts)<2:
        continue
    item = parts[0]
    try:
        count = int(parts[1])
    except Exception:
        continue
    counts[item] = counts.setdefault(item, 0) + count
pairs = []
for item,count in sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True):
    print item + "\t" + repr(count)