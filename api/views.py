from rest_framework import (
    filters,
    permissions,
    viewsets
)

from store.models import (
    JkCategory,
    JkJewelProduct,
)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
)



class CategoryViewSet(
    viewsets.ReadOnlyModelViewSet
):

    queryset = (

        JkCategory.objects

        .filter(
            is_active=True
        )

        .order_by(
            'category_name'
        )
    )


    serializer_class = (
        CategorySerializer
    )


    permission_classes = [
        permissions.AllowAny
    ]



class ProductViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = (
        ProductSerializer
    )


    permission_classes = [
        permissions.AllowAny
    ]


    filter_backends = [

        filters.SearchFilter,

        filters.OrderingFilter,
    ]


    search_fields = [

        'product_name',

        'sku',

        'description',

        'category__category_name',
    ]


    ordering_fields = [

        'product_name',

        'base_price',

        'created_at',
    ]


    def get_queryset(
        self
    ):

        return (

            JkJewelProduct.objects

            .filter(
                is_active=True
            )

            .select_related(
                'category'
            )

            .order_by(
                'product_id'
            )
        )
from django.urls import (
    include,
    path
)

from rest_framework.routers import (
    DefaultRouter
)

from .views import (
    CategoryViewSet,
    ProductViewSet,
)


router = DefaultRouter()


router.register(

    'categories',

    CategoryViewSet,

    basename='category'
)


router.register(

    'products',

    ProductViewSet,

    basename='product'
)


urlpatterns = [

    path(
        '',
        include(
            router.urls
        )
    ),
]