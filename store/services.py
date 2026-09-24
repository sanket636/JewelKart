from decimal import Decimal

from django.db import transaction

from django.utils import timezone

from .models import (
    JkCart,
    JkCartItem,
    JkCustomer,
    JkInventory,
    JkProductGemstone,
)


ZERO = Decimal(
    '0.00'
)


def get_current_customer(
    user
):

    if not user.is_authenticated:

        return None


    if not user.email:

        return None


    return (
        JkCustomer.objects
        .filter(
            email__iexact=
                user.email
        )
        .first()
    )
    
    def calculate_variant_price(
    variant
):

     metal_rate = (
        variant
        .metal
        .rate_per_gram
        or ZERO
    )


    weight = (
        variant.weight_grams
        or ZERO
    )


    metal_cost = (
        weight
        *
        metal_rate
    )


    making_charge = (
        variant.making_charge
        or ZERO
    )


    gemstone_cost = ZERO


    links = (

        JkProductGemstone.objects

        .filter(
            product_id=
                variant.product_id
        )

        .select_related(
            'gemstone'
        )
    )


    for link in links:

        price_per_carat = (

            link
            .gemstone
            .price_per_carat

            or ZERO
        )


        gemstone_cost += (

            link.carat_weight

            *

            link.quantity

            *

            price_per_carat
        )


    subtotal = (

        metal_cost
        +
        making_charge
        +
        gemstone_cost
    )


    gst_percent = (
        variant.gst_percent
        or ZERO
    )


    gst_amount = (

        subtotal

        *

        gst_percent

        /

        Decimal('100')
    )


    final_price = (

        subtotal
        +
        gst_amount
    )


    return (
        final_price.quantize(
            Decimal('0.01')
        )
    )