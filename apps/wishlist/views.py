from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist, WishlistItem
from apps.product.models import Product
from .serializers import WishlistSerializer


class GetWishlistItemsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            # Get the user's wishlist
            user_wishlist = Wishlist.objects.active().get(user=request.user)
            serializer = WishlistSerializer(user_wishlist)

            return Response(
                {
                    'message': 'Wishlist items retrieved successfully',
                    'type': 'success',
                    'items': serializer.data['products'],
                },
                status=status.HTTP_200_OK
            )
        except Wishlist.DoesNotExist:
            return Response(
                {'message': 'Wishlist not found for this user', 'type': 'failure'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'message': str(e), 'type': 'failure'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddItemToWishlistView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Get the user's wishlist or create one if it doesn't exist
            user_wishlist, created = Wishlist.objects.active().get_or_create(user=request.user)

            # Get the product ID from the request data
            product_id = request.data.get('product_id')

            # Check if the product with the specified ID exists
            try:
                product = Product.objects.active().get(id=product_id)
            except Product.DoesNotExist:
                data = {
                    'message': f'Product with ID {product_id} does not exist',
                    'type': 'failure',
                }
                return Response(data, status=status.HTTP_404_NOT_FOUND)

            # Check if the product is already in the wishlist (filter by product and is_deleted)
            if WishlistItem.objects.active().filter(wishlist=user_wishlist, product_id=product_id).exists():
                data = {
                    'message': 'Product is already in the wishlist',
                    'type': 'info',
                }
                return Response(data, status=status.HTTP_200_OK)

            # Add the product to the wishlist (soft delete check is not necessary)
            wishlist_item = WishlistItem(wishlist=user_wishlist, product_id=product_id)
            wishlist_item.save()

            data = {
                'message': 'Product added to wishlist successfully',
                'type': 'success',
            }
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as e:
            data = {
                'message': str(e),
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTotalItemsInWishlistView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            # Get the user's wishlist if it exists
            user_wishlist, created = Wishlist.objects.active().get_or_create(user=request.user)

            # Calculate the total number of items in the wishlist
            total_items = user_wishlist.products.count()

            data = {
                'message': 'Total items in wishlist retrieved successfully',
                'type': 'success',
                'total_items': total_items,
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            data = {
                'message': str(e),
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveItemFromWishlistView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Get the user's wishlist if it exists
            user_wishlist = Wishlist.objects.active().get(user=request.user)

            # Get the product ID from the request data
            product_id = request.data.get('product_id')

            # Check if the product is in the user's wishlist
            try:
                wishlist_item = WishlistItem.objects.active().get(wishlist=user_wishlist, product_id=product_id)
                wishlist_item.delete()  # Remove the item from the wishlist
                data = {
                    'message': 'Product removed from wishlist successfully',
                    'type': 'success',
                }
                return Response(data, status=status.HTTP_200_OK)
            except WishlistItem.DoesNotExist:
                data = {
                    'message': 'Product is not in the wishlist',
                    'type': 'info',
                }
                return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            data = {
                'message': 'Something went wrong when removing the product from the wishlist',
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
