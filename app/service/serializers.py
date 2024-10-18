from rest_framework import serializers
from django.contrib.gis.geos import Polygon, Point, MultiPolygon, MultiLineString, LineString
from .models import State, Capital, River
from django.db import transaction


class StateSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ['id', 'name', 'area', 'geometry']

    def get_geometry(self, obj):
        # Convert the MultiPolygon to GeoJSON-like structure
        if isinstance(obj.geometry, MultiPolygon):
            return {
                "type": "MultiPolygon",
                "coordinates": obj.geometry.coords
            }
        return None

    def create(self, validated_data):
        # Extract the geometry (MultiPolygon) from the validated_data
        geometry_data = validated_data.pop('geometry')
        coordinates = geometry_data['coordinates']

        # Convert each set of coordinates into a Polygon object
        polygons = []
        for polygon_coords in coordinates:
            polygons.append(Polygon(*polygon_coords))

        # Create a MultiPolygon from the list of Polygon objects
        multipolygon = MultiPolygon(*polygons)

        # Create and return the State instance with the correct 'geometry' field
        state = State.objects.create(geometry=multipolygon, **validated_data)
        return state

    def update(self, instance, validated_data):
        # Extract geometry if present
        geometry_data = validated_data.pop('geometry', None)
        if geometry_data:
            coordinates = geometry_data['coordinates']
            instance.geometry = MultiPolygon(*[Polygon(*polygon_coords) for polygon_coords in coordinates])

        # Update other fields
        instance.name = validated_data.get('name', instance.name)
        instance.area = validated_data.get('area', instance.area)
        instance.save()
        return instance

class CapitalSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = Capital
        fields = ['id', 'name', 'location']

    def get_location(self, obj):
        # Convert the location Point into a GeoJSON-compatible structure
        if isinstance(obj.location, Point):
            return {
                "type": "Point",
                "coordinates": [obj.location.x, obj.location.y]
            }
        return None

    def create(self, validated_data):
        # Directly use location in the payload, no conversion needed
        location_data = validated_data.pop('location')
        coordinates = location_data['coordinates']

        # Create a Point object from the coordinates
        point = Point(coordinates[0], coordinates[1])

        # Create and return a Capital instance
        capital = Capital.objects.create(location=point, **validated_data)
        return capital

    def update(self, instance, validated_data):
        # Extract location if present
        location_data = validated_data.pop('location', None)
        if location_data:
            coordinates = location_data['coordinates']
            instance.location = Point(coordinates[0], coordinates[1])

        # Update other fields
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class RiverSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField()

    class Meta:
        model = River
        fields = ['id', 'name', 'geometry']

    def get_geometry(self, obj):
        # Convert MultiLineString to GeoJSON format
        if isinstance(obj.geometry, MultiLineString):
            return {
                "type": "MultiLineString",
                "coordinates": obj.geometry.coords
            }
        return None

    def create(self, validated_data):
        print(validated_data.get('type'))
        # Extract the geometry from validated data
        geometry_data = validated_data.pop('geometry')
        coordinates = geometry_data['coordinates']

        lines = []
        for line_coords in coordinates:
            lines.append(LineString(line_coords))

        multilinestring = MultiLineString(*lines)

        # Create the River instance
        river = River.objects.create(geometry=multilinestring, **validated_data)
        return river

    def update(self, instance, validated_data):
        # Extract geometry if present
        geometry_data = validated_data.pop('geometry', None)
        if geometry_data:
            coordinates = geometry_data['coordinates']
            linestrings = [LineString(line_coords) for line_coords in coordinates]
            instance.geometry = MultiLineString(linestrings)

        # Update other fields
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance