from .views import *
from django.urls import path


urlpatterns = [
    path('new_referal/', NewReferal.as_view(), name='create_new_referal'),
    path('referal_statistic/', MyStatistic.as_view(), name='get_statistic'),
    path('get_some_data/', GetData.as_view(), name='get_some_data'),
    path('get_ded_row/', GetDed.as_view(), name='get_ded_row'),
    path('get_ded_link/', GetDedLink.as_view(), name='get_ded_link'),
]

