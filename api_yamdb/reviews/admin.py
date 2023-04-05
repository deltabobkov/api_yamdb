from django.contrib import admin

from .models import Title, Genre, Category, Review, Comment


admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Category)
