from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import BlogPost, BlogCategory, BlogTag, BlogComment
from .serializers import (
    BlogPostListSerializer, BlogPostDetailSerializer,
    BlogCategorySerializer, BlogTagSerializer,
    BlogCommentSerializer, BlogCommentCreateSerializer
)


class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for blog categories
    
    list: Get all active blog categories
    retrieve: Get a single blog category by ID or slug
    """
    queryset = BlogCategory.objects.filter(is_active=True)
    serializer_class = BlogCategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        """Filter active categories"""
        return BlogCategory.objects.filter(is_active=True)


class BlogTagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for blog tags
    
    list: Get all blog tags
    retrieve: Get a single blog tag by ID or slug
    """
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for blog posts
    
    list: Get all published blog posts with filtering and search
    retrieve: Get a single blog post by ID or slug
    featured: Get featured blog posts
    popular: Get most viewed blog posts
    recent: Get recent blog posts
    by_category: Get posts by category
    by_tag: Get posts by tag
    """
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'tags', 'is_featured']
    search_fields = ['title', 'excerpt', 'content', 'meta_keywords']
    ordering_fields = ['published_at', 'view_count', 'created_at']
    ordering = ['-published_at']
    lookup_field = 'slug'
    
    def get_queryset(self):
        """Get published blog posts"""
        return BlogPost.objects.filter(
            is_published=True
        ).select_related('category', 'author').prefetch_related('tags')
    
    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Get blog post detail and increment view count"""
        instance = self.get_object()
        
        # Increment view count
        instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured blog posts"""
        featured_posts = self.get_queryset().filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most viewed blog posts"""
        popular_posts = self.get_queryset().order_by('-view_count')[:10]
        serializer = self.get_serializer(popular_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent blog posts"""
        recent_posts = self.get_queryset().order_by('-published_at')[:10]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='category/(?P<category_slug>[^/.]+)')
    def by_category(self, request, category_slug=None):
        """Get posts by category slug"""
        posts = self.get_queryset().filter(category__slug=category_slug)
        
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='tag/(?P<tag_slug>[^/.]+)')
    def by_tag(self, request, tag_slug=None):
        """Get posts by tag slug"""
        posts = self.get_queryset().filter(tags__slug=tag_slug)
        
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        """Get related blog posts based on category and tags"""
        post = self.get_object()
        
        # Get posts with same category or tags
        related_posts = self.get_queryset().filter(
            Q(category=post.category) | Q(tags__in=post.tags.all())
        ).exclude(id=post.id).distinct()[:6]
        
        serializer = self.get_serializer(related_posts, many=True)
        return Response(serializer.data)


class BlogCommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for blog comments
    
    list: Get all approved comments for a post
    create: Create a new comment (requires authentication or name/email)
    """
    serializer_class = BlogCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Get approved comments"""
        queryset = BlogComment.objects.filter(is_approved=True)
        
        # Filter by post if provided
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        # Only top-level comments (no parent)
        queryset = queryset.filter(parent=None)
        
        return queryset.select_related('user', 'post').prefetch_related('replies')
    
    def get_serializer_class(self):
        """Use different serializers for create and list"""
        if self.action == 'create':
            return BlogCommentCreateSerializer
        return BlogCommentSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new comment"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return the created comment with full details
        comment = BlogComment.objects.get(id=serializer.data['id'])
        response_serializer = BlogCommentSerializer(comment)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
