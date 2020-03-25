from django.contrib import admin
from .models import Skill, Level
from django.db import models
from ckeditor.widgets import CKEditorWidget

# Register your models here.

class LevelInline(admin.TabularInline):
    model = Level
    formfield_overrides = {
        models.TextField : {'widget': CKEditorWidget(config_name='advanced_setting')},
    }
    ordering = ('level',)
    extra = 0

class SkillAdmin(admin.ModelAdmin):
    model = Skill
    list_display = ['name','code',]
    search_fields = ['name','code']
    inlines = [LevelInline]
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='advanced_setting')},
    }

admin.site.register(Skill, SkillAdmin)