from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models.parsing import ParsingRule

@admin.register(ParsingRule)
class ParsingRuleAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'file_type', 'created_at', 'updated_at')
    search_fields = ('bank_name', 'file_type')
