"""Views for the collection: home, catalogue, artifact detail, JSON APIs."""
import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .models import Artifact, Enquiry


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

def home(request):
    featured = Artifact.objects.filter(featured=True, status="available").first()
    recent = (
        Artifact.objects.exclude(status="archive")
        .order_by("-created_at", "-object_number")[:3]
    )
    carousel_ids = list(
        Artifact.objects.exclude(status="archive")
        .filter(featured=True)
        .values_list("object_number", flat=True)
    )
    top_ids = list(
        Artifact.objects.exclude(status="archive")
        .order_by("-object_number")
        .values_list("object_number", flat=True)[:5]
    )
    seen = set()
    ordered_ids = []
    for n in carousel_ids + top_ids:
        if n not in seen:
            seen.add(n)
            ordered_ids.append(n)
    by_id = {a.object_number: a for a in Artifact.objects.filter(object_number__in=ordered_ids[:5])}
    carousel = [by_id[n] for n in ordered_ids[:5] if n in by_id]

    categories = _category_tiles()

    testimonials = [
        {"name": "Isabelle Laurent", "place": "Paris",
         "text": "Une découverte remarquable — chaque pièce est choisie avec un soin rare. La maison a retrouvé pour nous un Bronze XVIIIᵉ qui complète parfaitement notre collection."},
        {"name": "Charles de Vigny", "place": "Lyon",
         "text": "Provenance documentée, livraison soignée, discrétion totale. On traite ici avec des gens qui connaissent leur métier."},
        {"name": "Amélie Rousseau", "place": "Bordeaux",
         "text": "Les Chroniques de la maison valent à elles seules la visite — et les objets sont encore plus beaux en vrai."},
    ]

    return render(request, "collection/home.html", {
        "hero": featured,
        "featured": featured,
        "recent": recent,
        "carousel": carousel,
        "categories": categories,
        "testimonials": testimonials,
        "object_count": Artifact.objects.exclude(status="archive").count(),
    })


def _category_tiles():
    """One premium card per category: first object's hero photo, server-rendered."""
    tiles = []
    for a in (
        Artifact.objects.exclude(status="archive")
        .order_by("object_number")
        .only("object_number", "category", "hero_frame")
    ):
        if any(t["cat"] == a.category for t in tiles):
            continue
        tiles.append({
            "cat": a.category,
            "count": 0,
            "hero": f"/static/img/objects/{a.object_number:03d}/{a.hero_frame:02d}.webp",
        })
    counts = dict(
        Artifact.objects.exclude(status="archive")
        .values_list("category")
        .annotate(n=models_count())
        .values_list("category", "n")
    )
    for t in tiles:
        t["count"] = counts.get(t["cat"], 0)
    return tiles


def collection_view(request):
    return render(request, "collection/catalogue.html")


def artifact_detail(request, number):
    artifact = get_object_or_404(Artifact, object_number=number)
    related = list(
        Artifact.objects.filter(category=artifact.category)
        .exclude(pk=artifact.pk)
        .exclude(status="archive")
        .order_by("object_number")[:3]
    )
    return render(request, "collection/artifact.html", {
        "artifact": artifact,
        "related": related,
    })


# --------------------------------------------------------------------------
# JSON APIs (vanilla JS frontend consumes these)
# --------------------------------------------------------------------------

def _artifact_card(a):
    return {
        "number": a.object_number,
        "label": a.label_number,
        "name": a.name,
        "subtitle": a.subtitle,
        "period": a.period,
        "period_sort": a.period_sort,
        "region": a.region,
        "category": a.category,
        "material": a.material,
        "status": a.status,
        "status_line": a.status_line,
        "url": a.get_absolute_url(),
        "hero": f"/static/img/objects/{a.object_number:03d}/{a.hero_frame:02d}.webp",
        "accent": a.accent_hex,
        "frame_count": a.frame_count,
        "image_source": a.image_source,
        "image_license": a.image_license,
    }


def _artifact_full(a):
    data = _artifact_card(a)
    data.update({
        "slug": a.slug,
        "accession": a.accession_code,
        "maker": a.maker,
        "attribution": a.attribution,
        "story": a.story,
        "story_lede": a.story_lede,
        "condition": a.condition,
        "condition_grade": a.condition_grade,
        "dimensions": a.dimensions,
        "weight": a.weight,
        "image_source": a.image_source,
        "image_source_url": a.image_source_url,
        "image_license": a.image_license,
        "image_credit": a.image_credit,
        "provenance": [
            {
                "year": p.year,
                "event": p.event,
                "evidence": p.evidence,
                "undocumented": p.undocumented,
            }
            for p in a.provenance.all()
        ],
        "inspection": [
            {
                "label": ip.label,
                "detail": ip.detail,
                "kind": ip.kind,
                "frame": ip.frame_index,
                "x": ip.x,
                "y": ip.y,
            }
            for ip in a.inspection_points.all()
        ],
        "documentation": [
            {"title": d.title, "kind": d.kind, "note": d.note}
            for d in a.documents.all()
        ] if hasattr(a, "documents") else [],
    })
    return data


@require_GET
def api_objects(request):
    qs = Artifact.objects.exclude(status="archive")

    region = request.GET.get("region")
    category = request.GET.get("category")
    period_min = request.GET.get("period_min")
    period_max = request.GET.get("period_max")
    material = request.GET.get("material")
    q = request.GET.get("q")

    if region:
        qs = qs.filter(region=region)
    if category:
        qs = qs.filter(category=category)
    if material:
        qs = qs.filter(material__icontains=material)
    if period_min:
        qs = qs.filter(period_sort__gte=int(period_min))
    if period_max:
        qs = qs.filter(period_sort__lte=int(period_max))
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(region__icontains=q) | Q(maker__icontains=q) | Q(material__icontains=q))

    sort = request.GET.get("sort", "number")
    order_map = {
        "number": "object_number",
        "-number": "-object_number",
        "period": "period_sort",
        "-period": "-period_sort",
        "name": "name",
    }
    qs = qs.order_by(order_map.get(sort, "object_number"))

    facets = _facet_counts(qs)
    return JsonResponse({"objects": [_artifact_card(a) for a in qs], "facets": facets})


def _facet_counts(qs):
    def counts(field):
        out = {}
        for row in qs.values(field).annotate(n=models_count()):
            out[row[field]] = row["n"]
        return out

    return {
        "regions": counts("region"),
        "categories": counts("category"),
    }


def models_count():
    from django.db.models import Count
    return Count("id")


@require_GET
def api_artifact(request, number):
    artifact = get_object_or_404(Artifact, object_number=number)
    return JsonResponse(_artifact_full(artifact))


@require_POST
def api_enquiry(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "The request could not be read."}, status=400)

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    message = (payload.get("message") or "").strip()
    phone = (payload.get("phone") or "").strip()
    number = payload.get("object")

    errors = {}
    if not name:
        errors["name"] = "Your name is required."
    if not email or "@" not in email:
        errors["email"] = "A valid email address is required."
    if not message:
        errors["message"] = "A few words about your interest help us respond well."
    if errors:
        return JsonResponse({"error": "A detail appears to be missing below.", "fields": errors}, status=400)

    artifact = None
    if number:
        try:
            artifact = Artifact.objects.get(object_number=int(number))
        except (Artifact.DoesNotExist, ValueError, TypeError):
            artifact = None

    enquiry = Enquiry.objects.create(
        name=name, email=email, phone=phone, message=message, artifact=artifact,
    )
    return JsonResponse({
        "ok": True,
        "number": "V.{}.{}".format(timezone.now().year, str(enquiry.id).zfill(3)),
        "reply": "Thank you. A member of the house will respond within one working day.",
    })
