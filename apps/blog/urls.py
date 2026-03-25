from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, BlogCategoryViewSet, BlogTagViewSet, BlogCommentViewSet

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='blogpost')
router.register(r'categories', BlogCategoryViewSet, basename='blogcategory')
router.register(r'tags', BlogTagViewSet, basename='blogtag')
router.register(r'comments', BlogCommentViewSet, basename='blogcomment')

urlpatterns = [
    path('', include(router.urls)),
]
