from django.urls import path, include
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from rest_framework import routers
from django.http import JsonResponse
from baton.autodiscover import admin
from api_orders.views import (
    CategoryView,
    ShopView,
    ProductInfoView,
    BasketView,
    OrderView,
    LoginAccount,
    ContactView,
    AccountDetails,
    ConfirmAccount,
    RegisterAccount,
    PartnerOrders,
    PartnerState,
    PartnerUpdate,
    auth
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

def api_home(request):
    data = {
        "message": "Welcome to the API",
        "endpoints": {
            "partner-update": "/api/v1/partner/update/",
            "partner-state": "/api/v1/partner/state/",
            # Другие эндпоинты...
        }
    }
    return JsonResponse(data)

app_name = 'shop'

router = routers.SimpleRouter()
router.register(r'shops', ShopView)
router.register(r'categories', CategoryView)
router.register(r'products', ProductInfoView, basename='products')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('', include('social_django.urls',namespace='social')),
    path('auth/', auth),
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state', PartnerState.as_view(), name='partner-state'),
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/details', AccountDetails.as_view(), name='user-details'),
    path('user/contact', ContactView.as_view(), name='user-contact'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
    path('user/password_reset', reset_password_request_token, name='password-reset'),
    path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    
    path('basket', BasketView.as_view(), name='basket'),
    path('order', OrderView.as_view(), name='order'),
    # path('', include(router.urls)),
    path('api/v1/', api_home, name='api-home'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


urlpatterns += router.urls