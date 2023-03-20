from django.http.response import HttpResponse
from random import sample
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from django.utils.text import slugify
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from cmsblg.models import *
from datetime import datetime
from django.urls import reverse_lazy, reverse
import pandas as pd
import psycopg2
import mysql.connector
import folium
from django.core.paginator import Paginator, EmptyPage

def index(request):
    slides = Slide.objects.all()
    post = Post.objects.filter(featured=True)

    news_category = Category.objects.filter(title='news').first()
    news_posts = Post.objects.filter(category=news_category) if news_category else None

    event_category = Category.objects.filter(title='events').first()
    new_events = Post.objects.filter(category=event_category) if event_category else None

    if post:
        random_post = sample(list(post), 1)[0]
    else:
        random_post = None

    if slides:
        num_slides = min(2, slides.count())
        random_slides = sample(list(slides), num_slides)
        num_mini_slides = min(4, slides.count())
        random_slide_mini = sample(list(slides), num_mini_slides)
    else:
        random_slides = None
        random_slide_mini = None
        # dynamic map
        #  # or other database connectors

            # # connect to database
    # conn = psycopg2.connect(database="databs", user="root", password="", host="localhost", port="3306")
    conn = mysql.connector.connect(user='root', password='',host='localhost', database='databs')
    
    cursor = conn.cursor()

            # query data from database and load into a DataFrame
    query = "SELECT geolat, geolong FROM cmi"
    df = pd.read_sql_query(query, conn)

            # create map
    m = folium.Map(location=[7.635,124.854], zoom_start=7)

            # loop through DataFrame rows and add markers to the map
    for index, row in df.iterrows():
        folium.Marker(
            location=[row['geolat'], row['geolong']],
            # popup=row['name'],
            icon=folium.Icon(icon='cloud')
        ).add_to(m)

    # m = folium.Map(location=[7.635,124.854], zoom_start=7)

    # folium.Marker(
    #     location=[7.040, 122.075],
    #     popup='Zamboanga',
    #     icon=folium.Icon(icon='cloud')
    # ).add_to(m)

    # folium.Marker(
    #     location=[7.187, 124.214],
    #     popup='Cotabato',
    #     icon=folium.Icon(icon='cloud')
    # ).add_to(m)

    # folium.Marker(
    #     location=[8.172, 124.216],
    #     popup='Cagayan de Oro',
    #     icon=folium.Icon(icon='cloud')
    # ).add_to(m)

    context = {
        'post': post,
        'new_events': new_events,
        'news_posts': news_posts,
        'slides' : slides, 
        'random_post' : random_post, 
        'random_slides' : random_slides, 
        'random_slide_mini' : random_slide_mini, 
        'map': m._repr_html_(),
    }
    return render(request, 'core/index.html', context)

def community(request):
    categories = Category.objects.all()
    posts = Post.objects.all()
    return render(request, 'community.html', {'categories': categories, 'posts': posts})

@login_required(login_url='/login')
def mypost(request):
    posts = Post.objects.filter(author=request.user)

    return render(request, 'single-post.html', {'posts': posts})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['category', 'title', 'intro', 'body', 'image']
    success_url = reverse_lazy('mypost')
    template_name = 'post_update.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

def allpost(request):
    posts = Post.objects.filter(status=Post.ACTIVE)
    posts = Post.objects.order_by('-created_at')

    return render(request, 'allposts.html', {'posts': posts})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'createpost.html'
    success_url = reverse_lazy('allpost')

    def form_valid(self, form):
        form.instance.author = self.request.user
        slug = slugify(form.cleaned_data['title'])
        count = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{slug}-{count}"
            count += 1
        form.instance.slug = slug
        return super().form_valid(form)

@staff_member_required(login_url='/login')
def deletepost(request, slug):
    slide = get_object_or_404(Post, slug=slug)
    try:
        slide.delete()
        messages.success(request, 'Post deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting Post: {str(e)}')
    return redirect('/dashboard')


def about(request):
    try:
        consortium = Consortium.objects.get(pk=1)
    except Consortium.DoesNotExist:
        consortium = None
    return render(request, 'about.html', {'consortium': consortium})


def consortium(request):
    try:
        consortium = Consortium.objects.get(pk=1)
    except Consortium.DoesNotExist:
        consortium = None
    return render(request, 'consortium.html', {'consortium': consortium})

@staff_member_required(login_url='/login')
def createconsortium(request):
    
    form = ConsortiumForm()
    if request.method == 'POST':
        form = ConsortiumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')

    context = {'form': form}
    return render(request, 'createpost.html', context)

class ConsortiumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Consortium
    fields = '__all__'
    success_url = reverse_lazy('dashboard')
    template_name = 'commodity_update.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


def organization(request):
    try:
        org = Organization.objects.get(pk=1)
    except Organization.DoesNotExist:
        org = None
    return render(request, 'organization.html', {'org': org})

class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'createcommodity.html'
    success_url = reverse_lazy('dashboard')

class OrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'commodity_update.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

@staff_member_required(login_url='/login')
def deleteorganization(request, pk):
    organization = get_object_or_404(Organization, id=pk)
    try:
        organization.delete()
        messages.success(request, 'Organization deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting Organization: {str(e)}')
    return redirect('/dashboard')


def cmi(request):
    return render(request, 'CMI.html')


def cmidetail(request):
    return render(request, 'CMI-detail.html')

# def category(request):
#     return render(request, 'category.html')


def commodities(request):
    commodity_list = Commodity.objects.all()
    paginator = Paginator(commodity_list, 4)  # Show 10 commodities per page
    page = request.GET.get('page')
    commodities = paginator.get_page(page)
    return render(request, 'Commodities.html', {'commodities': commodities, 'commodity_list': commodity_list})

def commodetail(request, commodity_slug):
    commodity = Commodity.objects.all()
    commodities = get_object_or_404(Commodity, slug=commodity_slug)
    
    return render(request, 'commodetail.html', {'commodities': commodities, 'commodity': commodity})

class CommodityCreateView(LoginRequiredMixin, CreateView):
    model = Commodity
    form_class = CommodityForm
    template_name = 'createpost.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        slug = slugify(form.cleaned_data['name'])
        count = 1
        while Commodity.objects.filter(slug=slug).exists():
            slug = f"{slug}-{count}"
            count += 1
        form.instance.slug = slug
        return super().form_valid(form)
    
class CommodityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Commodity
    fields = ['name', 'detail', 'image']
    success_url = reverse_lazy('dashboard')
    template_name = 'commodity_update.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    
@staff_member_required(login_url='/login')
def deletecommodity(request, commodity_slug):
    commodity = get_object_or_404(Commodity, slug=commodity_slug)
    try:
        commodity.delete()
        messages.success(request, 'Commodity deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting Commodity: {str(e)}')
    return redirect('/dashboard')
    

def project(request):
    projects = Project.objects.all()
    onprojects = Project.objects.filter(status=Project.ONGOING)
    finprojects = Project.objects.filter(status=Project.FINISHED)
    context = {
        'projects': projects,
        'onprojects': onprojects,
        'finprojects': finprojects,

    }
    return render(request, 'projects.html', context)

def onproject(request):
    onprojects = Project.objects.filter(status=Project.ONGOING)
    return render(request, 'onproject.html', {'onprojects': onprojects})

def finproject(request):
    finprojects = Project.objects.filter(status=Project.FINISHED)
    return render(request, 'finproject.html', {'finprojects': finprojects})

def onprojectdetail(request, project_slug):
    onprojects = get_object_or_404(Project, slug=project_slug)
    return render(request, 'ondetail.html', {'onprojects': onprojects})

def finprojectdetail(request, project_slug):
    finprojects = get_object_or_404(Project, slug=project_slug)
    return render(request, 'findetail.html', {'finprojects': finprojects})

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'createproject.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        slug = slugify(form.cleaned_data['title'])
        count = 1
        while Project.objects.filter(slug=slug).exists():
            slug = f"{slug}-{count}"
            count += 1
        form.instance.slug = slug
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['status']
    success_url = reverse_lazy('dashboard')
    template_name = 'project_update.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

@staff_member_required(login_url='/login')
def projectdelete(request, project_slug):
    project = get_object_or_404(Category, slug=project_slug)
    try:
        project.delete()
        messages.success(request, 'project deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting project: {str(e)}')
    return redirect('/dashboard')

def services(request):
    return render(request, 'services.html')

@staff_member_required(login_url='/login')
def createslide(request):
    
    form = SlideForm()
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')

    context = {'form': form}
    return render(request, 'core/createform.html', context)

class SliderUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Slide
    fields = '__all__'
    success_url = reverse_lazy('dashboard')
    template_name = 'commodity_update.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

@staff_member_required(login_url='/login')
def deleteslide(request, id):
    slide = get_object_or_404(Slide, id=id)
    try:
        slide.delete()
        messages.success(request, 'Slide deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting slide: {str(e)}')
    return redirect('/dashboard')
    # slides = Slide.objects.get(id=id)
    # slides.delete()
  
    # context = {
    # 'slides': 'slides'
    # }
    # return redirect( '/dashboard', context)

@staff_member_required(login_url='/login')
def deleteuser(request, id):
    user = get_object_or_404(User, id=id)
    try:
        user.delete()
        messages.success(request, 'User deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting User: {str(e)}')
    return redirect('/dashboard')

@staff_member_required(login_url='/login')
def deletecategory(request, slug):
    category = get_object_or_404(Category, slug=slug)
    try:
        category.delete()
        messages.success(request, 'Category deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting Category: {str(e)}')
    return redirect('/dashboard')

@staff_member_required(login_url='/login')
def dashboard(request):
    commodity = Commodity.objects.all()
    slides = Slide.objects.all()
    posts = Post.objects.all()
    categories = Category.objects.all()
    projects = Project.objects.all()
    try:
        consortium = Consortium.objects.get(id=1)
    except Consortium.DoesNotExist:
        consortium = None
    organizations = Organization.objects.all()

    users = User.objects.all().order_by('-is_staff')
    # Get a QuerySet of all session objects
    sessions = Session.objects.filter(expire_date__gte=timezone.now())  
    # Create a dictionary to hold the last activity time for each user
    user_activity = {}  
    # Loop over the sessions and update the last activity time for each user
    for session in sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            user_activity[user_id] = session.expire_date - datetime.now(timezone.utc)   
    # Loop over the users and update their active status
    for user in users:
        last_activity = user_activity.get(str(user.id), None)
        if last_activity:
            # User has an active session
            active_status = 'Logged In'
        else:
            # User does not have an active session
            active_status = 'Logged Off'
        # Update the active status for the user
        user.active_status = active_status   
    # Create a list of user dictionaries to hold the user data
    user_data_list = []    
    # Loop over the users and add their data to the user data list
    for user in users:
        user_data = {
            'user': user,
            'active_status': user.active_status
        }
        user_data_list.append(user_data)


    context = {
                'user_data_list': user_data_list,
                'slides': slides,
                'posts': posts,
                'commodity': commodity,
                'categories': categories,
                'projects' : projects,
                'consortium' : consortium,
                'organizations' : organizations,

}     
    return render(request, 'dashboard.html', context)

def postman(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'post-section.html', context)

def galleryman(request):
    photos = AlbumPhoto.objects.all()
    context = {'photos': photos}
    return render(request, 'dash-gallery.html', context)

def robots_txt(request):
    text = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(text), content_type="text/plain")

def gallery(request):
    albums = Album.objects.all()
    carousel = AlbumPhoto.objects.filter(carousel = True)

    context = {
        'albums': albums,
        'carousel': carousel,
        }
    return render(request, 'gallery.html', context )

@staff_member_required(login_url='/login')
def createalbum(request):
    
    form = AlbumForm()
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')

    context = {'form': form}
    return render(request, 'createcategory.html', context)

@staff_member_required(login_url='/login')
def deleteAlbum(request, pk):
    album = get_object_or_404(Album, id=pk)
    try:
        album.delete()
        messages.success(request, 'album deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting album: {str(e)}')
    return redirect('/dashboard')

def album(request, pk):
    albums = get_object_or_404(Album, pk=pk)
    albumphotos = albums.photos.all()
    context = {
        'albums': albums,
        'albumphotos': albumphotos,
        }

    return render(request, 'albumphoto.html', context)

@staff_member_required(login_url='/login')
def createphoto(request):
    
    form = PhotoForm()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')

    context = {'form': form}
    return render(request, 'createcategory.html', context)

class photoupdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AlbumPhoto
    fields = '__all__'
    success_url = reverse_lazy('dashboard')
    template_name = 'createcategory.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

@staff_member_required(login_url='/logout')
def deletePhoto(request, pk):
    photo = get_object_or_404(AlbumPhoto, id=pk)
    try:
        photo.delete()
        messages.success(request, 'photo deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting photo: {str(e)}')
    return redirect('/dashboard')

# def photo(request, pk):
#     photo = get_object_or_404(AlbumPhoto, pk=pk)

#     return render(request, 'singlephoto.html', {'photo': photo})

def contact(request):

    return render(request, 'contact.html')

def map(request):

    m = folium.Map(location=[7.040, 122.075], zoom_start=7)

    folium.Marker(
        location=[7.040, 122.075],
        popup='Zamboanga',
        icon=folium.Icon(icon='cloud')
    ).add_to(m)

    context = {'map': m._repr_html_()}

    return render(request, 'map.html', context)

def dashabout(request):
    try:
        consortium = Consortium.objects.get(id=1)
    except Consortium.DoesNotExist:
        consortium = None
    if consortium is not None:
        url = reverse('consortium_update', args=[consortium.pk])
    else:
    # Handle the case where there is no consortium object
        url = 'some_default_url'

    try:
        org = Organization.objects.get(pk=1)
    except Organization.DoesNotExist:
        org = None

    context = {'consortium': consortium, 'consortium_url': url, 'org': org}
    return render(request, 'dash-about.html', context)

def dashcmi(request):
    context = {'consortium': consortium}
    return render(request, 'dash-cmi.html', context)

def dashslider(request):
    slides = Slide.objects.all
    context = {'slides':slides}
    return render(request, 'dash-slider.html', context)

def dashfaq(request):
    faq = Fact.objects.all()
    context = {'faq': faq}
    return render(request, 'dash-faq.html', context)

def dashcommodity(request):
    commodity = Commodity.objects.all()
    context = {'commodity': commodity}
    return render(request, 'dash-commodities.html', context)

def dashcommunity(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    context = {'posts': posts, 'categories': categories}
    return render(request, 'dash-community.html', context)

def dashproject(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'dash-projects.html', context)

def dashservices(request):
    services = Commodity.objects.all()
    context = {'services': services}
    return render(request, 'dash-services.html', context)

def dashuser(request):

    users = User.objects.all().order_by('-is_staff')
    # Get a QuerySet of all session objects
    sessions = Session.objects.filter(expire_date__gte=timezone.now())  
    # Create a dictionary to hold the last activity time for each user
    user_activity = {}  
    # Loop over the sessions and update the last activity time for each user
    for session in sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            user_activity[user_id] = session.expire_date - datetime.now(timezone.utc)   
    # Loop over the users and update their active status
    for user in users:
        last_activity = user_activity.get(str(user.id), None)
        if last_activity:
            # User has an active session
            active_status = 'Logged In'
        else:
            # User does not have an active session
            active_status = 'Logged Off'
        # Update the active status for the user
        user.active_status = active_status   
    # Create a list of user dictionaries to hold the user data
    user_data_list = []    
    # Loop over the users and add their data to the user data list
    for user in users:
        user_data = {
            'user': user,
            'active_status': user.active_status
        }
        user_data_list.append(user_data)

    context = { 'user_data_list': user_data_list,
            }
    return render(request, 'dash-users.html', context)

def dashslider(request):
    try:
        slides = Slide.objects.all
    except:
        slides = None

    context = {
        
        'slides': slides
    }
    return render(request, 'dash-slider.html', context)

# class commoditylist(ListView):
#     template_name = 'commodities.html'
#     context_object_name = 'commodity_list'
#     queryset = Commodity.objects.all().order_by('-created_at')
#     paginate_by = 5
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = Paginator(context['commodity_list'], self.paginate_by)
#         page = self.request.GET.get('page')
#         context['commodity_list'] = paginator.get_page(page)
#         return context