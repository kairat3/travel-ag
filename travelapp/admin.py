from django.contrib import admin
from django.contrib.auth.models import Group
from travelapp.models import PostImages, Category, Comment, Product, Tour, Rating, Like

admin.site.register(Tour)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(PostImages)
admin.site.unregister(Group)
admin.site.register(Product)
admin.site.register(Rating)
admin.site.register(Like)
