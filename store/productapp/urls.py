from django.urls import path
from productapp import views
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


app_name = 'productapp'

urlpatterns = [
	path("",views.register,name="signup"),
	path("login/",views.login,name="login"),
	path("hello/",views.hello,name="hello"),
	path("logout/",views.logout,name="logout"),
	path("add/",views.add_product,name="add"),
	path("search/",views.search_product,name="search"),
	path("view/",views.view_product,name="view"),
	path("view_all/",views.view_all,name="view_all"),
	path("delete/<pid>",views.delete_product,name="delete"),
	path("update/<pid>",views.update_product,name="update"),
	path("search_by_name/",views.search_by_name,name="search_by_name")
 
 ]