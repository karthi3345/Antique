"""Volgo collection models — Artifact, Provenance, Inspection, Chronicle, Enquiry, Document."""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Artifact(models.Model):
    """A single catalogued object — the hero of the entire house."""

    STATUS_CHOICES = [
        ("available", "Available for acquisition"),
        ("reserved", "Under consideration"),
        ("acquired", "In a private collection"),
        ("archive", "Archived"),
    ]
    GRADE_CHOICES = [
        ("Excellent", "Excellent"),
        ("Very Good", "Very Good"),
        ("Good", "Good"),
        ("Fair", "Fair"),
    ]

    object_number = models.PositiveIntegerField(
        unique=True, help_text="Sequential public number; never reused."
    )
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    name = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=240, blank=True, help_text="One-line curatorial subtitle.")
    period = models.CharField(max_length=120, help_text="e.g. c. 1880 or dated 1887")
    period_sort = models.IntegerField(help_text="Numeric year for filtering/sorting.")
    region = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    material = models.CharField(max_length=240, help_text="Middot-separated, hierarchical.")
    maker = models.CharField(max_length=200, blank=True, help_text="Attributed maker/workshop, if documented.")
    attribution = models.CharField(max_length=240, blank=True, help_text="Cataloguing term: attributed to / circle of / manner of.")
    story = models.TextField(help_text="The historical narrative.")
    story_lede = models.TextField(blank=True, help_text="Opening paragraph, displayed larger.")
    condition = models.TextField(blank=True)
    condition_grade = models.CharField(max_length=40, choices=GRADE_CHOICES, blank=True)
    dimensions = models.CharField(max_length=200, blank=True)
    weight = models.CharField(max_length=100, blank=True)
    frame_count = models.PositiveIntegerField(default=1, help_text="Photograph frames available (1 for still photography).")
    hero_frame = models.PositiveIntegerField(default=0)
    # --- Reference-image rights / attribution (museum open-access imagery) ---
    image_source = models.CharField(
        max_length=200, blank=True,
        help_text="Holding institution of the reference photograph.")
    image_source_url = models.URLField(max_length=400, blank=True)
    image_license = models.CharField(max_length=120, blank=True, help_text="e.g. Open Access CC0.")
    image_credit = models.CharField(max_length=300, blank=True, help_text="Credit line required by source.")
    rights_verified = models.BooleanField(default=False, help_text="License checked for this image.")
    accent_hex = models.CharField(max_length=7, default="#6F5B45", help_text="Object-derived accent for cards.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["object_number"]

    def __str__(self):
        return f"No. {self.object_number:03d} — {self.name}"

    @property
    def label_number(self):
        """Public label form: OBJECT No. 024"""
        return f"OBJECT No. {self.object_number:03d}"

    @property
    def accession_code(self):
        """Archival accession code: V.2026.024"""
        return f"V.2026.{self.object_number:03d}"

    @property
    def status_line(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    def get_absolute_url(self):
        return reverse("artifact_detail", args=[self.object_number])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:110] or "object"
            slug = base
            n = 2
            while Artifact.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProvenanceEntry(models.Model):
    """One event in an object's chain of custody, ordered by year."""

    artifact = models.ForeignKey(
        Artifact, on_delete=models.CASCADE, related_name="provenance"
    )
    year = models.CharField(
        max_length=40, help_text="As documented: 1887, c. 1890, 1924."
    )
    year_sort = models.IntegerField(help_text="Numeric sort year.")
    event = models.TextField(help_text="What happened, in one or two precise sentences.")
    evidence = models.CharField(
        max_length=300, blank=True, help_text="Citation for the claim, if any."
    )
    undocumented = models.BooleanField(
        default=False, help_text="Mark a gap in the record honestly."
    )

    class Meta:
        ordering = ["year_sort", "id"]

    def __str__(self):
        return f"{self.year} — {self.event[:60]}"


class InspectionPoint(models.Model):
    """A hotspot on the turntable viewer: maker mark, engraving, patina, restoration."""

    KIND_CHOICES = [
        ("mark", "Maker's mark"),
        ("engraving", "Engraving / signature"),
        ("patina", "Patina / surface"),
        ("damage", "Damage / wear"),
        ("restoration", "Restoration"),
        ("craft", "Craftsmanship detail"),
    ]

    artifact = models.ForeignKey(
        Artifact, on_delete=models.CASCADE, related_name="inspection_points"
    )
    label = models.CharField(max_length=120)
    detail = models.TextField(blank=True)
    frame_index = models.PositiveIntegerField(default=0)
    x = models.FloatField(help_text="0..1 horizontal position within the frame.")
    y = models.FloatField(help_text="0..1 vertical position within the frame.")
    kind = models.CharField(max_length=40, choices=KIND_CHOICES, default="mark")

    class Meta:
        ordering = ["frame_index", "id"]

    def __str__(self):
        return f"{self.artifact.label_number} f{self.frame_index} — {self.label}"


class Chronicle(models.Model):
    """Editorial article — the parchment reading room."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    standfirst = models.TextField(blank=True)
    body = models.TextField(help_text="Markdown-lite: blank-line paragraphs, ## headings, > quotes, - lists.")
    published_at = models.DateField()
    reading_minutes = models.PositiveIntegerField(default=6)
    object_ref = models.ForeignKey(
        Artifact, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="chronicles",
    )

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class Enquiry(models.Model):
    """A private-acquisition enquiry — begins the assisted journey."""

    STAGE_CHOICES = [
        ("enquire", "Enquiry received"),
        ("discuss", "In discussion"),
        ("acquired", "Acquired"),
        ("closed", "Closed"),
    ]
    artifact = models.ForeignKey(
        Artifact, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="enquiries",
    )
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=60, blank=True)
    message = models.TextField()
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default="enquire")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} — {self.artifact.label_number if self.artifact else 'the house'}"


class Document(models.Model):
    """Documentation attached to an artifact — certificates, records, papers."""

    KIND_CHOICES = [
        ("certificate", "Certificate of Authenticity"),
        ("provenance", "Provenance document"),
        ("condition", "Condition report"),
        ("invoice", "Historic invoice / record"),
        ("letter", "Correspondence"),
        ("other", "Supporting record"),
    ]

    artifact = models.ForeignKey(
        Artifact, on_delete=models.CASCADE, related_name="documents"
    )
    title = models.CharField(max_length=200)
    kind = models.CharField(max_length=40, choices=KIND_CHOICES, default="other")
    note = models.CharField(max_length=300, blank=True, help_text="One-line archival note.")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.artifact.label_number} — {self.title}"
