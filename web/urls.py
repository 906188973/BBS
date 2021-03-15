from django.urls import path, re_path
from .views import account, home, bbs
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home.home, name='home'),

    path('register/', account.register, name='register'),
    path('login/', account.login, name='login'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('logout/', account.logout, name='logout'),
    path('send/sms', account.send_sms, name='send_sms'),
    path('image/code/', account.image_code, name='image_code'),
    path('account/', account.account, name='account'),
    path('headupload/', account.headupload, name='headupload'),
    re_path(r'^other/(?P<id>\d+)/$', account.other, name='other'),

    path('create_forum/', bbs.create_forum, name='create_forum'),
    re_path(r'^forum/(?P<forum_id>\d+)/$', bbs.fourm, name='forum'),
    re_path(r'^topic/(?P<topic_id>\d+)/$', bbs.topic, name='topic'),
    path('update_comment/', bbs.update_comment, name='update_comment'),
    re_path(r'^topic_del/(?P<id>\d+)/$', bbs.topic_del, name='topic_del'),
    re_path(r'^floor_del/(?P<id>\d+)/$', bbs.floor_del, name='floor_del'),
    re_path(r'^comment_del/(?P<id>\d+)/$', bbs.comment_del, name='comment_del'),
    re_path(r'^concerned/(?P<id>\d+)/$', bbs.concerned, name='concerned'),
    re_path(r'^unconcerned/(?P<id>\d+)/$', bbs.unconcerned, name='unconcerned'),
    re_path(r'^collect/(?P<id>\d+)/$', bbs.collect, name='collect'),
    re_path(r'^uncollect/(?P<id>\d+)/$', bbs.uncollect, name='uncollect'),
    re_path(r'^change_power/(?P<id>\d+)/$', bbs.change_power, name='change_power'),
    re_path(r'^moderator/(?P<id>\d+)/$', bbs.moderator, name='moderator'),
]