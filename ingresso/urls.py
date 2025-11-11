from django.urls import path
from .views import (
    EventoListClienteView,
    IngressoListClienteView,
    comprar_ingresso,
    confirmar_pagamento,
    registrar_cliente,

    EventoAdminView,
    IngressoAdminView,
    BloqueioAdminView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    # CLIENTE
    path('eventos/', EventoListClienteView.as_view()),
    path('eventos/<int:evento_id>/ingressos/', IngressoListClienteView.as_view()),
    path('comprar/', comprar_ingresso),
    path('confirmar-pagamento/', confirmar_pagamento),
    path('registrar/', registrar_cliente),

    # ADMIN
    path('admin/eventos/', EventoAdminView.as_view()),
    path('admin/ingressos/', IngressoAdminView.as_view()),
    path('admin/bloqueios/', BloqueioAdminView.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
