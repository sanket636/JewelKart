from rest_framework import (
    serializers
)

from store.models import (
    JkCategory,
    JkInventory,
    JkJewelProduct,
    JkProductVariant,
)

from store.services import (
    calculate_variant_price
)



class CategorySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = JkCategory

        fields = [

            'category_id',

            'category_name',

            'description',

            'is_active',
        ]



class ProductVariantSerializer(
    serializers.ModelSerializer
):

    metal_name = (
        serializers.CharField(
            source=
                'metal.metal_name',

            read_only=True
        )
    )


    purity = (
        serializers.CharField(
            source=
                'metal.purity',

            read_only=True
        )
    )


    final_price = (
        serializers
        .SerializerMethodField()
    )


    stock = (
        serializers
        .SerializerMethodField()
    )


    class Meta:

        model = (
            JkProductVariant
        )

        fields = [

            'variant_id',

            'variant_sku',

            'metal_name',

            'purity',

            'size',

            'weight_grams',

            'making_charge',

            'gst_percent',

            'final_price',

            'stock',
        ]


    def get_final_price(
        self,
        obj
    ):

        return (
            calculate_variant_price(
                obj
            )
        )


    def get_stock(
        self,
        obj
    ):

        inventory = (

            JkInventory.objects

            .filter(
                variant_id=
                    obj.variant_id
            )

            .first()
        )


        if not inventory:

            return 0


        return max(

            (
                inventory
                .available_quantity
                or 0
            )

            -

            (
                inventory
                .reserved_quantity
                or 0
            ),

            0
        )



class ProductSerializer(
    serializers.ModelSerializer
):

    category_name = (
        serializers.CharField(

            source=
                'category.category_name',

            read_only=True
        )
    )


    variants = (
        serializers
        .SerializerMethodField()
    )


    class Meta:

        model = (
            JkJewelProduct
        )


        fields = [

            'product_id',

            'product_name',

            'sku',

            'description',

            'design_type',

            'gender',

            'base_price',

            'product_attributes',

            'category_name',

            'variants',
        ]


    def get_variants(
        self,
        obj
    ):

        variants = (

            JkProductVariant.objects

            .filter(
                product_id=
                    obj.product_id
            )

            .select_related(
                'metal'
            )

            .order_by(
                'variant_id'
            )
        )


        return (
            ProductVariantSerializer(
                variants,
                many=True
            ).data
        )



class AddCartItemSerializer(
    serializers.Serializer
):

    variant_id = (
        serializers.IntegerField(
            min_value=1
        )
    )


    quantity = (
        serializers.IntegerField(
            min_value=1,
            default=1
        )
    )



class UpdateCartItemSerializer(
    serializers.Serializer
):

    quantity = (
        serializers.IntegerField(
            min_value=1
        )
    )



class CheckoutSerializer(
    serializers.Serializer
):

    address_id = (
        serializers.IntegerField(
            min_value=1
        )
    )


    coupon_code = (
        serializers.CharField(

            required=False,

            allow_blank=True,

            default=''
        )
    )


    payment_method = (
        serializers.ChoiceField(

            choices=[
                'COD',
                'UPI',
                'CARD'
            ],

            default='COD'
        )
    )