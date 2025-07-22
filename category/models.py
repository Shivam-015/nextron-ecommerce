from django.db import models

class Category(models.Model):
    cat_name = models.CharField(max_length=50,unique=True)
    slug     = models.SlugField(max_length=100,unique=True)
    description = models.CharField(max_length=250,blank=True)
    cat_image = models.ImageField(upload_to='images/categories', blank=True)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.cat_name
