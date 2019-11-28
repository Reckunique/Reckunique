from django.shortcuts import render
from . import forms
from django.contrib.messages import success,error
from django.shortcuts import HttpResponseRedirect
from django.db.models import Q

from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from App.models import *
from Reckunique import settings

#Paytm Payment Gateway
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
#from Paytm import checksum
#MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

def search(request,sr):
    cat = Category.objects.all()
    siz = Size.objects.all()
    data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                  size__sname='all')
    paginator = Paginator(data, 8)
    page = request.GET.get('page')
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)

    return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list})


def home(request):
    cat = Category.objects.all()
    siz = Size.objects.all()

    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr)| Q(pid__contains=sr),size__sname='all')
        datacount=data.count()
        noData = ""
        if(datacount == 0):
            noData="No Such product found"
            data=Product.objects.filter(size__sname='all')
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request,'shop.html',{"Data":data,"Cat":cat,"Siz":siz,"posts":product_list,"No":noData})

    abc = [None] * 6
    count=1019
    data = Product.objects.filter(size__sname='all')

    for i in range(6):
        abc[i]="STYLE"+str(count)
        count=count+1
    cat = Category.objects.all()
    return render(request, 'index.html', {"Data":data,"Cat":cat,"Abc":abc})



def addProduct(request):
    if(request.method=='POST'):
        data = forms.ProductForm(request.POST, request.FILES)
        if(data.is_valid()):
            data.save()
            success(request,"Product Added")
            return HttpResponseRedirect('/addproduct/')
        else:
            error(request,'Invalid Product Detail')
            return HttpResponseRedirect('/addproduct/')
    else:
        return render(request,'NewProduct.html', {'Form' : forms.ProductForm})

def addCategory(request):
    if(request.method=='POST'):
        data = forms.ProductForm(request.POST, request.FILES)
        if(data.is_valid()):
            data.save()
            success(request,"Product Added")
            return HttpResponseRedirect('/addproduct/')
        else:
            error(request,'Invalid Product Detail')
            return HttpResponseRedirect('/addproduct/')
    else:
        return render(request,'NewProduct.html', {'Form' : forms.ProductForm})




def email_send(request,email,name):
    subject = 'Thanks '+name+' for registering to our site'
    message = ' it  means a lot to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )

def dispatch_email(request,data):

    subject = 'Order Dispached'
    message = 'Dear Customer,\n       Your Product is being dispatched for our side and will reached soon.\nAt address: \n'+data.order_address.address+"\n"+data.order_address.pin
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.order_address.email,]
    send_mail( subject, message, email_from, recipient_list )

def Cancel_email(request,data):

    subject = 'Order Dispached'
    message = "Dear Customer,\n       Your Request of Product Cancelation is registered "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.order_address.email,]
    send_mail( subject, message, email_from, recipient_list )

def register(request):
    if(request.method=='POST'):
        lname=request.POST.get('usernam')
        lpward=request.POST.get('passwrd')
        user=auth.authenticate(username=lname,password=lpward)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
        else:
            error(request,"Invalid User")
    return render(request,'Login.html')

def SignUp(request):
    if(request.method=='POST'):
        unam=request.POST.get('uname')
        try:
            match = User.objects.get(username=str(unam))
            if (match):
                error(request, "Username Already Exist")

        except:
            fnam = request.POST.get('first_name')
            lnam = request.POST.get('last_name')
            mail = request.POST.get('email')
            pward = request.POST.get('pward')
            cpward = request.POST.get('cpward')
            if (pward == cpward):
                User.objects.create_user(username=str(unam),
                                         first_name=str(fnam),
                                         last_name=str(lnam),
                                         email=mail,
                                         password=pward
                                         )
                success(request, "Account is created")
                email_send(request, mail, unam)
                return HttpResponseRedirect('/register/')
            else:
                error(request, "Password and Confirm Password not Matched")
    return render(request, "Signup.html")


def Shop(request,cn):

    cat = Category.objects.all()
    siz = Size.objects.all()
    noData = ""
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr)| Q(pid__contains=sr),size__sname='all')
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.filter(size__sname='all')
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request,'shop.html',{"Data":data,"Cat":cat,"Siz":siz,"posts":product_list,"No":noData})

    if (cn == "sample"):
        data = Product.objects.filter(size__sname="all")
    else:
        data = Product.objects.filter(cat__cname=cn,size__sname="all")

    if(len(data)==0):
        noData="Product In This Category Is Not Available"
        data = Product.objects.filter(size__sname="all")
   # post = Product.objects.all()
    paginator = Paginator(data, 8)
    page = request.GET.get('page')
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)
    return render(request,"shop.html",{"Cat":cat,"Data":data,"Siz":siz,
                                       "No":noData,"posts":product_list})

def Shop2(request,si):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname='all')
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.filter(size__sname='all')
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list,"No":noData})

    noData = ""
    if (si == "sample"):
        data = Product.objects.filter(size__sname="all")
    else:
        data = Product.objects.filter(size__sname=si)
    if (len(data)==0):
        noData ="Product In This Size Is Not Available"
        data = Product.objects.filter(size__sname="all")
    paginator = Paginator(data, 8)
    page = request.GET.get('page')
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)
    return render(request,"shop.html",{"Cat":cat,"Data":data,"Siz":siz,"No":noData,"posts":product_list})

def ProductDetails(request,num):
    data = Product.objects.get(id=num)
    dat= Product.objects.filter(pid=num)
    siz= Size.objects.all()
    k=""
    avail = ""
    sicount=dat.count()
    if(sicount==1):
        avail="Out Of Stock"
    else:
        avail="In Stock"

    if (request.method == 'POST'):
        try:
            form = forms.CartForm(request.POST)

            q = request.POST['count']

            if (form.is_valid()):
                if (sicount == 1):
                    success(request,"Product is not avialabel")
                else:
                    success(request, "Please add the size ")
                k ="Please add the size"
                x= '/productdetails/'+str(num)+"/"
                return HttpResponseRedirect(x)
        except:
            error(request, "Invalid Record")
    else:
        form = forms.CartForm()
    return render(request, 'ProductDetails.html', {"Data": data,"Siz":siz,"Form":form,"Dat":dat,"K":k,"Avail":avail,"Count":sicount})

@login_required(login_url='/register/')
def ProductDetails2(request,num,s):
    dat = Product.objects.filter(pid=num)
    avail = ""
    sicount = dat.count()
    if (sicount == 1):
        avail = "Out Of Stock"
    else:
        avail = "In Stock"
    data = Product.objects.get(id=num)
    num=str(num)+"-"+str(s)
    dat = Product.objects.filter(pid=s)
    car = Cart.objects.all();
    siz = Size.objects.filter(sname=s)
    if (request.method == 'POST'):
        form = forms.CartForm(request.POST)
        q = request.POST['count']
        z=0
        if(request.user == None):

            HttpResponseRedirect('/register/')
        if (form.is_valid()):
            for x in car:

                if (data.id == x.cart_product.id):
                    x.count = x.count + 1
                    z = 1
                    x.save()
                    return HttpResponseRedirect('/cart/')
            if (z == 0):

                f = form.save(commit=False)
                f.cart_user = request.user
                f.cart_product = data
                f.count = q
                f.total = int(data.price) * float(q)
                f.save()
                return HttpResponseRedirect('/cart/')
    else:
        form = forms.CartForm()
    return render(request, 'ProductDetails.html', {"Data": data, "Siz": siz,"Dat":dat, "Form": form,"Avail":avail})
def logOut(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def addProduct(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        try:

            data = Product()

            data.pid = request.POST.get('id')
            s = request.POST.get('siz')
            st = Size.objects.get(sname="all")
            data.size = st
            data.id = request.POST.get('id')
            cn = request.POST.get('cat')
            ct = Category.objects.get(cname=cn)
            data.cat = ct
            s = request.POST.get('siz')
            st = Size.objects.get(sname="all")
            data.size = st


            data.name = request.POST.get('name')
            data.description = request.POST.get('description')
            data.basicPrice = request.POST.get('basicPrice')
            data.discount = request.POST.get('discount')

            bp = int(data.basicPrice)
            d = int(data.discount)

            data.price = int(bp - (bp * d / 100))
            data.color = request.POST.get('color')
            data.img1 = request.FILES.get('img1')
            data.img2 = request.FILES.get('img2')
            data.img3 = request.FILES.get('img3')
            data.img4 = request.FILES.get('img4')
            data.img5 = request.FILES.get('img5')
            data.img6 = request.FILES.get('img6')
            data.save()
            success(request, 'Product Inserted')
            return HttpResponseRedirect('/addproduct/')
        except:
            error(request, "Invalid Record")
    return render(request, "NewProduct.html", {"Cat": cat,"Siz": siz})

def AdminPage(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname='all')
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.filter(size__sname='all')
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list,"No":noData})

    data=Product.objects.filter(size__sname='all')
    return render(request,"AdminPanel.html",{"Data":data})

def Sizeavi(request,num):
    data=Product.objects.filter(pid=num)
    return render(request,"AvailableSizes.html",{"Data":data})

def addCategory(request):
    if (request.method == 'POST'):
        try:

            data = Category()
            data.cname= request.POST.get('name')
            data.save()
            success(request, 'Product Inserted')
            return HttpResponseRedirect('/addcategory/')
        except:
            error(request, "Invalid Record")
    return render(request, "NewCategory.html")


def SizeAdd(request,num):
    data = Product.objects.get(id=num)
    siz = Size.objects.all()
    cat = Category.objects.all()

    if (request.method == 'POST'):
        try:

            s = request.POST.get('size')
            st = Size.objects.get(sname=s)
            data.size = st

            data.id=str(request.POST.get('id'))+"_"+str(st)
            data.name = request.POST.get('name')
            data.description = request.POST.get('description')
            data.basicPrice = request.POST.get('basicPrice')
            data.discount = request.POST.get('discount')

            bp = int(data.basicPrice)
            d = int(data.discount)

            data.price = bp - bp * d / 100
            data.color = request.POST.get('color')
            data.save()
            success(request, 'Size Is Added')
            data = Product.objects.get(id=num)
        except:
            error(request, "Invalid Record")
    return render(request, "AddSizes.html", {"Data": data,"Siz":siz})

def editProduct(request,num):
    data=Product.objects.get(id=num)
    cat=Category.objects.all()
    if (request.method == 'POST'):
        try:

            data.name = request.POST.get('name')
            data.description = request.POST.get('description')
            data.basicPrice = request.POST.get('basicPrice')
            data.discount = request.POST.get('discount')
            bp = int(data.basicPrice)
            d = int(data.discount)

            data.price = bp - bp * d / 100
            data.color = request.POST.get('color')
            data.save()
            success(request, 'Product Edited')
            data = Product.objects.get(id=num)
        except:
            error(request, "Invalid Record")
    return render(request,"Edit.html",{"Data":data})

def DeleteProduct(request,num):
    data=Product.objects.filter(pid=num)
    for i in data:
        i.delete()
    return HttpResponseRedirect("/adminpage/")
def DeleteProduct2(request,num):
    data=Product.objects.filter(id=num)
    for i in data:
        i.delete()
    return HttpResponseRedirect("/adminpage/")
def DeleteAddress(request,num):
    adata=Checkout.objects.get(checkid=num)
    adata.delete()
    adata = Checkout.objects.filter(checkout_user=request.user)
    if (len(adata) == 0):
        return HttpResponseRedirect('/addaddress/')
    return render(request, "SelectAddress.html", {"Data": adata})


@login_required(login_url='/register/')
def CartDetails(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname='all')
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.filter(size__sname='all')
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list})

    data=Cart.objects.filter(cart_user=request.user)
    coun=data.count();
    t=0
    for i in data:
        t=t+i.cart_product.price*i.count
    return render(request,"Cart.html",{"Data":data,"Total":t,"length":coun})

@login_required(login_url='/register/')
def PastOrders(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname='all')
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.filter(size__sname='all')
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list,"No":noData})

    data=Order.objects.filter(order_user=request.user)
    cdata=CancelOrder.objects.filter(order_user=request.user)
    datacount = cdata.count()
    return render(request,"placedorder.html",{"Data":data,"CData":cdata,"datacount":datacount})

@login_required(login_url='/register/')
def PastOrders2(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname='all')
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.filter(size__sname='all')
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list,"No":noData})
    rdata=ReturnOrder.objects.filter(order_user=request.user)
    length=rdata.count()
    data=PreviousOrder.objects.filter(order_user=request.user)
    return render(request,"PreviousOrder.html",{"Data":data,"RData":rdata,"length":length})

def CartDelete(request,num):
    data=Cart.objects.get(cart_product__id=num)
    data.delete()
    return HttpResponseRedirect('/cart/')

def CartEdit1(request,num):
    data=Cart.objects.get(cart_product__id=num)
    data.count= int(data.count)-1
    if(int(data.count)==0):
        data.count=1
    data.save()
    return HttpResponseRedirect("/cart/")

def OrderPlaced(request,num):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname='all')
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.filter(size__sname='all')
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list,"No":noData})

    data = Cart.objects.filter(cart_user=request.user)
    adata = Checkout.objects.filter(checkid=num)
    t=0
    for i in data:
        t = t + i.cart_product.price * i.count

    return render(request,"OrderPlaced.html",{"Data":data,"Adata":adata,"total":t})
def homedelete(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/')
def deletecart(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/cart/')
def deleteabout(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/about/')
def deleteshop(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/shop/sample/')

def deletePreviousorders(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/Previousorders/')

def deletepastorder(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/pastorder/')
def deletelogout(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/logout/')
def deleteadminpage(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/adminpage/')

def OrderPlaced2(request):
    data=PreviousOrder.objects.filter(order_user=request.user)
    return render(request,"OrderPlaced.html",{"Data":data})

def CartEdit(request,num):
    data=Cart.objects.get(cart_product__id=num)
    data.count= int(data.count)+1
    data.save()
    return HttpResponseRedirect("/cart/")

@login_required(login_url='/register/')
def AddAddress(request):
    i=None
    x=""
    if (request.method == 'POST'):
         try:
            check = Checkout()
            check.checkid= request.user
            x=request.user
            check.chname = request.POST.get('name')
            check.checkout_user = request.user
            check.mobile = request.POST.get('mobile')
            check.email = request.POST.get('email')
            check.state = request.POST.get('state')
            check.city = request.POST.get('city')
            check.address = request.POST.get('address')
            check.pin = request.POST.get('pin')
            check.save()
            y = "/checkout/" + str(x) + "/"
            return HttpResponseRedirect(y)
         except:
            error(request, "Invalid Record")
    return render(request, "AddAddress.html")

@login_required(login_url='/register/')
def AddAddress2(request):
    i=None
    nam=None
    x=""
    data = Checkout.objects.filter(checkout_user=request.user)
    for i in data:
        nam=i.checkid
    x=int(len(nam))
    if (request.method == 'POST'):
        try:
            check = Checkout()
            names=str(request.user)
            y = x-int(len(names))
            y=y+1
            subname=names[:y]
            check.checkid= names+str(subname)
            x= check.checkid
            check.chname = request.POST.get('name')
            check.checkout_user = request.user
            check.mobile = request.POST.get('mobile')
            check.email = request.POST.get('email')
            check.state = request.POST.get('state')
            check.city = request.POST.get('city')
            check.address = request.POST.get('address')
            check.pin = request.POST.get('pin')
            check.save()
            success(request, "Address is added")
            y="/checkout/"+x+"/"
            return HttpResponseRedirect(y)
        except:
            error(request, "Invalid Record")
    return render(request, "AddAddress.html")
@login_required(login_url='/register/')
def SelectAddress(request):
    adata=Checkout.objects.filter(checkout_user=request.user)
    if(len(adata)==0):
        return HttpResponseRedirect('/addaddress/')
    return render(request,"SelectAddress.html",{"Data":adata})

#MERCHANT_KEY='sample'
@login_required(login_url='/register/')
def CheckoutForm(request,num):
    data = Cart.objects.filter(cart_user=request.user)
    temp=0
    t = 0
    for i in data:
        t = t + i.cart_product.price * i.count

    adata=Checkout.objects.filter(checkid=num)
    onum = OrderNumber.objects.all()
    ordernum=0
    for i in onum:
        ordernum=int(i.ordernumber)


    if(request.method=='POST'):
        try:
            choice = request.POST.get('choice')
            if(choice=='COD'):

                for i in data:
                    ON = OrderNumber()
                    O = Order()
                    O.ordernumber = ordernum+1
                    ON.ordernumber=ordernum+1
                    ON.save()
                    O.order_user = request.user
                    d = Product.objects.get(id=i.cart_product.id)
                    O.order_product = d
                    for x in adata:
                        O.order_address = x

                    O.count = i.count
                    O.save()

                x='/orderplaced/'+num+"/"
                return HttpResponseRedirect(x)
        #    elif(choice=='PAYTM'):
                # request paytm to transfer the amount to your account after paytm by user
          #      param_dict = {
          #          'MID': 'WorldP64425807474247',
           ##         'TXN_AMOUNT': str(t),
          #          'INDUSTRY_TYPE_ID': 'Retail',
          #          'WEBSITE': 'WEBSTAGING',
          #          'CHANNEL_ID': 'WEB',
          #          'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
          #      }
            #    param_dict['CHECKSUMHASH'] = checksum.generate_checksum, param_dict,
           #     return render(request, 'paytm.html', {'param_dict': param_dict})

            # elif\
            #         (choice=='Paypal'):
            #     success(request, "pay with paypal")
            #     return HttpResponseRedirect('/payment/process/')
        except:
            error(request, "Invalid Record")

    return render(request,"Checkout.html",{"Total":t,"Data":adata})

def About(request):
    return render(request,'About.html')

def OrderAdmin(request):
    count=len(PreviousOrder.objects.all())
    data=Order.objects.all()
    return render(request,'orderadmin.html',{"Data":data})

def CancelOrderAdmin(request):
    data=CancelOrder.objects.all()
    return render(request,'canceladmin.html',{"Data":data})

def DispatchedOrder(request,num):

    data = Order.objects.get(ordernumber=num)
    try:
        p = PreviousOrder()
        p.ordernumber = int(data.ordernumber)
        p.order_user = data.order_user
        p.order_product = data.order_product
        p.count=data.count
        p.order_address = data.order_address
        p.save()
        dispatch_email(request,data)

    except:
        error(request, "Invalid Record")
    data.delete()
    data=Order.objects.all()
    return render(request,'orderadmin.html',{"Data":data})

def Cancelorder(request,num):

    data = Order.objects.get(ordernumber=num)
    try:
        p = CancelOrder()
        p.ordernumber = int(data.ordernumber)
        p.order_user = data.order_user
        p.order_product = data.order_product
        p.count=data.count
        p.order_address = data.order_address
        p.save()
        Cancel_email(request,data)

    except:
        error(request, "Invalid Record")
    data.delete()
    data=Order.objects.filter(order_user=request.user)
    return HttpResponseRedirect("/pastorder/")

#@csrf_exempt
#def handlerequest(request):
#    return HttpResponse('payment completed')
##    pass

def Returnorder(request,num):

    data = PreviousOrder.objects.get(ordernumber=num)
    try:
        p = ReturnOrder()
        p.ordernumber = (data.ordernumber)
        p.order_user = data.order_user
        p.order_product = data.order_product
        p.count=data.count
        p.order_address = data.order_address
        p.save()
        Return_email(request,data)
        success(request,"Request of return is registered")
    except:
        error(request, "Invalid Record")
    data.delete()
    return HttpResponseRedirect("/Previousorders/")

def Return_email(request,data):

    subject = 'Return Request'
    message = 'Dear '+data.order_address.chname+",\n       Your Request of Product Return is registered "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.order_address.email,]
    send_mail( subject, message, email_from, recipient_list )

def ReturnOrderAdmin(request):
    data=ReturnOrder.objects.all()
    return render(request,'ReturnOrder.html',{"Data":data})

def CancelReturn(request,num):
    adata = ReturnOrder.objects.get(ordernumber=num)
    try:

        subject = 'Return Request'
        message = "Dear customer,\n       Your Request of Product Return is Decline "
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [adata.order_address.email, ]
        send_mail(subject, message, email_from, recipient_list)
    except:
        error(request,"Mail not send")
    try:
        p = PreviousOrder()
        p.ordernumber = int(adata.ordernumber)
        p.order_user = adata.order_user
        p.order_product = adata.order_product
        p.count = adata.count
        p.order_address = adata.order_address
        p.save()
        adata.delete()

    except:
        error(request, "Invalid Record")
    adata = ReturnOrder.objects.all()
    return render(request, 'ReturnOrder.html', {"Data": adata})

def ConfirmReturn(request,num):
    adata = ReturnOrder.objects.get(ordernumber=num)
    try:
        subject = 'Return Request'
        message = "Dear Customer ,\n       Your Request of Product Return is confirmed and your order will be picked soon by our executive from your delivered address "
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [adata.order_address.email, ]
        send_mail(subject, message, email_from, recipient_list)
    except:
        error(request,"Mail not sent")
    try:
        adata.delete()
    except:
        error(request, "Invalid Record")
    adata = ReturnOrder.objects.all()
    return render(request, 'ReturnOrder.html', {"Data": adata})
def Deletecancel(request,num):
    data=CancelOrder.objects.get(ordernumber=num)
    try:
        subject = 'Return Request'
        message = 'Dear ' + data.order_address.chname + ",\n       Your Request of Product Cancelation is confirmed and if you have paid for this order than the money will we returned as soon as possible "
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [data.order_address.email, ]
        send_mail(subject, message, email_from, recipient_list)
    except:
        error(request,"Mail not sent")
    try:
        data.delete()
    except:
        error(request,"Data is not deleted ")
    data = CancelOrder.objects.all()
    return render(request,'canceladmin.html',{"Data":data})
