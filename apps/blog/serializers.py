from rest_framework import serializers
from .models import BlogPost, BlogCategory, BlogTag, BlogComment
from apps.users.models import User


class BlogTagSerializer(serializers.ModelSerializer):
    """Serializer for blog tags"""
    class Meta:
        model = BlogTag
        fields = ['id', 'name', 'slug']


class BlogCategorySerializer(serializers.ModelSerializer):
    """Serializer for blog categories"""
    post_count = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description', 'post_count']


class BlogAuthorSerializer(serializers.ModelSerializer):
    """Serializer for blog post author"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class BlogCommentSerializer(serializers.ModelSerializer):
    """Serializer for blog comments"""
    author_name = serializers.ReadOnlyField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogComment
        fields = [
            'id', 'post', 'user', 'name', 'email', 'comment',
            'author_name', 'is_approved', 'parent', 'replies',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['is_approved', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        """Get nested replies"""
        if obj.replies.exists():
            return BlogCommentSerializer(
                obj.replies.filter(is_approved=True),
                many=True
            ).data
        return []


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer for blog post list view"""
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    author = BlogAuthorSerializer(read_only=True)
    reading_time = serializers.ReadOnlyField()
    comment_count = serializers.SerializerMethodField()
    featured_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image', 'featured_image_url',
            'category', 'tags', 'author', 'is_featured', 'view_count',
            'reading_time', 'comment_count', 'published_at', 'created_at'
        ]
    
    def get_comment_count(self, obj):
        """Get approved comment count"""
        return obj.comments.filter(is_approved=True, parent=None).count()
    
    def get_featured_image_url(self, obj):
        """Get full URL for featured image"""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
        return None


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog post detail view"""
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    author = BlogAuthorSerializer(read_only=True)
    reading_time = serializers.ReadOnlyField()
    comments = serializers.SerializerMethodField()
    featured_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image', 'featured_image_url',
            'category', 'tags', 'author', 'meta_description', 'meta_keywords',
            'is_featured', 'view_count', 'reading_time', 'comments',
            'published_at', 'created_at', 'updated_at'
        ]
    
    def get_comments(self, obj):
        """Get approved top-level comments with replies"""
        top_level_comments = obj.comments.filter(is_approved=True, parent=None)
        return BlogCommentSerializer(top_level_comments, many=True).data
    
    def get_featured_image_url(self, obj):
        """Get full URL for featured image"""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
        return None


class BlogCommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating blog comments"""
    class Meta:
        model = BlogComment
        fields = ['post', 'name', 'email', 'comment', 'parent']
    
    def validate(self, data):
        """Validate comment data"""
        user = self.context['request'].user
        
        # If user is authenticated, use their info
        if user.is_authenticated:
            data['user'] = user
            data['name'] = user.get_full_name() or user.username
            data['email'] = user.email
        else:
            # For anonymous users, name and email are required
            if not data.get('name'):
                raise serializers.ValidationError({'name': 'Name is required for anonymous comments'})
            if not data.get('email'):
                raise serializers.ValidationError({'email': 'Email is required for anonymous comments'})
        
        return data
    
    def create(self, validated_data):
        """Create comment"""
        # Auto-approve comments from authenticated users
        if validated_data.get('user'):
            validated_data['is_approved'] = True
        
        return super().create(validated_data)
