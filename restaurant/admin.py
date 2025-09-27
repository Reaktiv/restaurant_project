from django.contrib import admin
from .models import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_food', 'price', 'published', 'added_by', 'created_at')
    list_filter = ('published', 'type', 'created_at')
    search_fields = ('name_of_food', 'description', 'added_by__email')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if not change or not obj.added_by:  # yangi obyekt yoki qo‘lda kiritilmagan
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
