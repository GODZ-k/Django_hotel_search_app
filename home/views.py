from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import (Amenities,hotel,booking)
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate , login,logout


# Create your views here.
def home(request):

    aminities_obj=Amenities.objects.all()
    hotel_obj=hotel.objects.all() # limit of data items
    sort_by=request.GET.get('sort_by')
    search=request.GET.get('search')
    amenities=request.GET.getlist('amenities')
    Paginator_data=Paginator(hotel_obj,4)
    page_no=request.GET.get('page')
    # print(amenities)
    try:
    #   if search != None:
     if search:
       hotel_obj=hotel.objects.filter(
            Q(hotel_name__icontains=search) |
            Q(description__icontains=search) |
            Q(hotel_place__icontains=search) |
            Q(amenities__amenity_name__icontains=search) |
            Q(hotel_count__icontains=search) |
            Q(hotel_price__icontains=search)).distinct()
     # if request.GET.get('sort_by'):
     if sort_by:
         if sort_by == 'ASC':
          hotel_obj=hotel_obj.order_by("hotel_price")
         elif sort_by == 'DSC':
          hotel_obj=hotel_obj.order_by("-hotel_price")
    #  if request.GET.get('amenities'):
     if len(amenities):
        # if amenities != None:
        hotel_obj=hotel_obj.filter(amenities__amenity_name__in=amenities).distinct()

     finaldata=Paginator_data.get_page(page_no)
     totalpage=finaldata.paginator.num_pages
     totalpage_no=[n+1 for n in range(totalpage)]

    except:
        return HttpResponse("error 404")





    context={
        'aminities_obj':aminities_obj,
        # 'hotel_obj':hotel_obj,   without paginator
        'hotel_obj':finaldata,   # with paginator
        'lastpage':totalpage,
        'totalpage_no':totalpage_no,
        'sort_by':sort_by,
        'search':search,
        'amenities':amenities,
        # 'hotel_search':hotel_search
    }
    totalpage_no=[n+1 for n in range(totalpage)]
    return render(request, 'index.html',context)

def hotel_detail(request,uid):
    hotel_obj=hotel.objects.get(uid=uid)

    if request.method == 'POST':
        checkin=request.POST.get('checkin')
        checkout=request.POST.get('checkout')
        Hotel=hotel.objects.get(uid=uid)

        if not check_booking(checkin,checkout,uid,Hotel.hotel_count):
            messages.error(request,"No room Available")


        else:
         booking.objects.create(hotel=Hotel,user=request.user,start_date=checkin,end_date=checkout,booking_type='prepaid')
         messages.success(request,"Your Booking is created successfully")



    return render(request,'hotel-detail.html',{'hotel_obj':hotel_obj})


def check_booking(start_date,end_date,uid,hotel_count):
    hotel_booking=booking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid=uid
    )

    if len(hotel_booking) >= hotel_count:
        return False

    return True


def loginpage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=username)
        if not user_obj.exists():
            messages.warning(request,"user does not exist")
            return redirect('/login/')

        user_obj=authenticate(username=username, password=password)
        if not user_obj:
            messages.warning(request,"invalid password")
        else:
            login(request, user_obj)
            return redirect("/")

    return render(request, 'login.html')

def registerpage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        usernameobj=User.objects.filter(username=username)
        if usernameobj.exists():
            messages.warning(request, 'username already exists')
            return redirect("/register/")


        user=User.objects.create(
            username=username,
        )

        user.set_password(password)
        user.save()
        messages.warning(request,"account created successfully")
        return redirect("/")

    return render(request, 'register.html')


def logout_page(request):
    logout(request)
    return redirect("/")