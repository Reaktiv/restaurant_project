from django.contrib import admin
from .models import Food, FoodImage

class FoodImageInline(admin.TabularInline):
    model = FoodImage
    extra = 1


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    inlines = [FoodImageInline]
    list_display = ['name_of_food']
