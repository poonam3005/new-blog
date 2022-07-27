from datetime import date, datetime, timedelta
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from .models import Blog,Title,Category,Comment, ReplyComment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from calendar import HTMLCalendar
import calendar
from .utils import Calendar
from django.views.generic import ListView
from django.utils.safestring import mark_safe

def index(request):
    bloglist=Blog.objects.filter(private=False)
    category = Category.objects.all()
    print(request.user,"loged in")
    return render(request,'index.html',{'bloglist':bloglist,'category':category})

# privet or public
@login_required
def private(request,id):
    blog = Blog.objects.get(id=id)
    if blog.private is True:
        blog.private = False
        blog.save()
    else:
        blog.private = True
        blog.save()
    return redirect('profile')

# Calender
class CalendarView(ListView):
    model = Blog
    template_name = 'calender.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d, d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth()
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


# def calendar(request):
#     calendar = HTMLCalendar().formatmonth(2022,6)
#     return render(request,'calender.html',{'calendar':calendar})
# Selected Bolg

def selected_blog(request,id):
    fullblog = Blog.objects.get(id=id)
    total_likes = fullblog.total_likes()
    reply = ReplyComment.objects.all()

    liked = False
    if fullblog.likes.filter(id=request.user.id).exists():
        liked=True
    
    if request.method =='POST':
        comment = request.POST['comment']
        parentid = request.POST.get('parent',"")
        if parentid=="":
            Comment.objects.create(post=fullblog,name = request.user,body=comment)
            print("comment")
        else:
            parent = Comment.objects.get(id=parentid)
            ReplyComment.objects.create(post=fullblog,name = request.user,body=comment,parent=parent)
            print('reply')
        return HttpResponseRedirect(request.path_info)
    return render(request,'single-standard.html',{'fullblog':fullblog,'total_likes':total_likes,'liked':liked,'replyComment':reply})

# Like blog
@login_required
def like_blog(request,id):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        like=Blog.objects.get(id = post_id)

        liked = False
        if like.likes.filter(id=request.user.id).exists():
            like.likes.remove(request.user)
            liked=False
        else:
            like.likes.add(request.user)
            liked =True
        return redirect('selected_blog',id)
        # return HttpResponseRedirect(reverse('selected_blog',args=[str(id)]))

# category
def category(request,cat):
    category = Category.objects.all()
    cat_id = Category.objects.get(category=cat)
    bloglist = Blog.objects.filter(category=cat_id.id)

    # return HttpResponse("hello  "+cat)
    return render(request,'category.html',{'bloglist':bloglist,'category':category})


# Search Button

def search(request):
    if request.method =='POST':
        searchTxt = request.POST['search']
        search = Blog.objects.filter(Q(title__title__icontains=searchTxt)|Q(author__username__icontains=searchTxt)|Q(category__category__icontains=searchTxt)|Q(keyword__icontains=searchTxt))
        print(search)
    return render(request,'index.html',{'bloglist':search})

#Edit Blog
@login_required
def edit_blog(request,id):
    if request.user.is_authenticated:
        update_b = Blog.objects.get(id=id)
        if request.method =='POST':
            title = request.POST['title']
            category = request.POST['category']
            entryTxt = request.POST['entryTxt']
            Desc = request.POST['Desc']
            keyword = request.POST['keyword']
            image = request.FILES['Uploadimage']

            ttl=Title.objects.get(title=title)
            cat =Category.objects.get(category=category)

            update_b.title=ttl
            update_b.category=cat
            update_b.entryTxt=entryTxt
            update_b.Desc=Desc
            update_b.keyword=keyword
            update_b.image=image

            update_b.save()
            return redirect('profile')
        return render(request,'update-blog.html',{'update_b':update_b})

#delete blog
@login_required
def delete_blog(request,id):
    if request.user.is_authenticated:
        Blog.objects.filter(id=id).delete()
        return redirect('profile')
    else:
        return redirect('login')

# User Profile
@login_required
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Blog.objects.filter(author = user)
        return render(request,'profile.html',{'profile':profile})
    else:
        return redirect('login')

# Upload Blog
@login_required
def upload_blog(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        if request.method =='POST':
            title = request.POST['title']
            category = request.POST['category']
            entryTxt = request.POST['entryTxt']
            Desc = request.POST['Desc']
            keyword = request.POST['keyword']
            image = request.FILES['Uploadimage']
            
            try:
                title = Title.objects.get(title = title)
                category = Category.objects.get(category=category)
                Blog.objects.create(author=request.user,title=title,category=category,entryTxt=entryTxt,Desc=Desc,keyword=keyword,image=image)
            except:

                print("Title or Categoty")
            return redirect('index')

        return render(request,'upload-blog.html',{'category':category})
    else:
        return redirect('login')

# ---------- Registration -------------

def registration(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account Creates Successfully' + user)

    context = {'form' : form}
    return render(request,'registration.html', context)

# ---------- login -------------

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or Password incorrect')
    return render(request,'login.html')


# ---------- logout -------------

def logoutuser(request):
    logout(request)
    return redirect('login')
