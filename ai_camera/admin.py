from django.contrib import admin
from .models import Camera, PlaybackVideo, Person


class PersonAdmin(admin.ModelAdmin):
    fields = ('name', 'career', 'image')

admin.site.register(Camera)
admin.site.register(PlaybackVideo)
admin.site.register(Person, PersonAdmin)
