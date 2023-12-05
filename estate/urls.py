from django.contrib import admin
from django.urls import path,include
from.import views

urlpatterns = [
    path("",views.index_page,name="index"),
    path("home_page",views.home_page,name="home_page"),
    path("login",views.admin_login,name="login"),
    path("add_property",views.add_property,name="add_property"),
    path("add_tenant",views.add_tenant,name="add_tenant"),
    path("viewprop/<int:prop_id>",views.view_prop,name="viewprop"),
    path("viewten/<int:ten_id>",views.view_ten,name="viewten"),
    path("delprop/<int:prop_id>",views.del_prop,name="delprop"),
    path("delten/<int:ten_id>",views.del_ten,name="delten"),
    path("logout",views.user_logout,name="logout"),
]