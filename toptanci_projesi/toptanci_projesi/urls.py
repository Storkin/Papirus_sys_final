from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import set_language
from inventory.views import RememberMeLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
    # Özel login (oturum açık kalsın) — auth include'undan önce gelmeli
    path('login/', RememberMeLoginView.as_view(), name='login'),
    path('', include('inventory.urls')),
    path('', include('django.contrib.auth.urls')),
]