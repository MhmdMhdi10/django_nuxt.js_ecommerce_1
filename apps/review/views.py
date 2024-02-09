from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Review  # Import your Product and Review models
from apps.product.models import Product


class GetProductReviewsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, productId):
        try:
            product_id = int(productId)
        except:
            return Response(
                {'message': 'Product ID must be an integer', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            if not Product.objects.active().filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.active().get(id=product_id)

            results = []

            if Review.objects.active().filter(product=product).exists():
                reviews = Review.objects.active().order_by(
                    '-created_at'
                ).filter(product=product)

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['body'] = review.comment
                    item['created_at'] = review.created_at
                    item['user'] = review.user.username
                    item['reply'] = review.reply

                    results.append(item)

            return Response(
                {'reviews': results},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetProductReviewView(APIView):
    def get(self, request, productId):
        user = self.request.user

        try:
            product_id = int(productId)
        except:
            return Response(
                {'message': 'Product ID must be an integer', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            if not Product.objects.active().filter(id=product_id).exists():
                return Response(
                    {'message': 'This product does not exist', "type": "failure"},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.active().get(id=product_id)

            result = {}

            if Review.objects.active().filter(user=user, product=product).exists():
                review = Review.objects.active().get(user=user, product=product)

                result['id'] = review.id
                result['rating'] = review.rating
                result['body'] = review.comment
                result['created_at'] = review.created_at
                result['user'] = review.user.username
                result['reply'] = review.reply

            if len(result) == 0:
                return Response(
                    {'review': None, "message": "no review found", "type": "info"},
                    status=status.HTTP_200_OK
                )

            return Response(
                {'review': result},
                status=status.HTTP_200_OK
            )


        except:
            return Response(
                {'error': 'Something went wrong when retrieving review'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateProductReviewView(APIView):
    def post(self, request, productId):
        user = self.request.user
        data = self.request.data

        try:
            rating = float(data['rating'])
        except:
            return Response(
                {'message': 'Rating must be a decimal value', "type": "failure"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            comment = str(data['comment'])
        except:
            return Response(
                {'message': 'Must pass a comment when creating review', "type": "failure"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if not Product.objects.active().filter(id=productId).exists():
                return Response(
                    {'message': 'This Product does not exist', "type": "failure"},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.active().get(id=productId)

            result = {}
            results = []

            if Review.objects.active().filter(user=user, product=product).exists():
                return Response(
                    {'message': 'Review for this course already created', "type": "failure"},
                    status=status.HTTP_409_CONFLICT
                )

            review = Review.objects.create(
                user=user,
                product=product,
                rating=rating,
                comment=comment,
            )

            if Review.objects.active().filter(user=user, product=product).exists():
                result['id'] = review.id
                result['rating'] = review.rating
                result['body'] = review.comment
                result['created_at'] = review.created_at
                result['user'] = review.user.username
                result['reply'] = review.reply

                reviews = Review.objects.active().order_by('-created_at').filter(
                    product=product
                )

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['body'] = review.comment
                    item['created_at'] = review.created_at
                    item['user'] = review.user.username
                    item['reply'] = review.reply

                    results.append(item)

            return Response(
                {'review': result, 'reviews': results, "message": "review submitted successfully",
                 "type": "success"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'message': str(e), "type": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateProductReviewView(APIView):
    def put(self, request, productId):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(productId)
        except:
            return Response(
                {'message': 'Product ID must be an integer', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            rating = int(data['rating'])
        except:
            return Response(
                {'message': 'Rating must be an integer value' , "type": "failure"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            comment = str(data['comment'])
        except:
            return Response(
                {'message': 'Must pass a comment when creating review', "type": "failure"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if not Product.objects.active().filter(id=product_id).exists():
                return Response(
                    {'message': 'This product does not exist', "type": "failure"},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.active().get(id=product_id)

            result = {}
            results = []

            if not Review.objects.active().filter(user=user, product=product).exists():
                return Response(
                    {'message': 'Review for this product does not exist', "type": "failure"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if Review.objects.active().filter(user=user, product=product).exists():
                Review.objects.active().filter(user=user, product=product).update(
                    rating=rating,
                    comment=comment
                )

                review = Review.objects.active().get(user=user, product=product)

                result['id'] = review.id
                result['rating'] = review.rating
                result['body'] = review.comment
                result['created_at'] = review.created_at
                result['user'] = review.user.username
                result['reply'] = review.reply

                reviews = Review.objects.active().order_by('-created_at').filter(
                    product=product
                )

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['body'] = review.comment
                    item['created_at'] = review.created_at
                    item['user'] = review.user.username
                    item['reply'] = review.reply

                    results.append(item)

            return Response(
                {'review': result, 'reviews': results, "message": "review submitted successfully",
                 "type": "success"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': str(e), 'type': 'failure'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteProductReviewView(APIView):
    def delete(self, request, productId):
        user = self.request.user

        try:
            product_id = int(productId)
        except:
            return Response(
                {'message': 'Product ID must be an integer', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            if not Product.objects.active().filter(id=product_id).exists():
                return Response(
                    {'message': 'This product does not exist', "type": "failure"},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.active().get(id=product_id)

            results = []

            if Review.objects.active().filter(user=user, product=product).exists():
                Review.objects.active().filter(user=user, product=product).delete()

                reviews = Review.objects.active().order_by('-created_at').filter(
                    product=product
                )

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['body'] = review.comment
                    item['created_at'] = review.created_at
                    item['user'] = review.user.username
                    item['reply'] = review.reply

                    results.append(item)

                return Response(
                    {'reviews': results, "message": "review deleted successfully", "type": "success"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Review for this product does not exist', "type": "failure"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {'message': str(e), "type": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FilterProductReviewsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, productId):
        try:
            product_id = int(productId)
        except:
            return Response(
                {'message': 'Product ID must be an integer', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not Product.objects.active().filter(id=product_id).exists():
            return Response(
                {'message': 'This product does not exist', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND
            )

        product = Product.objects.active().get(id=product_id)

        rating = request.data.get('rating')

        try:
            rating = int(rating)
        except:
            return Response(
                {'message': 'Rating must be an integer value', "type": "failure"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if not rating:
                rating = 10
            elif rating > 10:
                rating = 10
            elif rating < 1:
                rating = 1

            results = []

            if Review.objects.active().filter(product=product).exists():
                if rating == 1:
                    reviews = Review.objects.active().order_by('-created_at').filter(
                        rating=rating, product=product
                    )
                else:
                    reviews = Review.objects.active().order_by('-created_at').filter(
                        rating__lte=rating,
                        product=product
                    ).filter(
                        rating__gte=(rating - 1),
                        product=product
                    )

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['body'] = review.comment
                    item['created_at'] = review.created_at
                    item['user'] = review.user.username
                    item['reply'] = review.reply

                    results.append(item)

            return Response(
                {'reviews': results, "message": "reviews filtered successfully", "type": "success"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': str(e), "type": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
