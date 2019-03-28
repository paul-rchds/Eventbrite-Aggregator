from django.contrib import admin
from django.urls import path, include
from api.views import EventList, EventDetail, OrganizerDetail, StatsDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('events/', EventList.as_view()),
    path('events/<int:uuid>/', EventDetail.as_view()),
    path('organizers/details/<int:uuid>/', OrganizerDetail.as_view()),
    path('stats/', StatsDetail.as_view()),
]
