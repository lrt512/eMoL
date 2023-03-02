from django.urls import include, path, re_path
from rest_framework import routers

from .card import CardDateViewSet, CardViewSet
from .combatant import CombatantListViewSet, CombatantViewSet
from .combatant_authorization import CombatantAuthorizationViewSet
from .combatant_warrant import CombatantWarrantViewSet
from .privacy import ResendPrivacyView
from .waiver import WaiverViewSet

api_router = routers.SimpleRouter()
api_router.register(r"combatant-list", CombatantListViewSet)
api_router.register(r"combatant", CombatantViewSet)
api_router.register(r"combatant-authorization", CombatantAuthorizationViewSet)
api_router.register(r"combatant-warrant", CombatantWarrantViewSet)
api_router.register(r"combatant-cards", CardViewSet)
api_router.register(r"waiver", WaiverViewSet)
api_router.register(r"card-date", CardDateViewSet)

# We have some non-model API views, so let's create urlpatterns manaully
urlpatterns = [
    path("", include(api_router.urls)),
    re_path(r"^resend-privacy/$", ResendPrivacyView.as_view(), name="resend-privacy"),
]
