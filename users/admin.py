from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Drive)
# admin.site.register(Planter)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Tree)
