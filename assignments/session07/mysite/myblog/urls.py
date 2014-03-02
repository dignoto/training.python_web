from django.conf.urls import patterns, url, include

urlpatterns = patterns('myblog.views',
    url(r'^$',
        'list_view',
        name="blog_index"),
    url(r'^posts/(?P<post_id>\d+)/$',
        'detail_view',
        name="blog_detail"),
    url(r'^ckeditor/', include('myblog.ckeditor_urls')),
)