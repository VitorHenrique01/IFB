from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path('', include('tarefas.urls')),  # app tarefas
    # opcional: redireciona index para lista
    path('', RedirectView.as_view(pattern_name='lista_tarefas', permanent=False)),
]
