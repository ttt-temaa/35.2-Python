from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import (PaymentsCreateAPIView, PaymentsViewSet,
                         UserCreateAPIView)

app_name = "users"

router = DefaultRouter()
router.register(r"payment", PaymentsViewSet, basename="payment")

urlpatterns = [
                  path("register/", UserCreateAPIView.as_view(), name="register"),
                  path(
                      "login/",
                      TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
                      name="token_obtain_pair",
                  ),
                  path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
                  path("payment/", PaymentsCreateAPIView.as_view(), name="payment"),
              ] + router.urls
