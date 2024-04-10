from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Brand
from .serializers import BrandSerializer


class BrandListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        brands = Brand.objects.active()

        if not brands.exists():
            return Response({'message': 'No brand was found', 'type': 'failure'}, status=status.HTTP_404_NOT_FOUND)

        serialized_brands = BrandSerializer(brands, many=True).data

        return Response({'brands': serialized_brands, 'message': 'brands displayed successfully',
                         'type': 'success'}, status=status.HTTP_200_OK)


class BrandDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pid):
        try:
            brand_id = pid
        except Exception as e:
            return Response(
                {'message': 'Brand ID must be an integer', 'type': 'failure'},
                status=status.HTTP_404_NOT_FOUND)

        if Brand.objects.active().filter(id=brand_id).exists():
            brand = Brand.objects.active().get(id=brand_id)
            brand = BrandSerializer(brand)

            return Response({'Brand': brand.data,
                             'message': 'brand returned successfully', 'type': 'success'},
                            status=status.HTTP_200_OK)

        else:
            return Response(
                {'message': 'brand with this ID does not exist', 'type': 'failure'},
                status=status.HTTP_404_NOT_FOUND)
