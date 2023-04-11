from django.contrib import admin
from .models import *
# Register your models here.


class SlideAdmin(admin.ModelAdmin):
    list_display = ['name', 'detail', 'image']

# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ['title', 'slug', 'description', 'researcher', 'image1', 'image2',]
#     prepopulated_fields = {'slug': ('title',)}

# class CommodityAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'detail', 'image', 'created_at',]
#     prepopulated_fields = {'slug': ('name',)}

admin.site.register(Slide, SlideAdmin)
# admin.site.register(Commodity, CommodityAdmin)
admin.site.register(About)
admin.site.register(Organization)
# admin.site.register(Project, ProjectAdmin)
admin.site.register(Album)
admin.site.register(AlbumPhoto)