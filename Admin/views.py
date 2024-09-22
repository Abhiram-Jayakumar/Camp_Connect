from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from Admin.models import Complaint
from Camp.models import Camp, CampPackage
from User.models import Booking, User

# Create your views here.

def Admin_home(request):
    return render(request,'Admin/Admin_home.html')

#///////////////////////////////////////////////////////////////////////////////////
def view_registered_Camp(request):
    registered_camp = Camp.objects.filter(vstatus=0)
    return render(request, 'Admin/view_registered_Camp.html', {'registered_camp': registered_camp})


def handle_camp_registration(request, camp_id, action):
    camp = get_object_or_404(Camp, pk=camp_id)

    if action == 'accept':
        camp.vstatus = 1  
    elif action == 'reject':
        camp.vstatus = -1 
    else:
        return redirect('Admin:view_registered_Camp')

    camp.save()
    return redirect('Admin:view_registered_Camp')



#////////////////////////////////////////////////////////////////////////////////


def complaint_list(request):
    complaints = Complaint.objects.all()
    return render(request, 'Admin/complaint_list.html', {'complaints': complaints})

def resolve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.resolved = True
    complaint.save()
    messages.success(request, "Complaint marked as resolved.")
    return redirect('Admin:complaint_list')


#/////////////////////////////////////////////////////////////////////////////////////////////////////

def Graph(request):
    package_names = []
    booking_counts = []

    packages = CampPackage.objects.all()
    for package in packages:
        package_names.append(package.package_name)
        booking_count = Booking.objects.filter(package=package).count()
        booking_counts.append(booking_count)

    return render(request, 'Admin/Graph.html', {
        'package_names': package_names,
        'booking_counts': booking_counts,
    })