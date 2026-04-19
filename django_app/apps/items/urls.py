from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, CategoryViewSet, LocationViewSet, index_view, report_item_view, item_detail_view, contact_info_view, resolve_item_view, seed_data_view

app_name = 'items'

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('', index_view, name='index'),
    path('item/<int:pk>/', item_detail_view, name='item_detail'),
    path('item/<int:pk>/contact/', contact_info_view, name='contact_info'),
    path('item/<int:pk>/resolve/', resolve_item_view, name='resolve_item'),
    path('report/<str:status>/', report_item_view, name='report_item'),
    path('seed-setup-secret/', seed_data_view, name='seed_data'),
    path('api/', include(router.urls)),
]
