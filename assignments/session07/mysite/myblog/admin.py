from django.contrib import admin
from myblog.models import Post
from myblog.models import Category


class CategoryAdmin(admin.ModelAdmin):
    # Suppress the 'post' field.
    exclude = ('posts',)

class CategoryInline(admin.TabularInline):
    # Display the many-to-many relations, and use the 'through' attribute to
    # reference the built in model that manages the many-to-many relation.
    model = Category.posts.through

class PostAdmin(admin.ModelAdmin):
   # Use 'inlines' so that we can edit the Category model from the Post page.
   inlines = [CategoryInline,]
       
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
