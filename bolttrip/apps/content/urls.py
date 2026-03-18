from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import (
    ContentCategoryViewSet,
    FAQViewSet,
    NewsletterBlockViewSet,
    PromoBannerViewSet,
    StoryViewSet,
    TestimonialViewSet,
)

router = SimpleRouter()
router.register(r"stories", StoryViewSet, basename="content-stories")
router.register(r"categories", ContentCategoryViewSet, basename="content-categories")
router.register(r"testimonials", TestimonialViewSet, basename="content-testimonials")
router.register(r"faqs", FAQViewSet, basename="content-faqs")
router.register(r"banners", PromoBannerViewSet, basename="content-banners")
router.register(r"newsletter-blocks", NewsletterBlockViewSet, basename="content-newsletters")

urlpatterns = [
    path("", include(router.urls)),
]
