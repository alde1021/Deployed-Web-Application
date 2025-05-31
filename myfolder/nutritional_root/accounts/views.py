from django.shortcuts import get_object_or_404, render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from accounts.forms import ProfileForm
from accounts.models import Student
from django.contrib import messages
from django.db.models import Count
from collections import Counter
# Create your views here.



def student_list(request):
     mem = Student.objects.all()
     return render(request, 'accounts/index.html', {'mem':mem})

def index(request):
    mem = Student.objects.all()  # Get all student records

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Or 'index' if that's the correct URL name
        else:
            print(form.errors)
    else:
        form = ProfileForm()

    context = {
        'form': form,
        'mem': mem,
    }

    return render(request, 'accounts/index.html', context)




def HomePage(request):
    return render (request,'accounts/home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'accounts/signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect!")

    return render (request,'accounts/login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    students = Student.objects.all()
    
    # Filter by gender
    males = students.filter(gender__iexact='Male')
    females = students.filter(gender__iexact='Female')

    # Count BMI categories
    bmi_counts_male = Counter(s.nutritional_status() for s in males)
    bmi_counts_female = Counter(s.nutritional_status() for s in females)

    # Count Height-for-Age categories
    height_counts_male = Counter(s.height_for_age() for s in males)
    height_counts_female = Counter(s.height_for_age() for s in females)

    context = {
        'total_students': students.count(),
        'total_male': males.count(),
        'total_female': females.count(),
        'bmi_counts_male': bmi_counts_male,
        'bmi_counts_female': bmi_counts_female,
        'height_counts_male': height_counts_male,
        'height_counts_female': height_counts_female,
    }

    return render(request, 'accounts/dashboard.html', context)

def Add_student(request):
    mem = Student.objects.all()  # Get all student records

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add')  # Or 'index' if that's the correct URL name
        else:
            print(form.errors)
    else:
        form = ProfileForm()

    context = {
        'form': form,
        'mem': mem,
    }

    return render(request, 'accounts/add.html', context)
# updpate view
def update_student(request, id_no):
    mem = Student.objects.get(id_no=id_no)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=mem)

        if form.is_valid():
            form.save()
            return redirect( 'index')
        
    else:
        form = ProfileForm(instance=mem)
    return render(request, 'accounts/update.html', {'form':form})

# delete view

def delete_student(request, id_no):
    mem = get_object_or_404(Student, id_no=id_no)

    if request.method == 'POST':
        mem.delete()
        messages.success(request, f"Student {mem.first} {mem.last} has been deleted.")
        return redirect('index')  # Adjust to your actual student list view name

    return render(request, 'accounts/delete.html', {'mem': mem})

def report_view(request):
    students = Student.objects.all()
    return render(request, 'accounts/reports.html', {'students': students})