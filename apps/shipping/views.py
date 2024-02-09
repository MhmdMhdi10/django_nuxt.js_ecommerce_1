from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Shipping
from .serializers import ShippingSerializer


class GetShippingView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        if Shipping.objects.active().all().exists():
            shipping_options = Shipping.objects.active().order_by('shipping_cost').all()
            shipping_options = ShippingSerializer(shipping_options, many=True)

            return Response(
                {'shipping_options': shipping_options.data, "message": "shipping list returned successfully",
                 "type": "success"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'No shipping options available', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND
            )