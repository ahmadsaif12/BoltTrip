from drf_spectacular.utils import extend_schema, extend_schema_view


story_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Content Stories"]),
    retrieve=extend_schema(tags=["Content Stories"]),
    create=extend_schema(tags=["Content Stories"]),
    partial_update=extend_schema(tags=["Content Stories"]),
    destroy=extend_schema(tags=["Content Stories"]),
)

story_featured_schema = extend_schema(tags=["Content Stories"])

content_category_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Content Categories"]),
    retrieve=extend_schema(tags=["Content Categories"]),
)

testimonial_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Testimonials"]),
    retrieve=extend_schema(tags=["Testimonials"]),
)

testimonial_featured_schema = extend_schema(tags=["Testimonials"])

faq_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Content FAQ"]),
    retrieve=extend_schema(tags=["Content FAQ"]),
)

promo_banner_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Promo Banners"]),
    retrieve=extend_schema(tags=["Promo Banners"]),
)

newsletter_block_viewset_schema = extend_schema_view(
    list=extend_schema(tags=["Newsletter Blocks"]),
    retrieve=extend_schema(tags=["Newsletter Blocks"]),
)
