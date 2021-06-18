import os
import random
from django.db import models


def upload_image_path(instance, filename):
    print(instance, filename)
    new_name = random.randint(1000000, 9999999)
    name, ext = Product.get_filename_ext(filename)
    final_name = f'{new_name}{ext}'
    return f'products/images/{final_name}'


class Category(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        if not self.parent:
            return f"Category: {self.name}"
        else:
            return f"{self.parent} --> {self.name}"

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)
    preview = models.ImageField(upload_to=upload_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey('user.CustomUser', related_name='Products', on_delete=models.CASCADE)

    @staticmethod
    def get_filename_ext(filepath):
        base_name = os.path.basename(filepath)
        name, ext = os.path.splitext(base_name)
        return name, ext

    def __str__(self):
        return f'{self.category}-->{self.title}'


class Tour(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=False)
    owner = models.ForeignKey('user.CustomUser', related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', null=True)
    preview = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return f"{self.owner}-->{self.title}"


class PostImages(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    @staticmethod
    def generate_name():
        import random
        return "Image" + str(random.randint(1, 99999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(PostImages, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} --> {self.post.id}"


class Comment(models.Model):
    owner = models.ForeignKey('user.CustomUser', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Tour, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner}-->{self.post}-->{self.created_at}-->{self.body[0:10]}"


class Rating(models.Model):
    owner = models.ForeignKey('user.CustomUser', related_name='rating', on_delete=models.CASCADE)
    VALUE = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    )

    rating_field = models.CharField(choices=VALUE, max_length=1, blank=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="rating")

    def __str__(self):
        return f"{self.rating_field} - {self.tour}-->{self.owner}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Like(models.Model):
    owner = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False, blank=True)

    # def __str__(self):
    #     return f'{self.owner}-->{self.post}'
