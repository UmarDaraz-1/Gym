from django.shortcuts import render, redirect
from django.db.models import Sum
from datetime import timedelta, date, datetime
from .models import Member
from .forms import MemberForm
from django.db.models import Sum
import datetime
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from .forms import PaymentForm



# Create your views here.
def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')

def service(request):
    return render(request, 'service.html')

def about(request):
    return render(request, 'about.html')

def members(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        fee_amount = request.POST.get('fee_amount')
        fee_date = request.POST.get('fee_date')
        picture = request.FILES.get('picture')
        captured_picture = request.POST.get('captured_picture')
        status = request.POST.get('status')
        
        

        member = Member(name=name, phone_number=phone_number, fee_amount=fee_amount, fee_date=fee_date, captured_picture=captured_picture, picture=picture, status=status)
        member.save()
        return redirect('dashboard') 

        

    members = Member.objects.all()
    active_members = members.filter(status='Active')
    non_active_members = members.filter(status='Non Active')
    due_members = members.filter(status='Non Active', fee_date__lte=datetime.date.today())
    
    context = {
        'active_members': active_members,
        'non_active_members': non_active_members,
        'due_members': due_members,
        
    }

    return render(request, 'members.html', context)


def update_member(request, member_id):
    member = Member.objects.get(pk=member_id)

    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.phone_number = request.POST.get('phone_number')
        member.fee_amount = request.POST.get('fee_amount')
        member.fee_date = request.POST.get('fee_date')
        member.status = request.POST.get('status')
        member.save()
        return redirect('dashboard')

    context = {
            'member': member,
        }

    return render(request, 'update_member.html', context)


def delete_member(request, member_id):
    member = Member.objects.get(pk=member_id)

    if request.method == 'POST':
        member.delete()
        return redirect('dashboard')
    
    context = {
        'member': member
    }

    return render(request, 'delete_member.html', context)


def dashboard(request):
    members = Member.objects.all()
    sorted_members_due = Member.objects.filter(status='Active', fee_date__lte=datetime.date.today() - timedelta(days=2)).order_by('fee_date')
    return render(request, 'dashboard.html', {'members': members, 'sorted_members_due': sorted_members_due})



def reports(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    revenue = None

    if start_date and end_date:
        revenue = Member.objects.filter(status='Active', fee_date__range=[start_date, end_date]).aggregate(Sum('fee_amount'))['fee_amount__sum']

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'revenue': revenue,
    }

    return render(request, 'reports.html', context)