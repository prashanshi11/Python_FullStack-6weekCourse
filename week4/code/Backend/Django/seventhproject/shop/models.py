from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


class ProductDetail(models.Model):
    description = models.TextField()
    warranty = models.CharField(max_length=100)

    def __str__(self):
        return f"Detail: {self.description[:20]}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    detail = models.OneToOneField(ProductDetail, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
