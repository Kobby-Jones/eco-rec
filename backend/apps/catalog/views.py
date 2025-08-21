from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class ProductSearch(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        q = self.request.query_params.get("query")
        category_id = self.request.query_params.get("category_id")
        if q: qs = qs.filter(title__icontains=q)
        if category_id: qs = qs.filter(category_id=category_id)
        return qs.order_by("-id")