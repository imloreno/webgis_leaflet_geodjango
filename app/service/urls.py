from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StateViewSet, CapitalViewSet, RiverViewSet

router = DefaultRouter()
router.register(r'states', StateViewSet, basename='state')
router.register(r'capitals', CapitalViewSet, basename='capital')
router.register(r'rivers', RiverViewSet, basename='rivers')

urlpatterns = [
    # other paths
    path('', include(router.urls)),
]