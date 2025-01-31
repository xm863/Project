from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Users(AbstractUser):
    about = models.TextField()
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    address = models.CharField(max_length=500)

class Categories(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    category = models.ManyToManyField(Categories)
    reviews = models.IntegerField()

    class Meta:
        db_table = 'apps_food'

    def __str__(self):
        return self.name

class FoodImage(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="images/")
    
    def __str__(self):
        return self.food.name
    
class Theme(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class New(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.ManyToManyField(Theme)
    about = models.TextField()

    class Meta:
        db_table = 'apps_new'

    def __str__(self):
        return self.name

class NewsImage(models.Model):
    news = models.ForeignKey(New, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.news.name
    
class Comment(models.Model):
    news = models.ForeignKey(New, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='comments') 
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.user.username} dan {self.news.name}"
