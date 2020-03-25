import json
from django.contrib import admin
from django.utils.text import slugify
from django.db import models
from ckeditor.widgets import CKEditorWidget
from .models import Skill, Level, SkillJSON

# Register your models here.

def processJSON(modeladmin, request, queryset):
    for file in queryset:
        #file.file.open()
        data = json.load(file.file)
        for skill in data['skills']:
            page_attrs = {
                'name': skill['name'],
                'description': skill['description'],
            }
            page, page_created = Skill.objects.get_or_create(code=slugify(skill['code']), defaults=page_attrs)
            if not page_created:
                continue
            else:
                #Delete current levels if updating
                for level in Level.objects.filter(skill=page):
                    level.delete()
            for level in skill['levels']:
                Level.objects.create(skill=page, level=level['level'], description=level['description'])

processJSON.short_description = 'Upload to Models'

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

class SkillJSONAdmin(admin.ModelAdmin):
    model = SkillJSON
    actions = [processJSON]

admin.site.register(Skill, SkillAdmin)
admin.site.register(SkillJSON, SkillJSONAdmin)