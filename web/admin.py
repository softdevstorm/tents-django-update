from django.contrib import admin

# Register your models here.
from .models import Gallery, Photo

admin.site.register(Gallery)
admin.site.register(Photo)