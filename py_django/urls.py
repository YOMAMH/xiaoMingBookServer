
from django.conf.urls import url, include
from django.contrib import admin
import blog.urls
import stacks.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include(blog.urls.urlpatterns)),
    url(r'^stacks/', include(stacks.urls.urlpatterns)),
]
