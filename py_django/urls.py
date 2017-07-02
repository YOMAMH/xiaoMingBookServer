
from django.conf.urls import url, include
from django.contrib import admin
import blog.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include(blog.urls.urlpatterns)),
]
