from datetime import timedelta
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView, DetailView,View
from django.utils import timezone
from django.http import JsonResponse
from newsportal.form import CommentForm, ContactForm, NewsLetterForm
from newsportal.models import Post

class HomeView(ListView):
    model = Post
    template_name = "tnews/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull = False, status="active"
    ).order_by("-published_at")[:5]

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at" ,"-views_count").first()            
        )
        context["featured_posts"] =Post.objects.filter(published_at__isnull=False, status="active"
        ).order_by("-published_at" ,"-views_count")[1:4]

        one_week_ago= timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] =Post.objects.filter(published_at__isnull=False, status="active", published_at__gte=one_week_ago
        ).order_by("-published_at" ,"-views_count")[:7]

        context["recent_posts"] =Post.objects.filter(published_at__isnull=False, status="active"
                                                     
        ).order_by("-published_at")[:7]

        context["category_spotlight_posts"] =Post.objects.filter(published_at__isnull=False, status="active").order_by("-views_count", "-published_at")[:2]
        context["editor_pick"] =Post.objects.filter(published_at__isnull=False, status="active").order_by("-views_count")[:2]
        return context
class PostListView(ListView):
    model = Post
    template_name = "tnews/list/list.html"
    context_object_name ="posts"
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status = "active"
        ).order_by("-published_at")
    

class PostByTagView(ListView):
    model = Post
    template_name = "tnews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset() #Post.objects.all()
        query = query.filter(published_at__isnull=False, status="active", tag__id = self.kwargs["tag_id"],
        ).order_by("-published_at")

        return query 

class PostByCategoryView(ListView):
    model = Post
    template_name = "tnews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset() #Post.objects.all()
        query = query.filter(published_at__isnull=False, status="active", category_id = self.kwargs["category_id"],
        ).order_by("-published_at")

        return query        

class PostDetailView(DetailView):
    model = Post
    template_name="tnews/detail/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status="active")
        return query 
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs) 
        obj = self.get_object() # currently viewed post
        obj.views_count += 1
        obj.save()
        context["previous_post"] =(
            Post.objects.filter(published_at__isnull=False, status ="active", id__lt=obj.id).order_by("-id").first()
        )
        context["next_post"] = (
            Post.objects.filter(published_at__isnull=False, status ="active", id__gt=obj.id).order_by("id").first()
        )
        return context
from django.contrib import messages    
class ContactView(TemplateView):
    template_name= "tnews/contact.html"  

    def get(self,request):
        return render(request, self.template_name)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,"Successfully submitted your query. We will content you soon ."
            )
            return redirect("contact")
        else:
            messages.error(
                request,"Connot submit your query. Please make sure all fields are valid.",
            ) 
            return render(
                request,
                self.template_name,
                {"form": form},
            )
class AboutView(TemplateView):
    template_name ="tnews/about_us.html"

class AllCategoryView(TemplateView):
    template_name ="tnews/list/categories.html"  

    def get(self,request):
        return render(request, self.template_name)

class AllTagView(TemplateView):
    template_name ="tnews/list/tags.html"  

    def get(self,request):
        return render(request, self.template_name)

from django.core.paginator import PageNotAnInteger,Paginator
from django.db.models import Q
class PostSearchView(View):
    template_name= "tnews/list/list.html"

    def get(self,request,*args,**kwargs):
        query = request.GET[
            "query"
        ]
        post_list = Post.objects.filter(
            (Q(title__icontains=query) |Q(content__icontains=query))
            &Q(status="active")
            &Q(published_at__isnull=False)
        ).order_by("-published_at")

        page = request.GET.get("page",1)
        paginate_by = 3
        paginator = Paginator(post_list, paginate_by)
        try:
            posts =paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)

        return render(
            request,
            self.template_name,
            {"page_obj": posts, "query": query}
        )  
    
class NewsLetterView(View):

    def post(self,request):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = NewsLetterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Successfully subscribe to the newsletter."
                    },
                    status =201,
                )
            else:
                return JsonResponse(
                    {
                       "success": False,
                        "message": "Con't subscribe to the newsletter.", 
                    },
                    status=400,
                )
    
        else:
            return JsonResponse(
                {
                       "success": False,
                        "message": "Con't process. Must be an AJAX HMLHttpRequest.", 
                    },
                status=400,
            )
        
# class CommentView(View):
#     def post(self,request,*args,**kwargs):
#         form = CommentForm(request.POST)
#         post_id = request.POST["post"]
#         if form.is_valid():
#             form.save()
#             return redirect("post-detail", post_id)
        
#         post = Post.objects.get(pk=post_id)
#         return render(
#             request,
#             "tnews/detail/detail.html",
#             {"post" :post , "form": form},
#         )        
        
class CommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST["post"]

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect("post-detail", post_id)
        else:
            post = Post.objects.get(pk=post_id)
            return render(
                request,
                "tnews/detail/detail.html",
                {
                    "post": post,
                    "form": form,
                },
            )        
