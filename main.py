# One Line, One Chill — @hayunkarimun
# Scores 6 candidate one-line horror sentences against the judge brief's
# 4 criteria, in the brief's own order (weights 5/4/3/2):
#  1. frightening (the first thing the judge weighs)
#  2. vivid (a concrete image the reader can see)
#  3. original (not one of the flooded angles: baby monitor, daughter's
#     drawing, ultrasound heartbeat, dog collar still warm, own voice,
#     doppelganger face, voicemail from my own number, photo of me asleep)
#  4. construction (one sentence, one breath, tight, under 200 chars)
# Writes the winner to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR).
# Gate: UTF-8, 1-200 chars, exactly one line, not only whitespace.
import os
import sys

WEIGHTS = [5, 4, 3, 2]

# (line, [frightening, vivid, original, construction], why)
CANDIDATES = [
    (
        "The dentist held up my pulled tooth and pointed inside it: my name, carved there in my own handwriting.",
        [5, 5, 5, 5],
        "Bodily horror with an impossible detail: the threat is inside the narrator's own body and signed in their own hand. Concrete, fresh, one breath.",
    ),
    (
        "I woke up with sand in my bed, and the nearest beach is four hundred miles away — but the tide was still coming in.",
        [4, 5, 5, 4],
        "Vivid and original, but the scare is slower: it dawns on the reader instead of hitting in one breath, and the em dash softens the landing.",
    ),
    (
        "The elevator stopped on my floor at 3 a.m. and opened on an empty car that smelled exactly like my bedroom.",
        [4, 4, 3, 5],
        "Tight and eerie, but elevators at 3 a.m. are a familiar horror setting and the smell detail does less work than the dentist's tooth.",
    ),
    (
        "I set the table for one, like always, and when I sat down, the chair across from me pulled itself out.",
        [4, 4, 4, 4],
        "A clean haunted-house beat, but the moving chair is a well-worn image and the fright stays at the surface.",
    ),
    (
        "My reflection finished brushing its teeth before I did, and it has been waiting for me to notice ever since.",
        [4, 4, 3, 4],
        "Mirror dread is a crowded shelf, and the line explains its own scare instead of letting the detail do it.",
    ),
    (
        "The answering machine played my own voice saying I would be home soon, and I have lived alone for eleven years.",
        [4, 4, 3, 5],
        "Tight construction, but the own-voice/own-number angle is already all over this bounty, so it loses on originality.",
    ),
    (
        "My grandmother's recipe card says to stir until she stops screaming, and her handwriting is on every card in the box.",
        [4, 5, 5, 4],
        "Vivid and original — a domestic object turned wrong — but the scare needs a second read to land, and the sentence carries one clause too many.",
    ),
]


def score(scores):
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def main():
    ranked = sorted(CANDIDATES, key=lambda c: score(c[1]), reverse=True)
    winner, wscores, why = ranked[0]
    # Rejected drafts, documented so the choice is auditable:
    #  - sand in the bed (63): vivid but slow; the scare dawns instead of hitting.
    #  - elevator at 3 a.m. (55): familiar setting, weaker detail.
    #  - chair pulling itself out (56): well-worn haunted-house image.
    #  - reflection finishing first (53): crowded mirror shelf, over-explains.
    #  - answering machine, own voice (55): own-voice angle is flooded here.
    #  - grandmother's recipe card (63, v2 addition): vivid and original, but
    #    the scare needs a second read and the sentence carries one clause
    #    too many; the tooth still wins on first-breath fright.
    if not (1 <= len(winner) <= 200):
        sys.exit(f"gate: winner is {len(winner)} chars, must be 1-200")
    if "\n" in winner or not winner.strip():
        sys.exit("gate: winner must be exactly one non-blank line")
    if winner.count(".") != 1 or not winner.endswith("."):
        sys.exit("gate: winner must be exactly one sentence")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner)
    print(f"winner ({len(winner)} chars, score {score(wscores)}): {winner}")
    print(f"why: {why}")
    for line, sc, _ in ranked[1:]:
        print(f"  {score(sc)}: {line}")


if __name__ == "__main__":
    main()
