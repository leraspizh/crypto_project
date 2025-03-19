from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CryptoPriceViewSet, index,stream_data
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'prices', CryptoPriceViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
    path('stream/',stream_data, name='stream_data'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

