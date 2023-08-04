from django.db import models


class Queries(models.Model):
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    number_of_data = models.IntegerField()
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=20, default=None, null=True)


class Google_data(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField()
    reviews = models.IntegerField()
    query_id = models.ForeignKey(Queries, on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    number_of_data = models.IntegerField()
    status = models.CharField(max_length=20)


