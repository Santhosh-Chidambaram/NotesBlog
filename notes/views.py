from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserRegisterForm,AddNotesForm,ProfileUpdateForm,UserUpdateForm,NotesEditForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import Notes
from django.contrib.auth.decorators import login_required

# Create your views here.


def homeView(request):
    note = Notes.objects.all()
    context = {
        'note':note
    }
    return render(request,'notes/home.html')
#auth View
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request,username=username,password=raw_password)
            login(request,user)
            return HttpResponseRedirect('notes')
    else:
        form = UserRegisterForm()
    return render(request,'notes/register.html',{'form':form})
#auth View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            return redirect('notes')
        return HttpResponseRedirect("/user_login")
    else:
        return render(request,'notes/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

#All Notes View
def notes(request):
    note = Notes.objects.all().order_by('-pub_date')
    pdf = []
    for n in note:
        pdf_str = str(n.notes_files)
        if ".pdf" in pdf_str:
            pdf.append(pdf_str)
    context={
        'notes':note,
        'pdf':pdf
        
    }
    return render(request,'notes/notes.html',context)


#User Posts View
def myposts(request):
    note = Notes.objects.filter(user=request.user).order_by('-pub_date') 
    pdf = []
    for n in note:
        pdf_str = str(n.notes_files)
        if ".pdf" in pdf_str:
            pdf.append(pdf_str)
    context={
        'notes':note,
        'pdf':pdf
        
    }
    return render(request,'notes/myposts.html',context)

#Add Notes View
@login_required
def add_notes(request):
    if request.method == 'POST':
        form = AddNotesForm(request.POST,request.FILES)
        if form.is_valid():
            n = Notes(user=request.user,title=request.POST['title'],context=request.POST['context'],notes_files=request.FILES['notes_files'])
            n.save()

    form = AddNotesForm()
    return render(request,'notes/addnotes.html',{'form':form})


def about(request):
    return render(request,'notes/about.html')

#Edit Notes View
@login_required
def edit_notes(request,id):
    if request.method == 'POST':
        n_form = NotesEditForm(request.POST,request.FILES,instance=request.user.notes)
        if n_form.is_valid():
            n_form.save()
            return redirect('myposts')
    n_form = NotesEditForm(instance=request.user.notes)
    context = {
        'n_form':n_form
    }
    
    return render(request,'notes/editnotes.html',context)
def delete_notes(request,id):
    n = Notes.objects.filter(user=request.user,id=id)
    n.delete()
    
    return redirect('myposts')

#Profile View
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        u_form = UserUpdateForm(request.POST,instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

   
    context ={
        'p_form':p_form,
        'u_form':u_form
    }
    return render(request,'notes/profile.html',context)