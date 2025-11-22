from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from accessrequestsapi.users.api.views import UserViewSet
from accessrequestsapi.access_control.api.views import SystemViewSet, AccessRequestViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("systems", SystemViewSet)
router.register("access-requests", AccessRequestViewSet, basename="access-request")


app_name = "api"
urlpatterns = router.urls
