from django.db import models

class County(models.Model):
    name = models.CharField(max_length=80, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=80, null=True)

    def __str__(self):
        return self.name
