from django.urls import path
from django.http import JsonResponse
from apps.reco.api import RecommendationsView, LogInteractionView
from apps.catalog.views import ProductDetail, ProductSearch


def health(_):
    return JsonResponse({"ok": True})


urlpatterns = [
path("api/health", health),
path("api/recommendations", RecommendationsView.as_view()),
path("api/interactions", LogInteractionView.as_view()),
path("api/products/<int:pk>", ProductDetail.as_view()),
path("api/products", ProductSearch.as_view()),
]