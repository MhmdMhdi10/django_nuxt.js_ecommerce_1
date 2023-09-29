from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Coupon


class CheckCouponView(APIView):
    def post(self, request):
        # Get the coupon code from the request data
        coupon_code = request.data.get('code', '')

        # Check if the coupon with the given code exists
        try:
            coupon = Coupon.objects.active().get(code=coupon_code)
        except Coupon.DoesNotExist:
            return Response({'type': 'failure', 'message': _('Coupon not found')}, status=status.HTTP_404_NOT_FOUND)

        # Check if the coupon has expired
        if coupon.expire_date < timezone.now():
            return Response({'type': 'failure', 'message': _('Coupon has expired')}, status=status.HTTP_400_BAD_REQUEST)

        # Build the response with coupon information
        response_data = {
            'type': 'success',
            'message': _('Coupon is valid'),
            'code': coupon.code,
            'coupon_type': coupon.get_coupon_type_display(),
            'coupon_value': coupon.coupon_value,
            'expire_date': coupon.expire_date.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return Response(response_data, status=status.HTTP_200_OK)
