"""Chronicle essay content for the seeder, kept separate from logic.

Bodies are markdown. Essays are re-anchored to living objects at seed time
by category in seed_volgo.py.
"""

CHRONICLES = [
    dict(
        title="On Attribution",
        slug="on-attribution",
        standfirst="Attribution is a spectrum, and the house writes where on that spectrum the evidence places an object — no further.",
        body="## The honest spectrum\n"
             "Attribution is a spectrum, and the house writes where on that spectrum the evidence places an object — no further.\n\n"
             "- **Attributed to** — the evidence points to a hand, but not conclusively.\n"
             "- **Circle of** — made in the immediate orbit of a documented master.\n"
             "- **Manner of** — later work in the style of, without workshop connection.\n"
             "- **Unsigned** — the maker is simply not recoverable, and we say so.\n\n"
             "In this archive, each object's image is a museum reference photograph, and the holding "
             "institution is credited in full. The house claims ownership of the catalogue, not of the "
             "depicted objects — an honesty that is itself the tradition of the great museums.",
    ),
    dict(
        title="Reading Patina",
        slug="reading-patina",
        standfirst="Patina is not dirt, and it is not damage. It is the chemical record of an object's environment over decades or centuries.",
        body="## Surfaces that testify\n"
             "Patina is not dirt, and it is not damage. It is the chemical record of an object's environment over decades or centuries.\n\n"
             "Bronze that has lived in air develops a stable, dark brown surface; buried bronze may carry "
             "malachite or azurite in the recesses. Silver blackens; oak silvers; leather darkens at the "
             "points of contact with hands. None of this can be hurried convincingly.\n\n"
             "When you examine an object here, read the surface the way you would read a document — "
             "asking what it records, and whether the record is consistent throughout.",
    ),
    dict(
        title="Provenance, Honestly",
        slug="provenance-honestly",
        standfirst="A provenance is a chain of custody: maker to owner to owner to collector. Each link must be evidenced.",
        body="## The chain, and its gaps\n"
             "A provenance is a chain of custody: maker to owner to owner to collector. Each link must be evidenced — an invoice, an inventory, a catalogue entry, a photograph.\n\n"
             "Where a link is missing, the house records the gap rather than decorating it. An undocumented "
             "century is stated as an undocumented century. This is the discipline that separates a "
             "catalogue from a sales brochure.\n\n"
             "For every object in this archive, the ultimate documented holder is the credited museum whose "
             "reference photograph illustrates the record.",
    ),
    dict(
        title="Restoration vs Original",
        slug="restoration-vs-original",
        standfirst="A restoration is not a flaw to hide; it is an event in the object's life. The question is whether it was done well, and when.",
        body="## When a repair is history\n"
             "A restoration is not a flaw to hide; it is an event in the object's life. The question is whether it was done well, and when.\n\n"
             "The house records every known intervention with the same seriousness as the original "
             "commission: a nineteenth-century repair is itself a document of how the object was valued "
             "in the nineteenth century.\n\n"
             "Where the museum record documents restoration, the catalogue follows it exactly — and where "
             "the record is silent, the catalogue is silent too.",
    ),
]
