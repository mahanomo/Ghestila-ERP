from rest_framework import routers

from .views import StatusModelViewSet

router = routers.DefaultRouter()
router.register("test-api", StatusModelViewSet, basename="p-modelviewset")
urlpatterns = router.urls