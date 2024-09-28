from importlib.resources import Package
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from Admin.models import Admintable, Complaint
from Camp.models import Camp, CampFacility, CampImage, CampPackage, CampProfile
from User.models import Booking, Feedback, Payment, User




# Create your views here.

def Index(request):
    return render(request,'User/Index.html')

#/////////////////////////////////////////////////////////////////////////////////////////////////////////

def User_home(request):
    return render(request,'User/User_home.html')


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////

def User_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'User:User_Reg.html')

        if User.objects.filter(id_number=id_number).exists():
            messages.error(request, "ID number already registered.")
            return render(request, 'User/User_Reg.html')

        user = User(name=name, email=email, phone_number=phone_number,
                    address=address, id_number=id_number, password=password)
        user.save()

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('User:Index')

    return render(request, 'User/User_Reg.html')

#///////////////////////////////////////////////////////////////////////////////////////////////////

def Login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        Clogin=Camp.objects.filter(email=email,password=password,vstatus=True).count()
        Ulogin=User.objects.filter(email=email,password=password).count()
        Alogin=Admintable.objects.filter(email=email,password=password).count()


        if Clogin > 0:
            Cadmin=Camp.objects.get(email=email,password=password,vstatus=1)
            request.session['Cid']=Cadmin.id
            return redirect('Camp:Camp_home')
        elif Ulogin > 0:
            Uadmin=User.objects.get(email=email,password=password)
            request.session['Uid']=Uadmin.id
            return redirect('User:User_home')
        elif Alogin > 0:
            Aadmin=Admintable.objects.get(email=email,password=password)
            request.session['aid']=Aadmin.id
            return redirect('Admin:Admin_home')
        
        else:
            error="Invalid Credentials!!"
            return render(request,"User/Login.html",{'ERR':error})
    else:
        return render(request, "User/Login.html")
    


#////////////////////////////////////////////////////////////////////////////////////////////////////////////
def view_Single_package(request, package_id):
    package = get_object_or_404(CampPackage, id=package_id)
    camp_profile = get_object_or_404(CampProfile, camp=package.camp)
    camp_provider_name = package.camp.camp_provider_name
    
    feedbacks = Feedback.objects.filter(camp=package.camp).order_by('-created_at')
    
    context = {
        'package': package,
        'camp_profile': camp_profile,
        'camp_provider_name': camp_provider_name,
        'feedbacks': feedbacks,
        'camp': package.camp
    }
    
    return render(request, 'User/View_Single_package.html', context)



def view_all_packages(request):
    packages = CampPackage.objects.all()
    return render(request, 'User/View_all_packages.html', {'packages': packages})

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def book_package(request, package_id):
    package = get_object_or_404(CampPackage, id=package_id)
    if request.method == "POST":
        number_of_persons = int(request.POST.get('number_of_persons'))
        facility_ids = request.POST.getlist('facilities')

        booking = Booking.objects.create(
            user=User.objects.get(id=request.session.get('Uid')),
            package=package,
            number_of_persons=number_of_persons
        )

        selected_facilities = CampFacility.objects.filter(id__in=facility_ids)
        booking.facilities.set(selected_facilities)

        messages.success(request, "Booking successful!")
        return redirect('User:view_all_packages')

    return render(request, 'User/Book_package.html', {'package': package})


#////////////////////////////////////////////////////////////////////////////////////////////////

def view_bookings(request):
    user = User.objects.get(id=request.session.get('Uid'))
    bookings = user.bookings.all() 
    return render(request, 'User/View_bookings.html', {'bookings': bookings})

#/////////////////////////////////////////////////////////////////////////////////////////////////////

def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    amount = booking.total_price
    return render(request, 'User/payment_page.html', {'booking': booking, 'amount': amount})

def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if not hasattr(booking, 'payment'):
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            payment_status='Completed'
        )
    else:
        payment = booking.payment
        payment.payment_status = 'Completed'
        payment.save()

    return redirect('User:view_bookings')

#//////////////////////////////////////////////////////////////////////////////////////////////////


def submit_complaint(request):
    if request.method == 'POST':
        complainant_type = request.POST.get('complainant_type')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        complainant_id = None
        if complainant_type == 'User':
            user = User.objects.get(id=request.session.get('Uid'))
            complainant_id = user.id
        elif complainant_type == 'Camp':
            camp = Camp.objects.get(id=request.session.get('Cid'))
            complainant_id = camp.id

        Complaint.objects.create(
            complainant_type=complainant_type,
            complainant_id=complainant_id,
            subject=subject,
            message=message
        )
        return redirect('User:submit_complaint')

    return render(request, 'User/submit_complaint.html')


#//////////////////////////////////////////////////////////////////////////////////////////////////////////
from django.http import HttpResponseForbidden

def view_profile(request):
    user_id = request.session.get('Uid')
    if not user_id:
        return HttpResponseForbidden("You are not logged in.")
    
    user = User.objects.filter(id=user_id).first()
    if not user:
        return HttpResponseForbidden("User not found.")

    return render(request, 'User/user_profile.html', {'user': user})


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def update_details(request):
    user_id = request.session.get('Uid')
    if not user_id:
        return HttpResponseForbidden("You are not logged in.")
    
    user = User.objects.filter(id=user_id).first()
    if not user:
        return HttpResponseForbidden("User not found.")
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        id_number = request.POST.get('id_number')

        if name and email and phone_number and address and id_number:
            user.name = name  
            user.email = email
            user.phone_number = phone_number
            user.address = address
            user.id_number = id_number
            user.save()
           
            messages.success(request, 'Your details have been updated successfully.')
            return redirect('User:view_profile')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'User/update_details.html', {'user': user})


#///////////////////////////////////////////////////////////////////////////////////////////////////////

def update_password(request):
    user_id = request.session.get('Uid')
    if not user_id:
        return redirect('User:Index')

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('User:Index')

        if user.password != current_password:
            messages.error(request, 'Current password is incorrect')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match')
        else:
            user.password = new_password  
            user.save()
            messages.success(request, 'Password updated successfully')
            return redirect('User:view_profile')  

    return render(request, 'User/change_password.html')


#////////////////////////////////////////////////////////////////////////////

def camp_gallery(request, camp_id):
    camp = get_object_or_404(Camp, id=camp_id)
    images = CampImage.objects.filter(camp=camp)
    return render(request, 'User/camp_gallery.html', {'camp': camp, 'images': images})

#////////////////////////////////////////////////////////////////////////////////////////////////


def add_feedback(request):
    user_id = request.session.get('Uid')
    if not user_id:
        return HttpResponseForbidden("You are not logged in.")
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseForbidden("User not found.")
    
    # Retrieve all bookings for the user
    bookings = Booking.objects.filter(user=user)
    if not bookings.exists():
        return HttpResponseForbidden("No bookings found for the user.")
    
    # Retrieve the list of packages related to the user's bookings
    packages = CampPackage.objects.filter(bookings__in=bookings).distinct()

    if request.method == 'POST':
        package_id = request.POST.get('package')
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        if not package_id or not comment or not rating:
            return render(request, 'User/add_feedback.html', {
                'packages': packages,
                'error': 'Please fill in all fields.'
            })

        if not rating.isdigit() or not (1 <= int(rating) <= 5):
            return render(request, 'User/add_feedback.html', {
                'packages': packages,
                'error': 'Rating must be an integer between 1 and 5.'
            })
        
        # Retrieve the package object
        package = get_object_or_404(CampPackage, id=package_id)
        
        Feedback.objects.create(
            user=user,
            camp=package.camp,
            comment=comment,
            rating=int(rating)
        )
        return redirect('User:User_home')

    return render(request, 'User/add_feedback.html', {'packages': packages})