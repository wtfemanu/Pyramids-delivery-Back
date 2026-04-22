from django.contrib import admin
from django.urls import include, path
from core.models import Motorista
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from core.views import MotoristaViewSet, UserRegistrationView, UserViewSet, VeiculoViewSet, CargaViewSet, RotaViewSet, UserViewSet, FreteViewSet, CustomLoginView

router = DefaultRouter()

router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'motoristas',MotoristaViewSet, basename='motoristas')
router.register(r'veiculos',VeiculoViewSet, basename='veiculos')
router.register(r'cargas',CargaViewSet, basename='cargas')
router.register(r'rotas',RotaViewSet, basename='rotas')
router.register(r'fretes',FreteViewSet, basename='fretes')


urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/doc/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    # Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Registro de usuários
    path('api/registro/', UserRegistrationView.as_view(), name='user_registration'),
    path('api/login/', CustomLoginView.as_view(), name='login'),
    # API
    path('api/', include(router.urls)),
  
]
