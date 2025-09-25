from django.contrib import admin

from .models import FlowStatus, FlowType, FlowCategory, FlowSubcategory, Transaction
from rangefilter.filters import DateRangeFilter

@admin.register(FlowStatus)
class FlowStatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(FlowType)
class FlowTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(FlowCategory)
class FlowCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(FlowSubcategory)
class FlowSubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "amount", "status", "type", "category", "subcategory", "comment")
    list_filter = (("created_at", DateRangeFilter), "status", "type", "category", "subcategory")
    search_fields = ("comment",)
    date_hierarchy = "created_at"
