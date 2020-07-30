from django.conf import settings
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('match/', matching, name='match'),
    path('results/', results, name='results'),
    path('account/not_found/', not_found, name='not_found'),
    path('account/verify/', verify, name="verify"),
    path('account/verified/', verified, name='verified'),
    path('account/send_verify/', verification, name='verification'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    path('notifications/read/', read_notifications, name='read_notifications'),
    path('notification/<int:id_>/delete/',
         delete_notifications, name='delete_notifications'),
    path('get_data/<type_>/', get_data, name="get_data"),
    path('personality_test/', personality_test, name="personality_test"),
    path('personality_test/submit/', personality, name='submit_test'),
    path('personality_test/result/', test_result, name="test_result"),
    path('logout/', logout, name='logout'),
    path('api/get_couple/<int:couple_id>/', get_couple, name="get_couple"),

]
