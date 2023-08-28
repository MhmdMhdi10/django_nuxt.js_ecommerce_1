from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Category
from .serializers import CategorySerializer


class CategoryListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_subcategories(self, category):
        subcategories = Category.objects.active().filter(parent=category)
        subcategory_data = CategorySerializer(subcategories, many=True).data

        for subcategory in subcategory_data:
            subcategory['sub_categories'] = self.get_subcategories(subcategory['id'])

        return subcategory_data

    def get(self, request):
        categories = Category.objects.active().filter(parent=None)

        if not categories.exists():
            return Response({'message': 'No category found', 'type': 'failure'}, status=status.HTTP_404_NOT_FOUND)

        serialized_categories = CategorySerializer(categories, many=True).data

        for category in serialized_categories:
            category['sub_categories'] = self.get_subcategories(category['id'])

        return Response({'categories': serialized_categories, 'message': 'categories displayed successfully', 'type': 'success'}, status=status.HTTP_200_OK)
