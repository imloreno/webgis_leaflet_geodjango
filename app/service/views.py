from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import State, Capital, River
from .serializers import StateSerializer, CapitalSerializer, RiverSerializer


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle multiple features (bulk creation) using 'geometry' field directly.
        """
        data = request.data

        # Check if the data contains a FeatureCollection
        if data.get('type') == 'FeatureCollection':
            features = data.get('features', [])
            response_data = []

            for feature in features:
                # Prepare each feature's properties and geometry (MultiPolygon)
                feature_data = {
                    'id': feature['properties']['id'],
                    'name': feature['properties']['name'],
                    'area': feature['properties']['area'],
                    'geometry': feature['geometry']
                }

                # Create and validate each feature using the serializer
                serializer = self.get_serializer(data=feature_data)
                if serializer.is_valid():
                    serializer.save()
                    response_data.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid GeoJSON format"}, status=status.HTTP_400_BAD_REQUEST)

class CapitalViewSet(viewsets.ModelViewSet):
    queryset = Capital.objects.all()
    serializer_class = CapitalSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle multiple features (bulk creation) using 'location' field directly.
        """
        data = request.data

        # Check if the data contains a FeatureCollection
        if data.get('type') == 'FeatureCollection':
            features = data.get('features', [])
            response_data = []

            for feature in features:
                # Prepare each feature's properties and location
                feature_data = {
                    'id': feature['properties']['id'],
                    'name': feature['properties']['name'],
                    'location': feature['location']  # Directly using 'location' from the payload
                }

                # Create and validate each feature using the serializer
                serializer = self.get_serializer(data=feature_data)
                if serializer.is_valid():
                    serializer.save()
                    response_data.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid GeoJSON format"}, status=status.HTTP_400_BAD_REQUEST)

class RiverViewSet(viewsets.ModelViewSet):
    queryset = River.objects.all()
    serializer_class = RiverSerializer

    def create(self, request, *args, **kwargs):
        """
        Handle multiple features (bulk creation) from a 'FeatureCollection'.
        """
        data = request.data

        # Check if the data contains a FeatureCollection
        if data.get('type') != 'FeatureCollection':
            return Response({"error": "Invalid GeoJSON format, expected 'FeatureCollection'."}, status=status.HTTP_400_BAD_REQUEST)

        features = data.get('features', [])
        response_data = []

        for feature in features:

            # Prepare each feature's properties and geometry (MultiLineString)
            feature_data = {
                'id': feature['properties']['id'],
                'name': feature['properties']['name'],
                'geometry': feature['geometry']  # Pass geometry from feature
            }

            # Create and validate each feature using the serializer
            serializer = self.get_serializer(data=feature_data)
            if serializer.is_valid():
                serializer.save()
                response_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status.HTTP_201_CREATED)
