from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from flask_login import login_required
from .forms import CreateUserForm
from .models import Blog, ReplyComment,Title,Category,Comment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
# Create your views here.

def index(request):
    bloglist=Blog.objects.all()
    category = Category.objects.all()
    print(request.user,"loged in")
    return render(request,'index.html',{'bloglist':bloglist,'category':category})
    

# Selected Bolg

def selected_blog(request,id):
    fullblog = Blog.objects.get(id=id)
    total_likes = fullblog.total_likes()

    liked = False
    if fullblog.likes.filter(id=request.user.id).exists():
        liked=True
    if request.method =='POST':
        comment = request.POST.get('comment')
        Comment.objects.create(post=fullblog,name = request.user,body=comment)
        print(comment)

       

        return HttpResponseRedirect(request.path_info)
    return render(request,'single-standard.html',{'fullblog':fullblog,'total_likes':total_likes,'liked':liked})

# Like blog

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

# Search Button

def search(request):
    if request.method =='POST':
        searchTxt = request.POST['search']
        search = Blog.objects.filter(Q(title__title__icontains=searchTxt)|Q(author__username__icontains=searchTxt)|Q(category__category__icontains=searchTxt)|Q(keyword__icontains=searchTxt))
        print(search)
    return render(request,'index.html',{'bloglist':search})

#Edit Blog

def edit_blog(request,id):
    if request.user.is_authenticated:
        update_b = Blog.objects.get(id=id)
        category = Category.objects.all()
        title1 = Title.objects.all()

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
        return render(request,'update-blog.html',{'update_b':update_b, 'category': category, 'title1':title1})

#delete blog
def delete_blog(request,id):
    if request.user.is_authenticated:
        Blog.objects.filter(id=id).delete()
        return redirect('profile')
    else:
        return redirect('login')

# User Profile

def profile(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Blog.objects.filter(author = user)
        return render(request,'profile.html',{'profile':profile})
    else:
        return redirect('login')

# Upload Blog

def upload_blog(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        title = Title.objects.all()
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

        return render(request,'upload-blog.html',{'category':category, 'title':title})
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
    return redirect('index')

# @login_required(login_url="")
def replyComment(request,id):
   comments = Comment.objects.get(id=id)

   if request.method == 'POST':
       replier_name = request.user
       reply_content = request.POST.get('reply_content')

       newReply = ReplyComment(replier_name=replier_name, reply_content=reply_content)
       newReply.reply_comment = comments
       newReply.save()
       messages.success(request, 'Comment replied!')
       return redirect('index')


@login_required
def make_private(request, id):
    blog = Blog.objects.get(id=id)
  
    blog.private = True
    blog.save()
    messages.success(request, "Your Blog has been successfully Private.")
  
    return redirect('index', id=id)

@login_required
def make_public(request, pk):
    blog = Blog.objects.get(id=id)

    blog.private = False
    blog.save()
    messages.success(request, "Your Blog has been successfully Public.")
    
    return redirect('index', id=id)