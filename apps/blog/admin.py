from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import BlogCategory, BlogTag, BlogPost, BlogComment


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at', 'post_count')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Status', {
            'fields': ('is_active', 'post_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'author', 'status_display', 'is_featured',
        'view_count', 'published_at', 'created_at'
    )
    list_filter = ('is_published', 'is_featured', 'category', 'published_at', 'created_at')
    search_fields = ('title', 'excerpt', 'content', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured',)
    readonly_fields = ('view_count', 'created_at', 'updated_at', 'reading_time')
    filter_horizontal = ('tags',)
    date_hierarchy = 'published_at'
    actions = ['publish_posts', 'unpublish_posts', 'mark_as_featured', 'unmark_as_featured']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
        ('Statistics', {
            'fields': ('view_count', 'reading_time'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_display(self, obj):
        if obj.is_published:
            return mark_safe('<span style="color: green; font-weight: bold;"><i class="fas fa-check-circle"></i> Published</span>')
        return mark_safe('<span style="color: orange;"><i class="far fa-circle"></i> Draft</span>')
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'is_published'
    
    def save_model(self, request, obj, form, change):
        # Set author to current user if not set
        if not obj.author:
            obj.author = request.user
        
        # Set published_at when publishing
        if obj.is_published and not obj.published_at:
            obj.published_at = timezone.now()
        
        super().save_model(request, obj, form, change)
    
    def publish_posts(self, request, queryset):
        now = timezone.now()
        for post in queryset:
            post.is_published = True
            if not post.published_at:
                post.published_at = now
            post.save()
        self.message_user(request, f'{queryset.count()} posts published.')
    publish_posts.short_description = 'Publish selected posts'
    
    def unpublish_posts(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} posts unpublished.')
    unpublish_posts.short_description = 'Unpublish selected posts'
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} posts marked as featured.')
    mark_as_featured.short_description = 'Mark as featured'
    
    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} posts unmarked as featured.')
    unmark_as_featured.short_description = 'Unmark as featured'


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('author_display', 'post', 'comment_preview', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('comment', 'name', 'email', 'user__username', 'post__title')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_comments', 'unapprove_comments']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'user', 'name', 'email', 'comment')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'parent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def author_display(self, obj):
        return obj.author_name
    author_display.short_description = 'Author'
    
    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Comment'
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments unapproved.')
    unapprove_comments.short_description = 'Unapprove selected comments'
