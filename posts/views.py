from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group

# Create your views here.
@login_required
def all_posts(request):
    posts = Post.objects.all()
    return render(request, "all_posts.html", context={"posts": posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    is_mod = request.user.groups.filter(
        name="mod").exists() or request.user.is_staff
    is_blocked = request.user.groups.filter(
        name="blocked").exists()
    
    print(is_blocked)
    
    if request.method == "POST":
        delete_id = request.POST.get("delete")
        author_to_ban = request.POST.get()

        if delete_id:
            post_to_delete = Post.objects.get(pk=delete_id)
            post_to_delete.delete()

        if author_to_ban:
            author = User.objects.filter(
                username=author_to_ban.username).first()
            mod_group = Group.objects.get(name="mod")
            default_group = Group.objects.get(name="default")
            blocked_group = Group.objects.get(name="blocled")

            mod_group.user_set.remove(author)
            default_group.user_set.remove(author)
            blocked_group.user_set.remove(author)

        return redirect("home")
    
    return render(request, "post_detail.html", context={"post": post, "is_mod": is_mod})

@permission_required("posts.add_post", raise_exception=True)
@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        if request.user:
            author = request.user
        else:
            author = "Arthur"
        post = Post.objects.create(title=title, body=body, author=author)
        post.save()
        return redirect("home")
    
    return render(request, "create_post.html")