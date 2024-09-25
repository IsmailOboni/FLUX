from django.contrib import admin
from .models import User

# Register your models here.
admin.site.site_header = "Virtual Learning"
admin.site.site_title = "Flux"
admin.site.register(User)
