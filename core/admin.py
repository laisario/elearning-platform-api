from django.contrib import admin, auth
from .models import User

admin.site.register(User)
admin.site.unregister(auth.models.Group)