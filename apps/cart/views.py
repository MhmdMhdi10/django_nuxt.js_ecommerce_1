from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from apps.product.models import Product
from apps.product.serializers import ProductSerializer  # Import your ProductSerializer
from django.db.models import Sum  # Import Sum from django.db.models


class GetItemsView(APIView):
    permission_classes = [IsAuthenticated]  # Apply permission classes

    def get(self, request):
        try:
            user = self.request.user
            cart = Cart.objects.active().get(user=user)
            cart_items = CartItem.objects.active().filter(cart=cart)

            if cart_items.exists():
                result = []
                for cart_item in cart_items:
                    item = {
                        'id': cart_item.id,
                        'count': cart_item.count,
                        'product': ProductSerializer(cart_item.product).data
                    }

                    result.append(item)

                return Response({'message': 'Cart items retrieved successfully', 'type': 'success',
                                 'cart': result},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Cart is empty', 'type': 'success', 'cart': []},
                                status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart not found', 'type': 'failure'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'type': 'failure'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddItemView(APIView):
    def post(self, request):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])
        except Exception as e:
            return Response(
                {'message': 'Product ID must be an integer', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND)

        count = 1

        try:
            if not Product.objects.active().filter(id=product_id).exists():
                return Response(
                    {'message': 'This product does not exist', "type": "failure"},
                    status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.active().get(id=product_id)

            cart = Cart.objects.active().get(user=user)

            if CartItem.objects.active().filter(cart=cart, product=product).exists():
                return Response(
                    {'message': 'Item is already in cart', "type": "failure"},
                    status=status.HTTP_409_CONFLICT)

            if int(product.count) > 0:
                CartItem.objects.create(
                    product=product, cart=cart, count=count
                )

                if CartItem.objects.active().filter(cart=cart, product=product).exists():

                    cart_items = CartItem.objects.active().order_by(
                        'product').filter(cart=cart)

                    result = []

                    for cart_item in cart_items:
                        item = {}
                        item['id'] = cart_item.id
                        item['count'] = cart_item.count
                        product = Product.objects.active().get(id=cart_item.product.id)
                        product = ProductSerializer(product)

                        item['product'] = product.data

                        result.append(item)

                    return Response({'cart': result,
                                     "message": "product added to cart successfully",
                                     "type": "success"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {'message': 'Not enough of this item in stock', "type": "failure"},
                        status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {'message': str(e), "type": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateItemView(APIView):
    def put(self, request):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])
        except Exception as e:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        try:
            count = int(data['count'])
        except Exception as e:
            return Response(
                {'error': 'Count value must be an integer'},
                status=status.HTTP_404_NOT_FOUND)

        try:
            if not Product.objects.active().filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exist'},
                    status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.active().get(id=product_id)
            cart = Cart.objects.active().get(user=user)

            if not CartItem.objects.active().filter(cart=cart, product=product).exists():
                return Response(
                    {'error': 'This product is not in your cart'},
                    status=status.HTTP_404_NOT_FOUND)

            quantity = product.count

            if count <= quantity:
                CartItem.objects.active().filter(
                    product=product, cart=cart
                ).update(count=count)

                cart_items = CartItem.objects.active().order_by(
                    'product').filter(cart=cart)

                result = []

                for cart_item in cart_items:
                    item = {}

                    item['id'] = cart_item.id
                    item['count'] = cart_item.count
                    product = Product.objects.active().get(id=cart_item.product.id)
                    product = ProductSerializer(product)

                    item['product'] = product.data

                    result.append(item)

                return Response({'cart': result}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Not enough of this item in stock'},
                    status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Something went wrong when updating cart item'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTotalView(APIView):
    def get(self, request):
        user = self.request.user

        try:
            cart = Cart.objects.active().get(user=user)
            cart_items = CartItem.objects.active().filter(cart=cart)

            total_cost = 0
            total_discount_cost = 0

            if cart_items.exists():

                for cart_item in cart_items:

                    total_cost += int(cart_item.product.price) * int(cart_item.count)

                    if cart_item.product.discount_type == "percentage":
                        total_discount_cost += (cart_item.product.price * int(cart_item.product.discount_value)
                                                * int(cart_item.count) / 100)
                    else:
                        total_discount_cost += int(cart_item.product.discount_value) * int(cart_item.count)

                    total_cost = int(round(total_cost, 0))
                    total_discount_cost = int(round(total_discount_cost, 0))
            return Response(
                {'total_cost': total_cost, 'total_discount_cost': total_discount_cost},
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTotalCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = self.request.user
            cart = Cart.objects.active().get(user=user)

            # Calculate the total count of items in the cart using the Sum aggregation
            total_items = CartItem.objects.active().filter(cart=cart).aggregate(total_count=Sum('count'))['total_count']

            if total_items is not None:
                return Response({'message': 'Total number of items in the cart', 'type': 'success',
                                 'total_items': total_items},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Cart is empty', 'type': 'success', 'total_items': 0},
                                status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart not found', 'type': 'failure'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'type': 'failure'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveItemView(APIView):
    def delete(self, request):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])
        except Exception as e:
            return Response(
                {'message': 'Product ID must be an integer', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND)

        try:
            if not Product.objects.active().filter(id=product_id).exists():
                return Response(
                    {'message': 'This product does not exist', "type": "failure"},
                    status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.active().get(id=product_id)
            cart = Cart.objects.active().get(user=user)

            if not CartItem.objects.active().filter(cart=cart, product=product).exists():
                return Response(
                    {'message': 'This product is not in your cart', 'type': 'failure'},
                    status=status.HTTP_404_NOT_FOUND)

            CartItem.objects.active().filter(cart=cart, product=product).delete()

            cart_items = CartItem.objects.active().order_by('product').filter(cart=cart)

            result = []

            if CartItem.objects.active().filter(cart=cart).exists():
                for cart_item in cart_items:
                    item = {}

                    item['id'] = cart_item.id
                    item['count'] = cart_item.count
                    product = Product.objects.active().get(id=cart_item.product.id)
                    product = ProductSerializer(product)

                    item['product'] = product.data

                    result.append(item)

            return Response({'cart': result, "message": "product removed successfully", "type": "success"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmptyCartView(APIView):
    def delete(self, request):
        user = self.request.user

        try:
            cart = Cart.objects.active().get(user=user)

            if not CartItem.objects.active().filter(cart=cart).exists():
                return Response(
                    {'message': 'Cart is already empty', "type": 'success'},
                    status=status.HTTP_200_OK)

            CartItem.objects.active().filter(cart=cart).delete()

            return Response(
                {'message': 'Cart emptied successfully', "type": "failure"},
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'message': str(e), "type": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SynchCartView(APIView):
    def put(self, request):
        user = self.request.user
        data = self.request.data

        try:
            cart_items = data['cart_items']

            for cart_item in cart_items:
                cart = Cart.objects.active().get(user=user)

                try:
                    product_id = int(cart_item['product_id'])
                except Exception as e:
                    return Response(
                        {'message': 'Product ID must be an integer', "type": "failure"},
                        status=status.HTTP_404_NOT_FOUND)

                if not Product.objects.active().filter(id=product_id).exists():
                    return Response(
                        {'message': 'Product with this ID does not exist', "type": "success"},
                        status=status.HTTP_404_NOT_FOUND)

                product = Product.objects.active().get(id=product_id)
                quantity = product.count

                if CartItem.objects.active().filter(cart=cart, product=product).exists():
                    # Actualiizamos el item del carrito
                    item = CartItem.objects.active().get(cart=cart, product=product)
                    count = item.count

                    try:
                        cart_item_count = int(cart_item['count'])
                    except Exception as e:
                        cart_item_count = 1

                    # Chqueo con base de datos
                    if (cart_item_count + int(count)) <= int(quantity):
                        updated_count = cart_item_count + int(count)
                        CartItem.objects.active().filter(
                            cart=cart, product=product
                        ).update(count=updated_count)
                else:
                    # Agregar el item al carrito del usuario
                    try:
                        cart_item_count = int(cart_item['count'])
                    except Exception as e:
                        cart_item_count = 1

                    if cart_item_count <= quantity:
                        CartItem.objects.create(
                            product=product, cart=cart, count=cart_item_count
                        )

                return Response(
                    {'message': 'Cart Synchronized', "type": "success"},
                    status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'message': str(e), "type": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
