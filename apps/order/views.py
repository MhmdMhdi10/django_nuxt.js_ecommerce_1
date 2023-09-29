from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from rest_framework import permissions


class ListOrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = self.request.user
        try:

            orders = Order.objects.active().filter(user=user.id)

            result = []

            for order in orders:

                item = {}
                item['status'] = order.status
                item['transaction_id'] = order.transaction_id
                item['amount'] = order.price
                item['discount_price'] = order.discount_price
                item['shipping_price'] = order.shipping_price
                item['address_line_1'] = order.address
                item['is_paid'] = order.is_paid
                item['creation_date'] = order.created_at
                item['last_update'] = order.updated_at

                result.append(item)


            return Response(
                {'orders': result, "message": "orders list returned successfully", "type": "success"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': str(e), "type": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListOrderDetailView(APIView):
    def get(self, request, transactionId):
        user = self.request.user

        try:
            if Order.objects.active().filter(user=user, transaction_id=transactionId).exists():
                order = Order.objects.active().get(user=user, transaction_id=transactionId)
                result = {}
                result['status'] = order.status
                result['transaction_id'] = order.transaction_id
                result['amount'] = order.price
                result['coupon'] = order.coupon
                result['address_line_1'] = order.address
                result['shipping_name'] = order.shipping_name
                result['shipping_time'] = order.shipping_time
                result['shipping_price'] = order.shipping_price
                result['date_issued'] = order.created_at

                order_items = OrderItem.objects.active().order_by('-date_added').filter(order=order)
                result['order_items'] = []

                for order_item in order_items:
                    sub_item = {}

                    sub_item['name'] = order_item.product.name
                    sub_item['price'] = order_item.price
                    sub_item['count'] = order_item.count

                    result['order_items'].append(sub_item)
                return Response(
                    {'order': result, 'message': 'Order returned successfully',
                     "type": "success"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Order with this transaction ID does not exist', "type": "failure"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {'message': str(e), "type": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
