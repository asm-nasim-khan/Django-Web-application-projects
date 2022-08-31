# Register your models here.
from django.contrib import admin
from .models import Courses
from .models import Cart
admin.site.register(Courses)
admin.site.register(Cart)

