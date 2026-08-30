"""Tests for the real museum imagery archive (Met Open Access CC0).

Covers: seed produces 56 objects across 7 categories; every object has its
hero image on disk with CC0 license metadata; detail page renders the
reference credit; related objects share the category; the JSON API exposes
attribution fields; home renders a hero and 7 category tiles.
"""
import json
import os
import unittest

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from .models import Artifact

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "management", "commands", "..", "..", "data",
    "museum_objects.json")
IMG_ROOT = os.path.join(settings.BASE_DIR, "static", "img", "objects")

CATEGORIES = [
    "Furniture", "Sculpture", "Scientific Instruments", "Ceramics",
    "Arms & Armour", "Metalwork", "Glass",
]


def run_seed():
    from django.core.management import call_command
    call_command("seed_volgo", verbosity=0)


class SeedArchiveTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        run_seed()

    def test_56_objects_seeded(self):
        self.assertEqual(Artifact.objects.count(), 56)

    def test_eight_per_category(self):
        for cat in CATEGORIES:
            self.assertEqual(
                Artifact.objects.filter(category=cat).count(), 8,
                f"{cat} should hold 8 objects")

    def test_every_hero_image_on_disk(self):
        for a in Artifact.objects.all():
            path = os.path.join(
                IMG_ROOT, f"{a.object_number:03d}",
                f"{a.hero_frame:02d}.webp")
            self.assertTrue(
                os.path.exists(path),
                f"missing image for {a.label_number}: {path}")

    def test_every_object_has_license_and_source(self):
        for a in Artifact.objects.all():
            self.assertTrue(a.rights_verified, f"{a.label_number} not verified")
            self.assertEqual(a.image_license, "Open Access CC0")
            self.assertIn("metmuseum.org", a.image_source_url)

    def test_dataset_matches_seed(self):
        with open(DATA_PATH) as f:
            data = json.load(f)
        self.assertEqual(len(data), 56)
        self.assertEqual(
            sorted(r["object_number"] for r in data),
            sorted(a.object_number for a in Artifact.objects.all()))


class DetailCreditTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        run_seed()

    def test_detail_page_renders_credit(self):
        a = Artifact.objects.filter(image_source__contains="Met").first()
        url = reverse("artifact_detail", args=[a.object_number])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Reference photograph")
        self.assertContains(r, "Open Access CC0")
        self.assertContains(r, a.image_source_url)

    def test_related_objects_same_category(self):
        a = Artifact.objects.filter(category="Glass").first()
        r = self.client.get(a.get_absolute_url())
        self.assertEqual(r.status_code, 200)
        for other in Artifact.objects.filter(category="Glass").exclude(pk=a.pk)[:3]:
            self.assertContains(r, other.get_absolute_url())


class ApiAttributionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        run_seed()

    def test_api_card_has_license_fields(self):
        r = self.client.get("/api/objects/")
        self.assertEqual(r.status_code, 200)
        payload = r.json()
        self.assertEqual(len(payload["objects"]), 56)
        for obj in payload["objects"]:
            self.assertEqual(obj["image_license"], "Open Access CC0")
            self.assertIn("image_source", obj)

    def test_api_full_has_credit(self):
        a = Artifact.objects.first()
        r = self.client.get(f"/api/objects/{a.object_number}/")
        payload = r.json()
        self.assertTrue(payload["image_credit"])
        self.assertTrue(payload["image_source_url"])


class HomeArchiveTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        run_seed()

    def test_home_has_hero_and_seven_tiles(self):
        r = self.client.get(reverse("home"))
        self.assertEqual(r.status_code, 200)
        self.assertIn("hero", r.context)
        self.assertIsNotNone(r.context["hero"])
        self.assertEqual(len(r.context["categories"]), 7)
        for tile in r.context["categories"]:
            self.assertIn("/collection/?category=", r.content.decode())
        # hero image is preloaded (LCP)
        self.assertContains(r, 'rel="preload" as="image"')
