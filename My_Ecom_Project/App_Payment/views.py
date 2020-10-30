from django.shortcuts import render,HttpResponseRedirect,redirect

from App_Order.models import Order
from App_Payment.models import BillingAddress
from App_Payment.forms import BillingForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.urls import reverse
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket


# Create your views here.
@login_required
def checkout(request):
	saved_address=BillingAddress.objects.get_or_create(user=request.user)
	save_address=saved_address[0]
	form=BillingForm(instance=save_address)
	if request.method =="POST":
		form=BillingForm(request.POST,instance=save_address)
		if form.is_valid():
			form.save()
			form=BillingForm(instance=save_address)
			messages.info(request,"Your address has been saved")
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	order_items = order_qs[0].orderitems.all()
	order_total=order_qs[0].get_totals()
	return render(request,'App_Payment/checkout.html',context={'form':form,'order_items':order_items,'order_total':order_total,'save_address':save_address})

@login_required
def payment(request):
	saved_address=BillingAddress.objects.get_or_create(user=request.user)
	saved_address=saved_address[0]
	if not saved_address.is_fully_filled():
		messages.info(request,"please complete shipping address")
		return redirect("App_Payment:checkout")
	if not request.user.profile.is_fully_filled():
		messages.info(request, f"Please complete profile details!")
		return redirect("App_login:profile")
	store_id='mypla5f87cc1750fcc'
	API_key='mypla5f87cc1750fcc@ssl'
	mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)
	status_url = request.build_absolute_uri(reverse("App_Payment:complete"))
	print(status_url)
	mypayment.set_urls(success_url='status_url', fail_url='status_url', cancel_url='status_url', ipn_url='status_url')
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	order_items = order_qs[0].orderitems.all()
	order_items_count = order_qs[0].orderitems.count()
	order_total = order_qs[0].get_totals()
	print(order_total)
	mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='clothing', product_name='demo-product', num_of_item=2, shipping_method='YES', product_profile='None')


	current_user = request.user
	mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address_1, address2=current_user.profile.address_1, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)

	mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)

	response_data = mypayment.init_payment()
	return redirect(response_data['GatewayPageURL'])



@login_required
def complete(request):
	return render(request,'App_Payment/complete.html',context={})	