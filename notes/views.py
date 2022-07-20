from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import*
from django.contrib.auth import authenticate,logout,login
from datetime import date

# Create your views here.
def about(request):
    return render(request,'about.html')

def view_messages(request):
    if not request.user.is_authenticated:
         return redirect('admin_login')
    contact=Contact.objects.all()
    d = {'contact':contact}
    return render(request,'view_messages.html',d)



def contact(request):
    if request.method=="POST":
        print(request)
        name=request.POST.get('name')
        email=request.POST.get('email')
        desc=request.POST.get('desc')
        contact = Contact(name=name, email=email, desc=desc)
        contact.save()
    return render(request,'contact.html')

def index(request):
    return render(request,'index.html')


def userlogin(request):
    error = ""
    if request.method == 'POST':
         u = request.POST['Email ID']
         p = request.POST['Password']
         user = authenticate(username=u, password=p)
         

         try:
               if user:
                   login(request, user)
                   error="no"
               else:
                  error="yes"
                


         except:
            error = "yes"
    d={'error': error}     
    return render(request, 'login.html', d)


def admin_login(request):
    error = ""
    if request.method == 'POST':
         u = request.POST['uname']
         p = request.POST['pwd']
         user = authenticate(username=u, password=p)
         

         try:
               if user.is_staff:
                   login(request, user)
                   error="no"
               else:
                  error="yes"
                


         except:
            error = "yes"
    d={'error': error}     
    return render(request, 'admin_login.html', d)        

def signup1(request):
    error = ""
    if request.method=='POST':
        f=request.POST['first_name']
        l=request.POST['last_name']
        c=request.POST['contact']
        e=request.POST['email']
        b=request.POST['branch']
        r=request.POST['role']
        p=request.POST['password']
        try:
            user= User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user,contact=c,branch=b,role=r)
            error="no"
        except:
            error="yes"
    d={'error':error}

    return render(request,'signup.html',d)

def admin_home(request):
    if not request.user.is_staff:
         return redirect('admin_login')
    pn=Notes.objects.filter(status="pending").count()
    an=Notes.objects.filter(status="Accept").count()
    rn=Notes.objects.filter(status="Reject").count()
    all=Notes.objects.all().count()
    d = {'pn':pn,'an':an,'rn':rn,'all':all}
    return render(request,'admin_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated:
         return redirect('login')
    user=User.objects.get(id=request.user.id)
    data=Signup.objects.get(user=user)
    d = {'data':data,'user':user}
    return render(request,'profile.html',d)

def edit_profile(request):
    if not request.user.is_authenticated:
         return redirect('login')
    user=User.objects.get(id=request.user.id)
    data=Signup.objects.get(user=user)
    error=False
    if request.method=='POST':
        f=request.POST['first_name']
        l=request.POST['last_name']
        e=request.POST['emailid']
        c=request.POST['contact']
        b=request.POST['branch']
        user.first_name=f
        user.last_name=l
        user.emailid=e
        data.contact=c
        data.branch=b
        user.save()
        data.save()
        error=True
    d = {'data':data,'user':user, 'error':error}
    return render(request,'edit_profile.html',d)

def changepassword(request):
    if not request.user.is_authenticated:
         return redirect('login')
    error=""
    if request.method=='POST':
        o=request.POST['old']
        n=request.POST['new']
        c=request.POST['confirm']
        if c==n:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"

        else:
            error="yes"
    d={'error':error}

    return render(request,'changepassword.html',d)



def upload_notes(request):
    if not request.user.is_authenticated:
         return redirect('login')
    error = ""
    if request.method=='POST':
        b=request.POST['branch']
        s=request.POST['subject']
        n=request.FILES['notesfile']
        f=request.POST['filetype']
        d=request.POST['description']
        u=User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,subject=s,notesfile=n,filetype=f,
            description=d,status='pending')
            error="no"
        except:
            error="yes"
    d={'error':error}

    return render(request,'upload_notes.html',d)

def view_mynotes(request):
    if not request.user.is_authenticated:
         return redirect('login')
    user=User.objects.get(id=request.user.id)
    notes=Notes.objects.filter(user=user)
    
    d = {'notes':notes,}
    return render(request,'view_mynotes.html',d)

def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('view_mynotes')

def view_users(request):
    if not request.user.is_authenticated:
         return redirect('admin_login')
    users=Signup.objects.all()
    d = {'users':users}
    return render(request,'view_users.html',d)

def delete_users(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user=User.objects.get(id=pid)
    user.delete()
    return redirect('view_users')




def pending_notes(request):
    if not request.user.is_authenticated:
         return redirect('admin_login')
    notes=Notes.objects.filter(status="pending")
    
    d = {'notes':notes,}
    return render(request,'pending_notes.html',d)

def accepted_notes(request):
    if not request.user.is_authenticated:
         return redirect('admin_login')
    notes=Notes.objects.filter(status="Accept")
    
    d = {'notes':notes,}
    return render(request,'accepted_notes.html',d)

def rejected_notes(request):
    if not request.user.is_authenticated:
         return redirect('admin_login')
    notes=Notes.objects.filter(status="Reject")
    
    d = {'notes':notes,}
    return render(request,'rejected_notes.html',d)

def all_notes(request):
    if not request.user.is_authenticated:
         return redirect('admin_login')
    notes=Notes.objects.all()
    
    d = {'notes':notes,}
    return render(request,'all_notes.html',d)
    
def assign_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    notes=Notes.objects.get(id=pid)
    error=""
    if request.method=='POST':
        s=request.POST['status']
        try:
            notes.status=s
            notes.save()
            error="no"
        except:
            error="yes"
    d={'notes':notes,'error':error}

    return render(request,'assign_status.html',d)

def delete_notes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('all_notes')

def viewallnotes(request):
    if not request.user.is_authenticated:
         return redirect('login')
    notes=Notes.objects.filter(status="Accept")
    
    d = {'notes':notes,}
    return render(request,'viewallnotes.html',d)



def CS_AND_IT(request):
    if not request.user.is_authenticated:
         return redirect('user_login')
    notes=Notes.objects.filter(branch="Information Technology")
    
    d = {'notes':notes,}
    return render(request,'CS_AND_IT.html',d)

def mechanical(request):
    if not request.user.is_authenticated:
         return redirect('user_login')
    notes=Notes.objects.filter(branch="Mechanical")
    
    d = {'notes':notes,}
    return render(request,'mechanical',d)

def civil(request):
    if not request.user.is_authenticated:
         return redirect('user_login')
    notes=Notes.objects.filter(branch="Civil")
    
    d = {'notes':notes,}
    return render(request,'civil.html',d)

def electrical(request):
    if not request.user.is_authenticated:
         return redirect('user_login')
    notes=Notes.objects.filter(branch="Electrical")
    
    d = {'notes':notes,}
    return render(request,'electrical.html',d)

def electronics(request):
    if not request.user.is_authenticated:
         return redirect('user_login')
    notes=Notes.objects.filter(branch="Electronics")
    
    d = {'notes':notes,}
    return render(request,'electronics.html',d)

