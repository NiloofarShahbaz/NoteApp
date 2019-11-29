from django.contrib import admin

from .models import *

admin.site.register(Note)
admin.site.register(Reminder)
admin.site.register(Image)
admin.site.register(Item)
admin.site.register(Label)
