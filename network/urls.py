from rest_framework.routers import DefaultRouter

from .views import NetworkNodeViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"networknodes", NetworkNodeViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = router.urls
