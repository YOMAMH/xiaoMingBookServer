
from django.conf.urls import url, include
from django.contrib import admin

import blog.urls
import stacks_all.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include(blog.urls.urlpatterns)),
    url(r'^stacks/', include(stacks_all.urls.urlpatterns)),
]
