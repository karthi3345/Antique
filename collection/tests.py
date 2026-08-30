from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
import json

from .models import Artifact, ProvenanceEntry, InspectionPoint, Chronicle, Enquiry


class ArtifactModelTest(TestCase):
    def test_label_number_is_zero_padded(self):
        a = Artifact.objects.create(
            object_number=24, name="Victorian Writing Desk", period="c. 1880",
            period_sort=1880, region="England", category="Furniture", material="Walnut · Brass",
            story="x", frame_count=36,
        )
        self.assertEqual(a.label_number, "OBJECT No. 024")

    def test_accession_code_format(self):
        a = Artifact.objects.create(
            object_number=7, name="Bronze Head", period="c. 1200",
            period_sort=1200, region="Nigeria", category="Sculpture", material="Bronze",
            story="x",
        )
        year = timezone.now().year
        self.assertEqual(a.accession_code, f"V.{year}.007")

    def test_slug_auto_generated_and_stable(self):
        a = Artifact.objects.create(
            object_number=1, name="Ming Porcelain Bowl", period="c. 1600",
            period_sort=1600, region="China", category="Ceramics", material="Porcelain",
            story="x",
        )
        self.assertEqual(a.slug, "ming-porcelain-bowl")
        a.name = "Renamed Later"
        a.save()
        self.assertEqual(a.slug, "ming-porcelain-bowl")  # slug survives rename

    def test_get_absolute_url_uses_number(self):
        a = Artifact.objects.create(
            object_number=5, name="Test Object", period="c. 1900",
            period_sort=1900, region="France", category="Metalwork", material="Silver",
            story="x",
        )
        self.assertEqual(a.get_absolute_url(), "/objects/5/")

    def test_object_number_unique(self):
        Artifact.objects.create(
            object_number=2, name="A", period="c. 1900", period_sort=1900,
            region="X", category="Y", material="Z", story="s",
        )
        with self.assertRaises(Exception):
            Artifact.objects.create(
                object_number=2, name="B", period="c. 1900", period_sort=1900,
                region="X", category="Y", material="Z", story="s",
            )


class ProvenanceOrderingTest(TestCase):
    def test_entries_order_by_year(self):
        a = Artifact.objects.create(
            object_number=3, name="Obj", period="c. 1800", period_sort=1800,
            region="R", category="C", material="M", story="s",
        )
        ProvenanceEntry.objects.create(artifact=a, year="1887", year_sort=1887, event="Made.")
        ProvenanceEntry.objects.create(artifact=a, year="1924", year_sort=1924, event="Sold.")
        ProvenanceEntry.objects.create(artifact=a, year="c. 1890", year_sort=1890, event="Acquired.")
        ordered = [e.year for e in a.provenance.all()]
        self.assertEqual(ordered, ["1887", "c. 1890", "1924"])


class EnquiryModelTest(TestCase):
    def test_str_includes_object(self):
        a = Artifact.objects.create(
            object_number=41, name="Astrolabe", period="c. 1720", period_sort=1720,
            region="Persia", category="Scientific", material="Brass", story="s",
        )
        e = Enquiry(name="Collector", email="c@example.com", message="Interested.", artifact=a)
        self.assertIn("OBJECT No. 041", str(e))


class ChronicleModelTest(TestCase):
    def test_default_ordering_latest_first(self):
        from datetime import date
        Chronicle.objects.create(title="Older", slug="older", body="x", published_at=date(2026, 1, 1))
        Chronicle.objects.create(title="Newer", slug="newer", body="x", published_at=date(2026, 6, 1))
        titles = [c.title for c in Chronicle.objects.all()]
        self.assertEqual(titles, ["Newer", "Older"])


class CommerceRemovedTest(TestCase):
    """The site is a catalog, not a store: no prices, no orders, no checkout."""

    def _make(self, number=50):
        return Artifact.objects.create(
            object_number=number, name=f"Test Object {number}", period="c. 1800",
            period_sort=1800, region="France", category="Metalwork", material="Brass",
            story="x", status="available",
        )

    def test_api_card_has_no_price_or_discount(self):
        self._make()
        r = self.client.get("/api/objects/")
        self.assertEqual(r.status_code, 200)
        obj = r.json()["objects"][0]
        self.assertNotIn("price", obj)
        self.assertNotIn("compare_price", obj)
        self.assertNotIn("discount", obj)
        self.assertNotIn("bestseller", obj)

    def test_api_detail_has_no_price(self):
        self._make(number=53)
        r = self.client.get("/api/objects/53/")
        self.assertEqual(r.status_code, 200)
        self.assertNotIn("price", r.json())

    def test_api_price_sort_rejected(self):
        self._make()
        r = self.client.get("/api/objects/?sort=-price")
        self.assertEqual(r.status_code, 200)  # falls back to number sort
        self.assertEqual(len(r.json()["objects"]), 1)

    def test_order_api_gone(self):
        r = self.client.post("/api/order/", json.dumps({"objects": [1]}), content_type="application/json")
        self.assertEqual(r.status_code, 404)

    def test_checkout_page_gone(self):
        r = self.client.get("/checkout/")
        self.assertEqual(r.status_code, 404)

    def test_home_page_renders_without_price_markup(self):
        self._make(number=10)
        self._make(number=11)
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertNotIn("add-to-cart", html)
        self.assertNotIn("% OFF", html)
        self.assertNotIn("Best Seller", html)
        self.assertNotIn("₹", html)

    def test_artifact_page_renders_without_price_markup(self):
        self._make(number=12)
        r = self.client.get("/objects/12/")
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertNotIn("add-to-cart", html)
        self.assertNotIn("₹", html)

    def test_enquiry_still_works(self):
        self._make(number=13)
        payload = {"name": "Collector", "email": "c@example.com",
                   "message": "Interested.", "object": 13}
        r = self.client.post("/api/enquiry/", json.dumps(payload), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["ok"])
        self.assertEqual(Enquiry.objects.count(), 1)


class CollectionCarouselTest(TestCase):
    """Home page shows one premium category carousel; old explore sections are gone."""

    def _make(self, number, category, name=None):
        return Artifact.objects.create(
            object_number=number, name=name or f"Object {number}", period="c. 1800",
            period_sort=1800, region="France", category=category,
            material="Brass · Glass", story="x", status="available",
        )

    def test_home_renders_carousel_with_category_cards(self):
        self._make(1, "Sculpture")
        self._make(2, "Furniture")
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertIn('id="collection-carousel"', html)
        self.assertIn("carousel-track", html)
        self.assertIn("carousel-arrow", html)
        self.assertIn("carousel-dots", html)
        self.assertIn("/collection/?category=Sculpture", html)
        self.assertIn("/collection/?category=Furniture", html)
        self.assertIn(">Sculpture<", html)
        self.assertIn(">Furniture<", html)

    def test_carousel_card_image_is_server_rendered_hero(self):
        self._make(7, "Glass")
        r = self.client.get("/")
        html = r.content.decode()
        self.assertIn("/static/img/objects/007/00.webp", html)
        self.assertNotIn("data-cat-img", html)  # no client-side fetch pop-in

    def test_old_explore_sections_removed(self):
        self._make(3, "Ceramics")
        r = self.client.get("/")
        html = r.content.decode()
        self.assertNotIn("grid-categories", html)
        self.assertNotIn("cat-tile", html)
        self.assertNotIn("grid-materials", html)
        self.assertNotIn("mat-chip", html)
        self.assertNotIn("Explore by Category", html)
        self.assertNotIn("Explore by Material", html)

    def test_carousel_orders_by_first_object_number(self):
        self._make(20, "Metalwork")
        self._make(5, "Ceramics")
        r = self.client.get("/")
        html = r.content.decode()
        self.assertLess(html.index("/collection/?category=Ceramics"),
                        html.index("/collection/?category=Metalwork"))

    def test_archived_objects_do_not_appear(self):
        a = self._make(30, "Textiles")
        a.status = "archive"
        a.save()
        self._make(31, "Woodwork")
        r = self.client.get("/")
        html = r.content.decode()
        self.assertNotIn("/collection/?category=Textiles", html)
        self.assertIn("/collection/?category=Woodwork", html)


class StaticExamineTest(TestCase):
    """Examine section shows one still photograph — no turntable, no rotation."""

    def _make(self, number=60):
        a = Artifact.objects.create(
            object_number=number, name="Lantern Pair", period="c. 1900",
            period_sort=1900, region="France", category="Metalwork",
            material="Tin · Glass", story="x", status="available",
        )
        InspectionPoint.objects.create(
            artifact=a, kind="patina", label="Rust patina", frame_index=4,
            x=50, y=50, detail="Honest surface rust; glass globes intact.",
        )
        return a

    def test_artifact_page_shows_static_photo(self):
        a = self._make()
        r = self.client.get(f"/objects/{a.object_number}/")
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertIn(f"/static/img/objects/{a.object_number:03d}/00.webp", html)
        self.assertIn("examine-photo", html)

    def test_artifact_page_has_no_turntable(self):
        a = self._make()
        r = self.client.get(f"/objects/{a.object_number}/")
        html = r.content.decode()
        self.assertNotIn("viewer-canvas", html)
        self.assertNotIn("viewer.js", html)
        self.assertNotIn("viewer.css", html)
        self.assertNotIn("Drag to rotate", html)
        self.assertNotIn("frame-indicator", html)
        self.assertNotIn("hotspot-layer", html)

    def test_inspection_notes_render_as_list(self):
        a = self._make()
        r = self.client.get(f"/objects/{a.object_number}/")
        html = r.content.decode()
        self.assertIn("Rust patina", html)
        self.assertIn("Honest surface rust; glass globes intact.", html)
        self.assertIn("inspect-list", html)



