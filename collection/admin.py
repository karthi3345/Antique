from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Artifact, ProvenanceEntry, InspectionPoint, Chronicle, Enquiry, Document


class ProvenanceInline(TabularInline):
    model = ProvenanceEntry
    extra = 1


class InspectionInline(TabularInline):
    model = InspectionPoint
    extra = 1


class DocumentInline(TabularInline):
    model = Document
    extra = 1


@admin.register(Artifact)
class ArtifactAdmin(ModelAdmin):
    list_display = ("object_number", "name", "period", "region", "category", "status", "featured")
    list_filter = ("category", "region", "status", "featured")
    search_fields = ("name", "maker", "story")
    inlines = [ProvenanceInline, InspectionInline, DocumentInline]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Chronicle)
class ChronicleAdmin(ModelAdmin):
    pass

@admin.register(Enquiry)
class EnquiryAdmin(ModelAdmin):
    pass

from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
