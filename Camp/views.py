from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from Admin.models import Complaint
from Camp.models import Camp, CampFacility, CampImage, CampPackage, CampProfile
from django.utils.dateparse import parse_date

from User.models import Booking, User

# Create your views here.

def Camp_home(request):
    return render(request,'Camp/Camp_home.html')

def Camp_register(request):
    if request.method == "POST":
        camp_name = request.POST.get('camp_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        camp_regno = request.POST.get('camp_regno')
        camp_provider_name = request.POST.get('camp_provider_name')
        password = request.POST.get('password')

        if Camp.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'Camp/Camp_Reg.html')

        if Camp.objects.filter(camp_regno=camp_regno).exists():
            messages.error(request, "Camp registration number already registered.")
            return render(request, 'Camp/Camp_Reg.html')

        camp = Camp(camp_name=camp_name, email=email, phone_number=phone_number,
                    camp_regno=camp_regno, camp_provider_name=camp_provider_name, password=password)
        camp.save()

        messages.success(request, "Camp registration successful.")
        return redirect('User:Index')  

    return render(request, 'Camp/Camp_Reg.html')

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def add_facility(request):
    camp_id = request.session.get('Cid')
    if not camp_id:
        messages.error(request, "Camp not logged in.")
        return redirect('User:Index')  
    camp = get_object_or_404(Camp, id=camp_id)

    if request.method == 'POST':
        facility_name = request.POST.get('facility_name')
        quantity_available = request.POST.get('quantity_available')
        price_per_item = request.POST.get('price_per_item')
        description = request.POST.get('description')

        valid_choices = dict(CampFacility.CAMP_ITEM_CHOICES).keys()
        if facility_name not in valid_choices:
            messages.error(request, "Invalid facility name selected.")
            return redirect('Camp:Camp_home')

        CampFacility.objects.create(
            facility_name=facility_name,
            quantity_available=quantity_available,
            price_per_item=price_per_item,
            description=description,
            camp=camp
        )

        messages.success(request, "Facility added successfully.")
        return redirect('Camp:Camp_home')

    context = {
        'camp': camp,
        'CAMP_ITEM_CHOICES': CampFacility.CAMP_ITEM_CHOICES,
    }
    return render(request, 'Camp/Add_Facility.html', context)


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def Add_camp_profile(request):
    camp_id = request.session.get('Cid')
    if not camp_id:
        messages.error(request, "Camp not logged in.")
        return redirect('User:Index')  
    
    camp = get_object_or_404(Camp, id=camp_id)

    context = {
        'camp': camp,
        'CAMP_TYPE_CHOICES': CampProfile.CAMP_TYPE_CHOICES,
    }
    if request.method == 'POST':
        camp_name = request.POST.get('camp_name')
        description = request.POST.get('description')
        camp_type = request.POST.get('camp_type')
        operating_hours = request.POST.get('operating_hours')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')
        address = request.POST.get('address')
        location = request.POST.get('location')
        pricing_info = request.POST.get('pricing_info')
        social_media_facebook = request.POST.get('social_media_facebook')
        social_media_twitter = request.POST.get('social_media_twitter')
        social_media_instagram = request.POST.get('social_media_instagram')

        CampProfile.objects.create(
            camp_name=camp_name,
            description=description,
            camp_type=camp_type,
            operating_hours=operating_hours,
            contact_phone=contact_phone,
            contact_email=contact_email,
            address=address,
            location=location,
            pricing_info=pricing_info,
            social_media_facebook=social_media_facebook,
            social_media_twitter=social_media_twitter,
            social_media_instagram=social_media_instagram,
            camp=camp
        )
        
       
        messages.success(request, "Camp profile added successfully.")
        return redirect('Camp:Camp_home')  
    return render(request, 'Camp/Add_camp_profile.html', context)


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def upload_images(request):
    camp_id = request.session.get('Cid')
    if not camp_id:
        messages.error(request, "Camp not logged in.")
        return redirect('User:Index') 
    
    camp = get_object_or_404(Camp, id=camp_id)

    if request.method == 'POST':
        if 'images' in request.FILES:
            images = request.FILES.getlist('images')
            for image in images:
                description = request.POST.get('description', '')
                CampImage.objects.create(
                    camp=camp,
                    image=image,
                    description=description
                )
            messages.success(request, "Images uploaded successfully.")
            return redirect('Camp:Camp_home') 

    return render(request, 'Camp/Upload_C_images.html', {'camp': camp})


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////


def add_package(request):
    camp_id = request.session.get('Cid')
    if not camp_id:
        messages.error(request, "Camp not logged in.")
        return redirect('User:Index')
    
    camp = get_object_or_404(Camp, id=camp_id)

    if request.method == 'POST':
        package_name = request.POST.get('package_name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        camp_start_date = parse_date(request.POST.get('camp_start_date'))
        camp_end_date = parse_date(request.POST.get('camp_end_date'))
        booking_start_date = parse_date(request.POST.get('booking_start_date'))
        booking_end_date = parse_date(request.POST.get('booking_end_date'))
        max_people = request.POST.get('max_people')
        facilities_ids = request.POST.getlist('facilities')  # Get list of selected facilities
        price = request.POST.get('price')
        availability = request.POST.get('availability') == 'on'
        image = request.FILES.get('image')

        # Create the package
        package = CampPackage.objects.create(
            camp=camp,
            package_name=package_name,
            description=description,
            location=location,
            camp_start_date=camp_start_date,
            camp_end_date=camp_end_date,
            booking_start_date=booking_start_date,
            booking_end_date=booking_end_date,
            max_people=max_people,
            price=price,
            availability=availability,
            images=image
        )
        
        # Set facilities for the package
        facilities = CampFacility.objects.filter(id__in=facilities_ids)
        package.facilities_provided.set(facilities)

        messages.success(request, "Package added successfully.")
        return redirect('Camp:Camp_home')

    facilities = CampFacility.objects.filter(camp=camp)
    return render(request, 'Camp/Add_package.html', {'camp': camp, 'facilities': facilities})


#/////////////////////////////////////////////////////////////////////////////////////////////

def view_package(request, package_id):
    package = get_object_or_404(CampPackage, id=package_id)
    return render(request, 'Camp/View_package.html', {'package': package})


def view_all_packages(request):
    camp_id = request.session.get('Cid')
    if not camp_id:
        messages.error(request, "Camp not logged in.")
        return redirect('User:Index')

    camp = get_object_or_404(Camp, id=camp_id)
    packages = CampPackage.objects.filter(camp=camp)
    
    return render(request, 'Camp/View_all_packages.html', {'camp': camp, 'packages': packages})


#//////////////////////////////////////////////////////////////////////////////////////////////////

def camper_view_bookings(request):
    try:
        camper = Camp.objects.get(id=request.session.get('Cid'))
    except Camp.DoesNotExist:
        # Handle the case where the camper is not found
        return render(request, 'User/error_page.html', {'message': 'Camper not found.'})
    
    packages = camper.packages.all()
    
    # Get all bookings made by users for the camper's packages
    bookings = Booking.objects.filter(package__in=packages).select_related('package', 'user', 'payment').prefetch_related('facilities')
    
    return render(request, 'Camp/camper_view_bookings.html', {'bookings': bookings})

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


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
        return redirect('Camp:submit_complaint')

    return render(request, 'Camp/submit_complaint.html')


#/////////////////////////////////////////////////////////////////////////////////////////////
from django.http import HttpResponseForbidden

def camp_profile_view(request):
    camp_id = request.session.get('Cid')
    if not camp_id:
        return HttpResponseForbidden("You are not logged in.")
    
    camp = Camp.objects.filter(id=camp_id).first()
    if not camp:
        return HttpResponseForbidden("camp not found.")    
    return render(request, 'Camp/camp_profile.html', {'camp': camp})

#////////////////////////////////////////////////////////////////////////////////////////////////////////////


def edit_camp_details_view(request, camp_id):
    camp = get_object_or_404(Camp, id=camp_id)
    
    if request.method == 'POST':
        camp.camp_name = request.POST['camp_name']
        camp.email = request.POST['email']
        camp.phone_number = request.POST['phone_number']
        camp.camp_provider_name = request.POST['camp_provider_name']
        camp.save()
        return redirect('Camp:camp_profile')
    
    return render(request, 'Camp/edit_camp_details.html', {'camp': camp})


#////////////////////////////////////////////////////////////////////////////////////////////////////////////


def change_camp_password_view(request, camp_id):
    camp = get_object_or_404(Camp, id=camp_id)
    
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if new_password == confirm_password:
            camp.password = new_password
            camp.save()
            return redirect('Camp:camp_profile')
        else:
            return render(request, 'Camp/change_camp_password.html', {'camp': camp, 'error': 'Passwords do not match.'})
    
    return render(request, 'Camp/change_camp_password.html', {'camp': camp})

#////////////////////////////////////////////////////////////////////////////////////////////////////////////

def camp_profile_update_detailed(request):
    camp_id = request.session.get('Cid')
    if not camp_id:
        return HttpResponseForbidden("You are not logged in.")
    
    camp_profile = get_object_or_404(CampProfile, camp_id=camp_id)

    if request.method == 'POST':
        camp_profile.camp_name = request.POST.get('camp_name', camp_profile.camp_name)
        camp_profile.description = request.POST.get('description', camp_profile.description)
        camp_profile.camp_type = request.POST.get('camp_type', camp_profile.camp_type)
        camp_profile.operating_hours = request.POST.get('operating_hours', camp_profile.operating_hours)
        camp_profile.contact_phone = request.POST.get('contact_phone', camp_profile.contact_phone)
        camp_profile.contact_email = request.POST.get('contact_email', camp_profile.contact_email)
        camp_profile.address = request.POST.get('address', camp_profile.address)
        camp_profile.location = request.POST.get('location', camp_profile.location)
        camp_profile.pricing_info = request.POST.get('pricing_info', camp_profile.pricing_info)
        camp_profile.social_media_facebook = request.POST.get('social_media_facebook', camp_profile.social_media_facebook)
        camp_profile.social_media_twitter = request.POST.get('social_media_twitter', camp_profile.social_media_twitter)
        camp_profile.social_media_instagram = request.POST.get('social_media_instagram', camp_profile.social_media_instagram)

        camp_profile.save()
        return redirect('Camp:camp_profile')

    return render(request, 'Camp/camp_profile_update.html', {'camp_profile': camp_profile})

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def profile_view_detailed(request):
    camp_id = request.session.get('Cid')
    if not camp_id:
        return HttpResponseForbidden("You are not logged in.")
    
    camp_profile = get_object_or_404(CampProfile, camp_id=camp_id)    
    context = {
        'camp_profile': camp_profile,
    }
    
    return render(request, 'Camp/camp_profile_detailed_view.html', context)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def edit_camp_package(request, package_id):
    camp_id = request.session.get('Cid')
    if not camp_id:
        return HttpResponseForbidden("You are not authorized to edit this package.")

    camp = get_object_or_404(Camp, id=camp_id)

    package = get_object_or_404(CampPackage, id=package_id, camp=camp)

    facilities = CampFacility.objects.all()

    if request.method == 'POST':
        package.package_name = request.POST.get('package_name')
        package.description = request.POST.get('description')
        package.location = request.POST.get('location')
        package.camp_end_date = request.POST.get('camp_end_date')
        package.booking_end_date = request.POST.get('booking_end_date')
        package.max_people = request.POST.get('max_people')
        package.price = request.POST.get('price')
        package.availability = request.POST.get('availability') == 'on'
        
        facilities = request.POST.getlist('facilities')
        package.facilities_provided.set(facilities)

        if 'image' in request.FILES:
            package.images = request.FILES['image']

        package.save()

        return redirect('Camp:view_package', package_id=package.id)

    return render(request, 'Camp/edit_package.html', {'package': package,'facilities': facilities})
