from django.contrib import admin

# Register your models here.
from .models import Application, Token, Grant

admin.site.register(Application)
admin.site.register(Token)
admin.site.register(Grant)
