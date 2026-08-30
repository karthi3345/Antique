from django.test import TestCase

# Create your tests here.


class PostAnimationAssetsTest(TestCase):
    """Contact + acquisition pages ship the letter & post animation assets."""

    def test_contact_page_references_post_assets(self):
        r = self.client.get("/contact/")
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertIn("post.css", html)
        self.assertIn("post.js", html)

    def test_acquisition_page_references_post_assets(self):
        r = self.client.get("/acquisition/")
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertIn("post.css", html)
        self.assertIn("post.js", html)

    def test_post_assets_resolve_via_finders(self):
        from django.contrib.staticfiles import finders
        self.assertTrue(finders.find("css/post.css"))
        self.assertTrue(finders.find("js/post.js"))


class EnquiryNumberAPITest(TestCase):
    """The API returns a museum-style enquiry number for the receipt."""

    def test_number_pattern(self):
        import json
        payload = {"name": "Collector", "email": "c@example.com",
                   "message": "Interested in the astrolabe."}
        r = self.client.post("/api/enquiry/", json.dumps(payload), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertTrue(body["ok"])
        self.assertRegex(body["number"], r"^V\.\d{4}\.\d{3,}$")
