from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from apps.product.models import Product, ProductDiscount
from apps.product.serializers import ProductSerializer
from apps.category.models import Category
from django.db.models import Q


class ListProductsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        sort_by = request.query_params.get('sort_by')

        if not (sort_by == 'created' or sort_by == 'price' or sort_by == 'sold' or sort_by == 'name'):
            sort_by = 'created_at'

        order = request.query_params.get('order')
        limit = request.query_params.get('limit')

        if not limit:
            limit = 12

        try:
            limit = int(limit)
        except Exception as e:
            return Response(
                {'message': 'Limit must be an integer', 'type': 'failure'},
                status=status.HTTP_404_NOT_FOUND)

        if limit <= 0:
            limit = 12

        if order == 'desc':
            sort_by = '-' + sort_by
            products = Product.objects.active().order_by(sort_by).all()[:int(limit)]
        elif order == 'asc':
            products = Product.objects.active().order_by(sort_by).all()[:int(limit)]
        else:
            products = Product.objects.active().order_by(sort_by).all()

        products = ProductSerializer(products, many=True)

        products_data = []


        for product in products.data:

            try:
                discount = ProductDiscount.objects.get(product=product['id'])

                product['discount_type'] = discount.type
                product['discount_value'] = discount.value

                products_data.append(product)
            except Exception as e:

                product['discount_type'] = None
                product['discount_value'] = None

                products_data.append(product)

        if products:
            return Response({'products': products_data,
                             'message': 'products listed successfully',
                             'type': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'No products to list', 'type': 'failure'},
                status=status.HTTP_404_NOT_FOUND)


class ProductDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pid):
        try:
            product_id = int(pid)
        except Exception as e:
            return Response(
                {'message': 'Product ID must be an integer', 'type': 'failure'},
                status=status.HTTP_404_NOT_FOUND)

        if Product.objects.active().filter(id=product_id).exists():
            product = Product.objects.active().get(id=product_id)
            product = ProductSerializer(product)

            product_data = product.data

            try:
                discount = ProductDiscount.objects.get(product=product_id)

                product_data['discount_type'] = discount.type
                product_data['discount_value'] = discount.value

            except Exception as e:

                product_data['discount_type'] = None
                product_data['discount_value'] = None

            return Response({'product': product_data,
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

        if len(search) == 0:
            search_results = Product.objects.active().order_by('-created_at').all()
        else:
            search_results = Product.objects.active().filter(
                Q(description__icontains=search) | Q(name__icontains=search)
            )

        if category_id == 0:

            search_results = ProductSerializer(search_results, many=True)
            return Response(
                {'search_products': search_results.data,
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

        products_data = []

        for product in search_results.data:

            try:
                discount = ProductDiscount.objects.get(product=product['id'])

                product['discount_type'] = discount.type
                product['discount_value'] = discount.value

                products_data.append(product)
            except Exception as e:

                product['discount_type'] = None
                product['discount_value'] = None

                products_data.append(product)

        if len(products_data) == 0:
            return Response({'search_products': products_data,
                             'message': 'no product were found', 'type': 'failure'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({'search_products': products_data,
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

        product_results_data = []

        for product in product_results.data:

            try:
                discount = ProductDiscount.objects.get(product=product['id'])

                product['discount_type'] = discount.type
                product['discount_value'] = discount.value

                product_results_data.append(product)
            except Exception as e:

                product['discount_type'] = None
                product['discount_value'] = None

                product_results_data.append(product)

        if len(product_results_data) > 0:
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

            related_products_data = []

            for product in related_products.data:

                try:
                    discount = ProductDiscount.objects.get(product=product['id'])

                    product['discount_type'] = discount.type
                    product['discount_value'] = discount.value

                    related_products_data.append(product)
                except Exception as e:

                    product['discount_type'] = None
                    product['discount_value'] = None

                    related_products_data.append(product)

            if len(related_products_data) > 3:
                return Response(
                    {'related_products': related_products.data[:3],
                     'message': 'related products returned successfully', 'type': "success"},
                    status=status.HTTP_200_OK)
            elif len(related_products_data) > 0:
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
