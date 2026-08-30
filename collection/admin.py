from django.contrib import admin

from .models import Artifact, ProvenanceEntry, InspectionPoint, Chronicle, Enquiry, Document


class ProvenanceInline(admin.TabularInline):
    model = ProvenanceEntry
    extra = 1


class InspectionInline(admin.TabularInline):
    model = InspectionPoint
    extra = 1


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ("object_number", "name", "period", "region", "category", "status", "featured")
    list_filter = ("category", "region", "status", "featured")
    search_fields = ("name", "maker", "story")
    inlines = [ProvenanceInline, InspectionInline, DocumentInline]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Chronicle)
admin.site.register(Enquiry)
