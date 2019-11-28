"""Reckunique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Reckunique import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns,static
from App import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('addproduct/', views.addProduct),
    path('addcategory/', views.addCategory),
    path('shop/<str:cn>/',views.Shop,name='shop'),
    path('shop2/<str:si>/',views.Shop2),
    path('productdetails/<str:num>/', views.ProductDetails,name='productdetail' ),
    path('productdetails2/<str:num>/<str:s>/', views.ProductDetails2,name='productdetail2'),
    path('register/', views.register,name='register'),
    path('signup/', views.SignUp),
    path('logout/',views.logOut),
    path('adminpage/',views.AdminPage,name="adminpage"),
    path('sizeavailable/<str:num>/', views.Sizeavi),
    path('sizeadd/<str:num>/', views.SizeAdd),
    path('delete/<str:num>/',views.DeleteProduct,name='deleteproduct'),
    path('deletesi/<str:num>/',views.DeleteProduct2,name='deleteproduct'),
    path('delete2/<str:num>/',views.DeleteAddress,name='deleteaddress'),
    path('edit/<str:num>/',views.editProduct,name='edit'),
    path('cart/',views.CartDetails,name='cart'),
    path('orderplaced/<str:num>/',views.OrderPlaced,name='cart'),
    path('selectaddress/',views.SelectAddress,name='cart'),
    path('cartdelete/<str:num>/',views.CartDelete),
    path('cartedit1/<str:num>/',views.CartEdit1),
    path('cartedit/<str:num>/',views.CartEdit),
    path('checkout/<str:num>/',views.CheckoutForm,name='checkout'),
    path('addaddress/',views.AddAddress),
    path('addaddress2/',views.AddAddress2),
    path('pastorder/',views.PastOrders),
    path('Previousorders/',views.PastOrders2),
    path('cancelorder/<int:num>/',views.Cancelorder),
    path('cancelorder/',views.CancelOrderAdmin,name='cart'),
    path('about/',views.About,name = 'about'),
    path('orderadmin/',views.OrderAdmin),
    path('deletecart/',views.deletecart),
    path('deleteshop/',views.deleteshop),
    path('deleteabout/',views.deleteabout),
    path('deletelogout/',views.deletelogout),
    path('deletepastorder/',views.deletepastorder),
    path('deleteadminpage/',views.deleteadminpage),
    path('deletePreviousorders/',views.deletePreviousorders),
    path('dispatchedorder/<int:num>/',views.DispatchedOrder),
    path('homedelete/',views.homedelete),
#    path('handlerequest/',views.handlerequest,name='HandleRequest'),
    path('returnorder/<int:num>/',views.Returnorder),
    path('returnorder/',views.ReturnOrderAdmin),
    path('cancelreturn/<int:num>/',views.CancelReturn),
    path('confirmreturn/<int:num>/',views.ConfirmReturn),
    path('deletecancel/<int:num>/',views.Deletecancel),

]



urlpatterns=urlpatterns+staticfiles_urlpatterns()
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)