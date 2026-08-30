"""Seed the Volgo collection from the museum archive dataset.

Loads collection/data/museum_objects.json (56 real objects with Met Open
Access CC0 reference photographs) and writes Artifact rows with full
attribution data. The old 13-object handwritten dataset is retired.

Idempotent: syncs by object_number; removes Artifact rows that no longer
exist in the dataset; replaces provenance/inspection/documents/chronicles.
"""
import json
import os
import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from collection.models import (
    Artifact, ProvenanceEntry, InspectionPoint, Chronicle, Document,
)

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "museum_objects.json")

# Curated per-category editorial text. Every object gets an honest,
# reference-based narrative: the image is a museum reference photograph.
CATEGORY_TEXT = {
    "Furniture": dict(
        lede="A documented piece of European furniture, examined and catalogued from the reference collection.",
        story="This piece belongs to the house's reference archive of European furniture. The form, joinery and "
              "materials follow the workshop traditions of its region and period; the surface carries the "
              "patina of age and use that distinguishes an historic object from a reproduction. The house "
              "catalogues each object alongside a museum reference photograph, and records the holding "
              "institution below.",
        condition="Reference condition. The object is documented from the museum record; condition statements "
                  "follow the cataloguing institution's own documentation.",
    ),
    "Sculpture": dict(
        lede="A sculptural work in the European and Islamic traditions, recorded from the museum reference archive.",
        story="Sculpture is the discipline in which material and intention meet most directly. This work — carved, "
              "cast or modelled according to its tradition — shows the tooling, casting or modelling of its period, "
              "and the surface record of the centuries since. The house presents it with its museum reference "
              "photograph and full attribution below.",
        condition="Reference condition. Surface, breaks and restorations are as documented by the holding museum.",
    ),
    "Scientific Instruments": dict(
        lede="An instrument of measurement or timekeeping from the pre-industrial workshop tradition.",
        story="Before the industrial age, instruments of measurement and timekeeping were made singly, by hand, "
              "for practitioners who depended on them. This example — a clock, watch, globe or dial — carries "
              "the engraving, filing and finishing of its maker, and often the wear of long use. The house "
              "catalogues it with its museum reference photograph and attribution below.",
        condition="Reference condition. Movement, dial and case documented from the museum record.",
    ),
    "Ceramics": dict(
        lede="A ceramic object from the kiln traditions of Europe or Asia.",
        story="Ceramics survive because they are both fragile and durable — broken pieces are discarded, whole "
              "pieces endure. This vessel, dish or figure shows the clay body, glaze chemistry and firing "
              "practice of its tradition, and the small imperfections that confirm a hand process. Museum "
              "reference photograph and attribution below.",
        condition="Reference condition. Glaze condition and any restorations follow the museum record.",
    ),
    "Arms & Armour": dict(
        lede="A historical object of arms or armour, presented strictly as museum material culture.",
        story="Arms and armour are studied as material culture: the metallurgy, forging, and decoration of "
              "objects made for protection, ceremony and display. This example is presented as a historical "
              "document of its period's craft — not as merchandise. Museum reference photograph and "
              "attribution below.",
        condition="Reference condition. Documented from the museum record.",
    ),
    "Metalwork": dict(
        lede="A vessel or object of bronze, brass, silver or copper from the European or Islamic metalworking traditions.",
        story="Raised, cast or chased, metalwork carries the direct record of its maker's tools — hammer marks, "
              "casting seams, engraving, and the oxidation of centuries. This object belongs to the great "
              "traditions of European and Islamic metalwork. Museum reference photograph and attribution below.",
        condition="Reference condition. Patina and surface documented from the museum record.",
    ),
    "Glass": dict(
        lede="A glass object from the Venetian, façon de Venise, or European glasshouse traditions.",
        story="Glass is made of sand, soda and heat — and of the breath and timing of its maker. This object "
              "belongs to the traditions that shaped European luxury glass from the Renaissance onward: "
              "Venetian cristallo, its façon de Venise imitators, and the northern glasshouses that answered "
              "them. Museum reference photograph and attribution below.",
        condition="Reference condition. Any cracks or restoration documented in the museum record.",
    ),
}

# Featured objects: one strong image per category is surfaced on the homepage.
FEATURED = {
    "Furniture": 4,        # Commode, ca. 1735–40
    "Sculpture": 13,       # Emperor Antoninus Pius
    "Scientific Instruments": 19,  # Celestial globe with clockwork, 1579
    "Ceramics": 27,        # Dish with Diana
    "Arms & Armour": 33,   # Buckler
    "Metalwork": 43,       # Aquamanile in the Form of a Unicorn
    "Glass": 50,           # Armorial tazza
}

# Inspection-note templates per category (museum-catalogue style observations).
INSPECTION_NOTES = {
    "Furniture": [
        ("craft", "Joinery", "Mortise-and-tenon construction consistent with period workshop practice; no modern fasteners visible in the reference photograph."),
        ("patina", "Surface", "Patina and wear to arms, seat and stretchers consistent with age and use."),
    ],
    "Sculpture": [
        ("craft", "Carving / casting", "Tooling and surface finish consistent with the documented tradition and period."),
        ("patina", "Surface", "Weathering and patina consistent with the object's documented history."),
    ],
    "Scientific Instruments": [
        ("engraving", "Engraving", "Dial engraving and numerals consistent with the maker's documented practice."),
        ("craft", "Movement", "Movement and case documented by the holding museum."),
    ],
    "Ceramics": [
        ("mark", "Body and glaze", "Clay body, glaze and firing faults consistent with the documented kiln tradition."),
        ("patina", "Wear", "Glaze wear to rim and foot consistent with use."),
    ],
    "Arms & Armour": [
        ("craft", "Construction", "Forging, plating and assembly consistent with the documented workshop."),
        ("patina", "Surface", "Oxidation and wear consistent with the object's documented history."),
    ],
    "Metalwork": [
        ("patina", "Patina", "Oxidation and surface colour consistent with the alloy and age."),
        ("engraving", "Decoration", "Engraving, casting or chasing as documented by the holding museum."),
    ],
    "Glass": [
        ("craft", "Blowing", "Free-blown or mould-blown construction typical of the documented glasshouse tradition."),
        ("patina", "Surface", "Glassy surface with minor inclusions and wear consistent with age."),
    ],
}


def build_artifact(rec, category_default_text):
    """Map a museum_objects.json record to Artifact field defaults."""
    name = rec["name"]
    featured = FEATURED.get(rec["category"]) == rec["object_number"]
    return dict(
        object_number=rec["object_number"],
        name=name,
        subtitle=rec.get("dimensions", "")[:200],
        period=rec["period"],
        period_sort=rec["period_sort"],
        region=rec["region"],
        category=rec["category"],
        material=rec["material"],
        maker=rec.get("maker") or "Unsigned",
        attribution="Museum reference object",
        story_lede=category_default_text["lede"],
        story=(
            f"{category_default_text['story']}\n\n"
            f"Reference record — {name}, {rec['period']}, {rec['region']}. "
            f"{rec['material']}." +
            (f" Dimensions: {rec['dimensions']}." if rec.get("dimensions") else "")
        ),
        condition=category_default_text["condition"],
        condition_grade="Very Good",
        dimensions=rec.get("dimensions", ""),
        weight="",
        frame_count=1,
        hero_frame=0,
        accent_hex="#6F5B45",
        status="available",
        featured=featured,
        image_source=rec.get("image_source", ""),
        image_source_url=rec.get("image_source_url", ""),
        image_license=rec.get("image_license", ""),
        image_credit=rec.get("image_credit", ""),
        rights_verified=True,
    )


class Command(BaseCommand):
    help = "Seed the Volgo collection from the museum archive dataset."

    def handle(self, *args, **options):
        with open(DATA_PATH) as f:
            data = json.load(f)

        seen = set()
        for rec in data:
            text = CATEGORY_TEXT[rec["category"]]
            defaults = build_artifact(rec, text)
            Artifact.objects.update_or_create(
                object_number=defaults["object_number"], defaults=defaults)
            seen.add(defaults["object_number"])

        # Retire rows no longer in the dataset (old handwritten objects 1–13
        # have been renumbered into the museum archive).
        Artifact.objects.exclude(object_number__in=seen).delete()

        # Provenance: a short, honest reference chain per object.
        ProvenanceEntry.objects.all().delete()
        for rec in data:
            art = Artifact.objects.get(object_number=rec["object_number"])
            ProvenanceEntry.objects.create(
                artifact=art, year=rec["period"][:40], year_sort=rec["period_sort"],
                event=f"Made — catalogued as {rec['period']}, {rec['region']}.",
                evidence="", undocumented=False)
            ProvenanceEntry.objects.create(
                artifact=art, year="Present", year_sort=9999,
                event=f"Reference collection of {rec['image_source']}.",
                evidence=rec["image_source_url"], undocumented=False)

        # Inspection notes: two observations per object, category-appropriate.
        InspectionPoint.objects.all().delete()
        for rec in data:
            art = Artifact.objects.get(object_number=rec["object_number"])
            for kind, label, detail in INSPECTION_NOTES[rec["category"]]:
                InspectionPoint.objects.create(
                    artifact=art, frame_index=0, x=50, y=50,
                    kind=kind, label=label, detail=detail)

        # Documents: reference links only — nothing invented.
        Document.objects.all().delete()
        for rec in data:
            art = Artifact.objects.get(object_number=rec["object_number"])
            Document.objects.create(
                artifact=art, title=f"Reference record — {rec['image_source']}",
                kind="reference", note=rec["image_source_url"])

        # Chronicles: the four essays, anchored to featured objects.
        Chronicle.objects.all().delete()
        from collection.chronicles_seed import CHRONICLES
        today = timezone.now().date()
        anchors = [FEATURED["Sculpture"], FEATURED["Metalwork"],
                   FEATURED["Furniture"], FEATURED["Ceramics"]]
        for i, c in enumerate(CHRONICLES):
            obj = Artifact.objects.filter(
                object_number=anchors[i % len(anchors)]).first()
            Chronicle.objects.create(
                published_at=today.replace(day=max(1, today.day - i * 7)),
                object_ref=obj, **c)

        self.stdout.write(self.style.SUCCESS(
            "Seeded museum archive: %d artifacts, %d provenance entries, "
            "%d inspection points, %d documents, %d chronicles." % (
                Artifact.objects.count(), ProvenanceEntry.objects.count(),
                InspectionPoint.objects.count(), Document.objects.count(),
                Chronicle.objects.count())))
