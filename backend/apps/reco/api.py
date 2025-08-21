from rest_framework import serializers, views
from rest_framework.response import Response
from apps.catalog.models import Product
from apps.catalog.serializers import ProductSerializer
from apps.interactions.models import Interaction
from .inference import recommend_for_user


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ["user","product","type","value","context"]


class RecommendationsView(views.APIView):
    def get(self, request):
        user_id = int(request.query_params.get("user_id"))
        k = int(request.query_params.get("k", 20))
        items = recommend_for_user(user_id=user_id, k=k)
        data = [{"product": ProductSerializer(p).data, "score": float(s)} for p,s in items]
        return Response(data)


class LogInteractionView(views.APIView):
    def post(self, request):
        ser = InteractionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        inter = ser.save()
        return Response({"ok": True, "id": inter.id})