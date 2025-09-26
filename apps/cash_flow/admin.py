from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import FlowStatus, FlowType, FlowCategory, FlowSubcategory, Transaction
from rangefilter.filters import DateRangeFilter

class UniqueCategoryListFilter(admin.SimpleListFilter):
    
    title = "Категория"
    parameter_name = "category_name"

    def lookups(self, request, model_admin):
        categories = FlowCategory.objects.values_list("name", flat=True).distinct()
        return [(name, name) for name in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__name=self.value())
        return queryset
    
class UniqueSubcategoryListFilter(admin.SimpleListFilter):
    
    title = "Подкатегория"
    parameter_name = "subcategory_name"

    def lookups(self, request, model_admin):
        subcategories = FlowSubcategory.objects.values_list("name", flat=True).distinct()
        return [(name, name) for name in subcategories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subcategory__name=self.value())
        return queryset

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
    list_filter = ("name", "type",)
    search_fields = ("name",)


@admin.register(FlowSubcategory)
class FlowSubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("name", UniqueCategoryListFilter)
    search_fields = ("name",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = ("created_at", "amount", "status", "type", "category", "subcategory", "comment")
    list_filter = (("created_at", DateRangeFilter), "status", "type", UniqueCategoryListFilter, UniqueSubcategoryListFilter)
    search_fields = ("comment",)
    date_hierarchy = "created_at"
