from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from .views import NoteViewSet, UserViewSet, filter_note

app_name = 'api'

router = DefaultRouter(trailing_slash=False)
router.register('notes', NoteViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('notes/filter/<str:name>', filter_note, name='filter_note'),
]
