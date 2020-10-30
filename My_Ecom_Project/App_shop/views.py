from django.shortcuts import render

from django.views.generic import ListView,DetailView


from App_shop.models import Product


from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.




class Home(ListView):
	model=Product
	template_name='App_shop/home.html'


class ProductDetail(LoginRequiredMixin,DetailView):
	model=Product
	template_name='App_shop/product_detail.html'
