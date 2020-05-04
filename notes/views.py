from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserRegisterForm,AddNotesForm,ProfileUpdateForm,UserUpdateForm,NotesEditForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import Notes
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView,View,ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def homeView(request):
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
    return render(request,'notes/index.html',context)
#About View
def about(request):
    return render(request,'notes/about.html')

#Register View

class RegisterView(View):
    
    def post(self,request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request,username=username,password=raw_password)
            login(request,user)
            return HttpResponseRedirect('home')
    def get(self,request):
        form = UserRegisterForm()
        return render(request,'notes/register.html',{'form':form})

#Login View

class LoginView(View):
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            return redirect('home')
        return HttpResponseRedirect("/user_login")
    
    def get(self,request):
        return render(request,'notes/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

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

class NotesAddView(LoginRequiredMixin,View):

    def post(self,request):
        form = AddNotesForm(request.POST,request.FILES)
        if form.is_valid():
            n = Notes(user=request.user,title=request.POST['title'],context=request.POST['context'],notes_files=request.FILES['notes_files'])
            n.save()
            return redirect('home')
        return render(request,'notes/addnotes.html',{'form':form})
    
    def get(self,request):
         form = AddNotesForm()
         return render(request,'notes/addnotes.html',{'form':form})


#Edit Notes View

class NotesUpdateView(LoginRequiredMixin,UpdateView):
    model = Notes
    fields = ['title','context','notes_files']
    template_name='notes/edit_notes.html'
    pk_url_kwarg = 'pk'
    def form_valid(self,form):
        note = form.save(commit=False)
        note.user = self.request.user
        note.save()
        return redirect('myposts')


#Post DeleteView

def NotesDeleteView(request,pk):
    n = Notes.objects.filter(id=pk)
    n.delete()
    return redirect('myposts')


#Profile View

class ProfileView(LoginRequiredMixin,View):

    def get(self,request):
        return render(request,'notes/profile.html')
    

#ProfileEdit View
   
class ProfileEditView(View):
    def post(self,request):
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        u_form = UserUpdateForm(request.POST,instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            return redirect('profile')
    def get(self,request):
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)
        context ={
        'p_form':p_form,
        'u_form':u_form,
        'profile':True
    }
        return render(request,'notes/profile.html',context)

class NotificationsView(LoginRequiredMixin,ListView):
    template_name='notes/notification.html'
    context_object_name='notifis'

    def get_queryset(self):
        return self.request.user.to_user_set.all().order_by('-date')