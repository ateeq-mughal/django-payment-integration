from django.contrib import admin

from .models import TechBlogs, Customer

# Register your models here.


admin.site.register(TechBlogs)
admin.site.register(Customer)