# break_the_hash.py — AI 230 · Project 2 · Break the Hash Table
# One tiny coat check, two ticket systems: a good one and a terrible one.
# Mission: find FIVE real words that all pile onto the SAME hook under
# the bad hash. Put them in YOUR_FIVE below and run me again.

import time

BUCKETS = 256   # a fixed little coat check: 256 hooks, numbered 0-255

def bad_hash(word):
    # "Add up the letters" from Notes 06: a=1, b=2, ... z=26, then sum.
    # Same word always gives the same number — job 1, done perfectly.
    # But adding doesn't care about ORDER. Remember that.
    return sum(ord(c) - 96 for c in word.lower() if c.isalpha())

def good_hash(word):
    # Python's built-in scrambler — the professionals' ticket system.
    return hash(word)

class TinyTable:
    # chaining, exactly like Notes 06 Section 4: one small rack per hook
    def __init__(self, hash_fn):
        self.hash_fn = hash_fn
        self.racks = [[] for _ in range(BUCKETS)]

    def bucket_of(self, word):
        return self.hash_fn(word) % BUCKETS   # wrap onto a hook number

    def add(self, word):
        rack = self.racks[self.bucket_of(word)]
        if word not in rack:
            rack.append(word)

    def has(self, word):   # the lookup we time below
        return word in self.racks[self.bucket_of(word)]

    def longest_rack(self):
        return max(len(r) for r in self.racks)

def where(word):
    # your hunting tool: which hook does the BAD hash pick?
    print(f"  bad hash sends {word!r} to bucket {bad_hash(word) % BUCKETS}")

# ======================================================================
# YOUR FIVE VILLAIN WORDS GO HERE — five DIFFERENT real words that all
# land in the SAME bucket under the bad hash. Hunt interactively with:
#     python -i break_the_hash.py      then      where("yourword")
YOUR_FIVE = ["hot", "cater", "saw", "trace", "was"]
# ======================================================================

WORDS = """
time year people day man thing woman life child world school state family
student group country problem hand part place week company system program
question work night point home water room mother area money story month
study book job word business side kind head house service friend father
power hour game line member law car city name team minute idea body parent
face level office door health person art history party result change
morning reason girl moment teacher force education policy music market
sense nation plan college interest effect class control care field role
rate heart leader light voice police mind price report flower spoon window
garden winter summer bridge castle ocean paper town road wind peace trade
star bird song iron rain snow stone tree cake corn farm gate lake pond
rope sand wool clay moss pine reed silk empty fresh grand heavy plain
round sharp bake call fall grow hunt jump
""".split()

if __name__ == "__main__":
    bad, good = TinyTable(bad_hash), TinyTable(good_hash)
    everything = WORDS + [w for w in YOUR_FIVE if w not in WORDS]
    for w in everything:
        bad.add(w)
        good.add(w)

    def clock(table):   # time 800 lookups of every single word
        start = time.perf_counter()
        for _ in range(800):
            for w in everything:
                table.has(w)
        return time.perf_counter() - start

    print(f"stored {len(everything)} words in two {BUCKETS}-bucket tables\n")
    for name, t in (("BAD  hash (add the letters)", bad),
                    ("GOOD hash (python built-in)", good)):
        print(f"  {name}:  longest rack {t.longest_rack():3d}"
              f"   {len(everything)*800:,} lookups in {clock(t):6.3f} s")

    if len(set(YOUR_FIVE)) == 5:
        spots = sorted({bad_hash(w) % BUCKETS for w in YOUR_FIVE})
        if len(spots) == 1:
            print(f"\n  VILLAIN CHECK PASSED: {', '.join(YOUR_FIVE)}")
            print(f"  all five crammed onto hook {spots[0]} -- its rack "
                  f"now holds {len(bad.racks[spots[0]])} words")
        else:
            print(f"\n  not yet: your words spread over buckets {spots} -- "
                  f"they must all share ONE bucket")
    else:
        print("\n  no villain words yet -- put five different words in YOUR_FIVE.")
        print("  hunt with:  python -i break_the_hash.py   then   where(\"word\")")
        print("  a free clue:")
        where("cat")
        where("act")
