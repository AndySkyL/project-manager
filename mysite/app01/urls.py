from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'^index_test/', views.index, name='index_url'),
    url(r'^login/', views.login, name='login_url'),
    url(r'^logout', views.logout,name='logout'),
    url(r'^project/$', views.project, name='project'),
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^update_project/(\d+)/$', views.update_project, name='update_project'),
    # url(r'^del_project/(\d+)/$', views.del_project, name='del_project'),
    url(r'^host_info/$', views.Host_info.as_view(),name='hostlist'),
    url(r'^add_host/$', views.Add_host.as_view(),name='add_host'),
    url(r'^edit_host/(\d+)/$', views.Edit_host.as_view(), name='edit_host'),
    url(r'^del_(hostlist|project)/(\d+)/$', views.Del.as_view(), name='delete'),

]
