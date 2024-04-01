from django.contrib import admin

from blog.models import Category, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    """
    Класс администратора категорий
    """
    search_fields = ('title',)


class LocationAdmin(admin.ModelAdmin):
    """
    Класс администратора местоположений
    """
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    """
    Класс администратора публикаций
    """
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
