from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from apps.product.models import Product
from apps.ProductPhotos.models import ProductPhoto
from apps.product.serializers import ProductSerializer
from apps.ProductPrice.serializers import PriceByUnitSerializer
from apps.category.models import Category
from django.db.models import Q


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Product
from .serializers import ProductSerializer


class ListProductsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        sort_by = request.query_params.get('sort_by')
        if not (sort_by == 'created' or sort_by == 'price' or sort_by == 'sold' or sort_by == 'name'):
            sort_by = 'created_at'

        order = request.query_params.get('order')
        limit = request.query_params.get('limit')
        page = request.query_params.get('page', 0)

        limit = int(limit)
        page = int(page)

        offset = (int(page)-1) * int(limit)

        if not limit:
            limit = 12

        try:
            limit = int(limit)
        except ValueError:
            return Response(
                {'message': 'Limit must be an integer', 'type': 'failure'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if limit <= 0:
            limit = 12

        try:
            offset = int(offset)
        except ValueError:
            return Response(
                {'message': 'Offset must be an integer', 'type': 'failure'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if page < 0:
            page = 0

        if order == 'desc':
            sort_by = '-' + sort_by

        total_products = Product.objects.active().count()
        products = Product.objects.active().order_by(sort_by)[offset:offset+limit]
        serialized_products = ProductSerializer(products, many=True)

        return Response(
            {
                'products': serialized_products.data,
                'total_products': total_products,
                'message': 'Products listed successfully',
                'type': 'success'
            },
            status=status.HTTP_200_OK
        )


class ProductDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pid):
        try:
            slug = pid
        except Exception as e:
            return Response(
                {'message': 'Product ID must be an integer', 'type': 'failure'},
                status=status.HTTP_404_NOT_FOUND)

        if Product.objects.active().filter(slug=slug).exists():
            product = Product.objects.active().get(slug=slug)
            product = ProductSerializer(product)

            return Response({'product': product.data,
                             'message': 'product returned successfully', 'type': 'success'},
                            status=status.HTTP_200_OK)

        else:
            return Response(
                {'message': 'Product with this ID does not exist', 'type': 'failure'},
                status=status.HTTP_404_NOT_FOUND)


class ListSearchView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = self.request.data

        try:
            category_id = int(data['category_id'])
        except Exception as e:
            return Response(
                {'message': 'Category ID must be an integer', 'type': 'failure'},
                status=status.HTTP_404_NOT_FOUND)

        search = data['search']

        page = data['page']
        limit = data['limit']

        offset = (int(page) - 1) * int(limit)

        if not limit:
            limit = 12

        try:
            limit = int(limit)
        except ValueError:
            return Response(
                {'message': 'Limit must be an integer', 'type': 'failure'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if limit <= 0:
            limit = 12

        try:
            offset = int(offset)
        except ValueError:
            return Response(
                {'message': 'Offset must be an integer', 'type': 'failure'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if page < 0:
            page = 0



        if len(search) == 0:
            search_results = Product.objects.active().order_by('-created_at').all()[offset:offset+limit]
            total_products = Product.objects.active().count()
        else:
            search_results = Product.objects.active().filter(
                Q(description__icontains=search) | Q(name__icontains=search)
            )[offset:offset+limit]
            total_products = Product.objects.active().filter(
                Q(description__icontains=search) | Q(name__icontains=search)
            ).count()


        if category_id == 0:

            search_results = ProductSerializer(search_results, many=True)
            return Response(
                {'search_products': search_results.data,
                 "total_products": total_products,
                 'message': 'search results returned successfully', 'type': 'success'},
                status=status.HTTP_200_OK)

        if not Category.objects.active().filter(id=category_id).exists():
            return Response(
                {'message': 'Category not found', 'type': 'failure'},
                status=status.HTTP_404_NOT_FOUND)

        category = Category.objects.active().get(id=category_id)

        if category.parent:
            search_results = search_results.order_by(
                '-created_at'
            ).filter(category=category)

        else:
            if not Category.objects.active().filter(parent=category).exists():
                search_results = search_results.order_by(
                    '-created_at'
                ).filter(category=category)

            else:
                categories = Category.objects.active().filter(parent=category)
                filtered_categories = [category]

                for cat in categories:
                    filtered_categories.append(cat)

                filtered_categories = tuple(filtered_categories)

                search_results = search_results.order_by(
                    '-created_at'
                ).filter(category__in=filtered_categories)

        search_results = ProductSerializer(search_results, many=True)



        if len(search_results.data) == 0:
            return Response({'search_products': search_results.data,
                             'message': 'no product were found', 'type': 'failure'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({'search_products': search_results.data,
                         "total_products": total_products,
                         'message': 'search results returned successfully', 'type': 'success'},
                        status=status.HTTP_200_OK)


class ListBySearchView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = self.request.data

        try:
            category_id = int(data['category_id'])
        except Exception as e:
            return Response(
                {'message': 'Category ID must be an integer', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND)

        least_price = data['least_price']
        most_price = data['most_price']
        sort_by = data['sort_by']

        if not (sort_by == 'created_at' or sort_by == 'price' or sort_by == 'sold' or sort_by == 'name'):
            sort_by = 'created_at'

        order = data['order']

        if category_id == 0:
            product_results = Product.objects.active().all()
        elif not Category.objects.active().filter(id=category_id).exists():
            return Response(
                {'message': 'This category does not exist', "type": 'failure'},
                status=status.HTTP_404_NOT_FOUND)
        else:
            category = Category.objects.active().get(id=category_id)
            if category.parent:
                product_results = Product.objects.active().filter(category=category)
            else:
                if not Category.objects.active().filter(parent=category).exists():
                    product_results = Product.objects.active().filter(category=category)
                else:
                    categories = Category.objects.active().filter(parent=category)
                    filtered_categories = [category]

                    for cat in categories:
                        filtered_categories.append(cat)

                    filtered_categories = tuple(filtered_categories)
                    product_results = Product.objects.active().filter(
                        category__in=filtered_categories)

        if least_price is not None:
            product_results = product_results.filter(price__gte=least_price-1)

        if most_price is not None:
            product_results = product_results.filter(price__lt=most_price+1)

        if order == 'desc':
            sort_by = '-' + sort_by
            product_results = product_results.order_by(sort_by)
        elif order == 'asc':
            product_results = product_results.order_by(sort_by)
        else:
            product_results = product_results.order_by(sort_by)

        product_results = ProductSerializer(product_results, many=True)

        if len(product_results.data) > 0:
            return Response(
                {'filtered_products': product_results.data,
                 'message': 'results filtered successfully', "type": "success"},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'No products found', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND)


class ListRelatedView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pid):
        try:
            product_id = int(pid)
        except Exception as e:
            return Response(
                {'message': 'Product ID must be an integer', 'type': "failure"},
                status=status.HTTP_404_NOT_FOUND)

        if not Product.objects.active().filter(id=product_id).exists():
            return Response(
                {'message': 'Product with this product ID does not exist', "type": "failure"},
                status=status.HTTP_404_NOT_FOUND)

        category = Product.objects.active().get(id=product_id).category

        if Product.objects.active().filter(category=category).exists():
            if category.parent:
                related_products = Product.objects.active().order_by(
                    '-sold'
                ).filter(category=category)
            else:
                if not Category.objects.active().filter(parent=category).exists():
                    related_products = Product.objects.active().order_by(
                        '-sold'
                    ).filter(category=category)

                else:
                    categories = Category.objects.active().filter(parent=category)
                    filtered_categories = [category]

                    for cat in categories:
                        filtered_categories.append(cat)

                    filtered_categories = tuple(filtered_categories)
                    related_products = Product.objects.active().order_by(
                        '-sold'
                    ).filter(category__in=filtered_categories)

            related_products = related_products.exclude(id=product_id)

            related_products = ProductSerializer(related_products, many=True)

            if len(related_products.data) > 3:
                return Response(
                    {'related_products': related_products.data[:3],
                     'message': 'related products returned successfully', 'type': "success"},
                    status=status.HTTP_200_OK)
            elif len(related_products.data) > 0:
                return Response(
                    {'related_products': related_products.data,
                     'message': 'related products returned successfully', 'type': "success"},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'message': 'No related products found', "type": "failure"},
                    status=status.HTTP_200_OK)

        else:
            return Response(
                {'message': 'No related products found', "type": "failure"},
                status=status.HTTP_200_OK)
