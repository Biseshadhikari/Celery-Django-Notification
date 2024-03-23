from django.contrib import admin
from .models import * 
admin.site.register(Creator)
# Register your models here.
admin.site.register(Post)
admin.site.register(Notification)
