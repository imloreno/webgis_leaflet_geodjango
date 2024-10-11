from django.contrib.gis.db import models

class Capital(models.Model):
    id = models.IntegerField(primary_key=True)  # 'id' from the properties
    name = models.CharField(max_length=100)     # 'name' from the properties
    location = models.PointField(geography=True)  # 'coordinates' as PointField

    def __str__(self):
        return self.name

class State(models.Model):
    id = models.IntegerField(primary_key=True)  # 'id' from the properties
    name = models.CharField(max_length=100)     # 'name' from the properties
    area = models.FloatField()                  # 'area' from the properties
    geometry = models.MultiPolygonField(geography=True)  # 'geometry' as MultiPolygon

    def __str__(self):
        return self.name

class River(models.Model):
    id = models.CharField(primary_key=True)  # 'full_id' from the properties
    name = models.CharField(max_length=100)    # 'name' from the properties
    layer = models.CharField(max_length=255)   # 'layer' from the properties
    path = models.CharField(max_length=500)    # 'path' from the properties
    geometry = models.MultiLineStringField(geography=True)  # 'geometry' as MultiLineString

    def __str__(self):
        return self.name