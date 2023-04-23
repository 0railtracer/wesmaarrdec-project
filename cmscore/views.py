from django.http.response import HttpResponse
from random import sample
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from auth_user.models import User
from django.utils.text import slugify
from django.contrib.sessions.models import Session
from django.utils import timezone
# from django.contrib.auth.models import User
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
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.core.paginator import Paginator, EmptyPage
from django.core.files.storage import default_storage

def index(request):
    slides = Slide.objects.all()
    post = Post.objects.filter(featured=True)
    photo = AlbumPhoto.objects.filter(slide=True)
    # commodity = Commodity.objects.filter(slide=True)

    news_category = Category.objects.filter(title__iexact='news').first()
    news_posts = Post.objects.filter(category=news_category) if news_category else None

    event_category = Category.objects.filter(title__iexact='events').first()
    new_events = Post.objects.filter(category=event_category).first() if event_category else None

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
    cursor = None
    conn = None 
    m = None
    try:
        conn = mysql.connector.connect(user='root', password='',host='localhost', database='testo')
        
        cursor = conn.cursor()

                # query data from database and load into a DataFrame
        query = "SELECT geolat, geolong, name FROM cmi"
        df = pd.read_sql_query(query, conn)

                # create map
        m = folium.Map(location=[7.561,124.233], zoom_start=8, control_scale=True)
        
                # loop through DataFrame rows and add markers to the map
        for index, row in df.iterrows():
            folium.Marker(
                location=[row['geolat'], row['geolong']],
                popup=row['name'],
                icon=folium.Icon(icon='icon')
            ).add_to(m)
    except mysql.connector.errors.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        # dynamic icon test
        # markers = Marker.objects.all()
        # for marker in markers:
        #     folium.Marker(
        #         location=[marker.geolat, marker.geolong],
        #         popup=marker.name,
        #         icon=folium.Icon(icon=marker.icon_path)
        #     ).add_to(m)

        # context = {
        #     'my_map': m._repr_html_(),
            
        # m = folium.Map(location=[7.635,124.854], zoom_start=7)

        # folium.Marker(
        #     location=[7.040, 122.075],
        #     popup='Zamboanga',
        #     icon=folium.Icon(icon='icon')
        # ).add_to(m)

        # folium.Marker(
        #     location=[7.187, 124.214],
        #     popup='Cotabato',
        #     icon=folium.Icon(icon='icon')
        # ).add_to(m)

        # folium.Marker(
        #     location=[8.172, 124.216],
        #     popup='Cagayan de Oro',
        #     icon=folium.Icon(icon='icon')
        # ).add_to(m)

    context = {
        'post': post,
        'new_events': new_events,
        'news_posts': news_posts,
        'slides' : list(slides) + list(photo), 
        'random_post' : random_post, 
        'random_slides' : random_slides, 
        'random_slide_mini' : random_slide_mini, 
        # 'map': m._repr_html_(),
    }
    if m is not None:
        context['map'] = m._repr_html_()
    
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
        consortium = About.objects.get(pk=1)
    except About.DoesNotExist:
        consortium = None
    return render(request, 'about.html', {'consortium': consortium})


def consortium(request):
    try:
        consortium = About.objects.get(pk=1)
    except About.DoesNotExist:
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
    return render(request, 'createcategory.html', context)

class ConsortiumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = About
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

class CMI:
    def __init__(self, cmi_id, name, detail, logo):
        self.cmi_id = cmi_id
        self.name = name
        self.detail = detail
        self.logo_url = default_storage.url(logo)

def cmi(request):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='testo')
        cursor = conn.cursor()

        query = "SELECT * FROM cmi"
        cursor.execute(query)

        cmi_list = []
        for row in cursor.fetchall():
            cmi = CMI(row[0], row[2], row[8], row[7])
            cmi_list.append(cmi)
            # print(row[3])
    except mysql.connector.errors.Error as e:
        print(f"An error occurred: {e}")
        cmi_list = None
        # commodity_list = None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if cmi_list is not None:
        context = {
            'cmi_list': cmi_list,
        
        }
    else:
        context = {}
        
    return render(request, 'CMI.html', context)


def cmidetail(request, cmi_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(user='root', password='',
                              host='localhost', database='testo')
        cursor = conn.cursor()

        query = "SELECT * FROM cmi WHERE agency_id = %s"
        cursor.execute(query, (cmi_id,))
        row = cursor.fetchone()
        cmi = CMI(row[0], row[2], row[8], row[7])

        # Make sure cursor is fully read before executing second query
        cursor.fetchall()

        query_all = "SELECT * FROM cmi"
        cursor.execute(query_all)

        cmis = []
        for rows in cursor.fetchall():
            cmidetail = CMI(rows[17], rows[2], rows[8], rows[7])
            cmis.append(cmidetail)

    except mysql.connector.errors.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    context = {
        'cmi':cmi,
        # 'cmis':cmis
    }
    return render(request, 'CMI-detail.html', context)


# def category(request):
#     return render(request, 'category.html')

class Commodity:
    def __init__(self, com_id, name, detail, img_path):
        self.com_id = com_id
        self.name = name
        self.detail = detail
        self.img_url = default_storage.url(img_path)

def commodities(request):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='test101')
        cursor = conn.cursor()

        query = "SELECT * FROM commodity"
        cursor.execute(query)

        commodity_list = []
        for row in cursor.fetchall():
            commodity = Commodity(row[0], row[1], row[2], row[3])
            commodity_list.append(commodity)
            print(row[3])
        paginator = Paginator(commodity_list, 4)
        page = request.GET.get('page')
        commodities = paginator.get_page(page)
    except mysql.connector.errors.Error as e:
        print(f"An error occurred: {e}")
        commodities = None
        commodity_list = None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if commodities is not None and commodity_list is not None:
        context = {'commodities': commodities,
                   'commodity_list': commodity_list,
        }
    else:
        context = {}
        
    return render(request, 'Commodities.html', context)



def commodetail(request, com_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(user='root', password='',
                              host='localhost', database='test101')
        # create a cursor to execute SQL queries
        cursor = conn.cursor()

        # execute a SELECT query to fetch data for the specified commodity
        query = "SELECT * FROM commodity WHERE com_id = %s"
        cursor.execute(query, (com_id,))

        row = cursor.fetchone()
        commodite = Commodity(row[0], row[1], row[2], row[3])
        
        
        # execute a SELECT query to fetch all the data from the commodity table
        query_all = "SELECT * FROM commodity"
        cursor.execute(query_all)
        commodity = cursor.fetchall()
    except mysql.connector.errors.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        # render the template with the fetched data
    return render(request, 'commodetail.html', {'commodite': commodite, 'commodity': commodity})

# class CommodityCreateView(LoginRequiredMixin, CreateView):
#     model = Commodity
#     form_class = CommodityForm
#     template_name = 'createcommodity.html'
#     success_url = reverse_lazy('dashboard')

#     def form_valid(self, form):
#         slug = slugify(form.cleaned_data['name'])
#         count = 1
#         while Commodity.objects.filter(slug=slug).exists():
#             slug = f"{slug}-{count}"
#             count += 1
#         form.instance.slug = slug
#         return super().form_valid(form)
    
# class CommodityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Commodity
#     fields = ['name', 'detail', 'image']
#     success_url = reverse_lazy('dashboard')
#     template_name = 'commodity_update.html'

#     def test_func(self):
#         return self.request.user.is_staff or self.request.user.is_superuser
    
# @staff_member_required(login_url='/login')
# def deletecommodity(request, commodity_slug):
#     commodity = get_object_or_404(Commodity, slug=commodity_slug)
#     try:
#         commodity.delete()
#         messages.success(request, 'Commodity deleted successfully')
#     except Exception as e:
#         messages.error(request, f'Error deleting Commodity: {str(e)}')
#     return redirect('/dashboard')
    
class Project:
    def __init__(self, title, proj_description, status, proj_team, start_date, end_date, Researcher):
        self.title = title
        self.proj_description = proj_description
        self.status = status
        self.proj_team = proj_team
        self.start_date = start_date
        self.end_date = end_date

class Researcher:
    def __init__(self, researcher_id, fname, lname):
        self.researcher_id = researcher_id
        self.fname = fname
        self.lname = lname

def project(request):
    cnx = None
    cursor = None
    try:
        cnx = mysql.connector.connect(user='root', password='',
                                host='localhost', database='testo')

        # create a cursor to execute SQL queries
        cursor = cnx.cursor()

        # execute a SELECT query to fetch data from a table
        query = "SELECT p.proj_id, p.title, p.proj_description, p.status, r.researcher_id, r.fname, r.lname, p.start_date, p.end_date FROM project p \
                LEFT JOIN project_proj_team ppt ON p.proj_id = ppt.project_id \
                LEFT JOIN researcher r ON ppt.researcher_id = r.researcher_id \
                ORDER BY p.proj_id ASC"

        cursor.execute(query)

        current_project_id = None
        current_project = None
        projects = []
        for row in cursor.fetchall():
            project_id = row[0]
            if project_id != current_project_id:
                current_project = Project(row[1], row[2], row[3], [], row[7], row[8], None)
                projects.append(current_project)
                current_project_id = project_id
            researcher_id = row[4]
            if researcher_id is not None:   
                researcher = Researcher(row[4], row[5], row[6])
                current_project.proj_team.append(researcher)

        # Filter by ONGOING status
        query_ongoing = "SELECT p.proj_id, p.title, p.proj_description, p.status, r.researcher_id, r.fname, r.lname, p.start_date, p.end_date \
                                FROM project p \
                                LEFT JOIN project_proj_team ppt ON p.proj_id = ppt.project_id \
                                LEFT JOIN researcher r ON ppt.researcher_id = r.researcher_id \
                                WHERE p.status = 'ongoing'\
                                ORDER BY p.proj_id ASC"
        cursor.execute(query_ongoing)
        onprojects = []
        current_proj_id = None
        for row in cursor.fetchall():
            proj_id = row[0]
            if proj_id != current_proj_id:
                # Add a new project to the list
                projecton = Project(row[1], row[2], row[3], [], row[7], row[8], row[0])
                onprojects.append(projecton)
                current_proj_id = proj_id

            researcher_id = row[4]
            if researcher_id is not None:
                researcher = Researcher(row[4], row[5], row[6])
                projecton.proj_team.append(researcher)
            # onprojects.append(projecton)
        # for project in onprojects:
        #     print(project.title)

        # Filter by FINISHED status
        query_completed = "SELECT p.proj_id, p.title, p.proj_description, p.status, r.researcher_id, r.fname, r.lname, p.start_date, p.end_date \
                                FROM project p \
                                LEFT JOIN project_proj_team ppt ON p.proj_id = ppt.project_id \
                                LEFT JOIN researcher r ON ppt.researcher_id = r.researcher_id \
                                WHERE p.status = 'completed'\
                                ORDER BY p.proj_id ASC"
        cursor.execute(query_completed)
        finprojects = []
        current_proj_id = None
        for row in cursor.fetchall():
            proj_id = row[0]
            if proj_id != current_proj_id:
                # Add a new project to the list
                projecton = Project(row[1], row[2], row[3], [], row[7], row[8], row[0])
                finprojects.append(projecton)
                current_proj_id = proj_id

            researcher_id = row[4]
            if researcher_id is not None:
                researcher = Researcher(row[4], row[5], row[6])
                projecton.proj_team.append(researcher)

            # finprojects.append(projecton)
        # for project in finprojects:
        #     print(project.title)
    except mysql.connector.errors.Error as e:
        print(f"An error occurred: {e}")
        projects = None
        onprojects = None
        finprojects = None
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    if projects is not None and onprojects is not None and finprojects is not None:
        context = {
            'projects': projects,
            'onprojects': onprojects,
            'finprojects': finprojects,

        }
    else:
        context = {}
    return render(request, 'projects.html', context)

def onproject(request):
    cnx = None
    cursor = None
    try:
        cnx = mysql.connector.connect(user='root', password='',
                                host='localhost', database='testo')

        # create a cursor to execute SQL queries
        cursor = cnx.cursor()

        # execute a SELECT query to fetch data from a table

        # Filter by ONGOING status
        # Filter by ONGOING status
        query_ongoing = "SELECT p.proj_id, p.title, p.proj_description, p.status, r.researcher_id, r.fname, r.lname, p.start_date, p.end_date \
                                FROM project p \
                                LEFT JOIN project_proj_team ppt ON p.proj_id = ppt.project_id \
                                LEFT JOIN researcher r ON ppt.researcher_id = r.researcher_id \
                                WHERE p.status = 'ongoing'\
                                ORDER BY p.proj_id ASC"
        cursor.execute(query_ongoing)
        onprojects = []
        current_proj_id = None
        for row in cursor.fetchall():
            proj_id = row[0]
            if proj_id != current_proj_id:
                # Add a new project to the list
                projecton = Project(row[1], row[2], row[3], [], row[7], row[8], row[0])
                onprojects.append(projecton)
                current_proj_id = proj_id

            researcher_id = row[4]
            if researcher_id is not None:
                researcher = Researcher(row[4], row[5], row[6])
                projecton.proj_team.append(researcher)
            # onprojects.append(projecton)
        # for project in onprojects:
        #     print(project.title)
    except mysql.connector.errors.Error as e:
        print(f"An error occurred: {e}")
        onprojects = None
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
    if onprojects is not None:
        context = {'onprojects': onprojects}
    else:
        context = {}
    return render(request, 'onproject.html', context)

def finproject(request):
    cnx = None
    cursor = None
    try:
        cnx = mysql.connector.connect(user='root', password='',
                                host='localhost', database='testo')

        # create a cursor to execute SQL queries
        cursor = cnx.cursor()

        # execute a SELECT query to fetch data from a table

        # Filter by ONGOING status
        # Filter by ONGOING status
        query_completed = "SELECT p.proj_id, p.title, p.proj_description, p.status, r.researcher_id, r.fname, r.lname, p.start_date, p.end_date \
                                FROM project p \
                                LEFT JOIN project_proj_team ppt ON p.proj_id = ppt.project_id \
                                LEFT JOIN researcher r ON ppt.researcher_id = r.researcher_id \
                                WHERE p.status = 'completed'\
                                ORDER BY p.proj_id ASC"
        cursor.execute(query_completed)
        finprojects = []
        current_proj_id = None
        for row in cursor.fetchall():
            proj_id = row[0]
            if proj_id != current_proj_id:
                # Add a new project to the list
                projecton = Project(row[1], row[2], row[3], [], row[7], row[8], row[0])
                finprojects.append(projecton)
                current_proj_id = proj_id

            researcher_id = row[4]
            if researcher_id is not None:
                researcher = Researcher(row[4], row[5], row[6])
                projecton.proj_team.append(researcher)
            # onprojects.append(projecton)
        # for project in onprojects:
        #     print(project.title)
    except mysql.connector.errors.Error as e:
        print(f"An error occurred: {e}")
        finprojects = None
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
    
    if finprojects is not None:
        context = {'finprojects': finprojects}
    else:
        context = {}
    return render(request, 'finproject.html', context)

# def onprojectdetail(request, project_slug):
#     onprojects = get_object_or_404(Project, slug=project_slug)
#     return render(request, 'ondetail.html', {'onprojects': onprojects})

# def finprojectdetail(request, project_slug):
#     finprojects = get_object_or_404(Project, slug=project_slug)
#     return render(request, 'findetail.html', {'finprojects': finprojects})

# class ProjectCreateView(LoginRequiredMixin, CreateView):
#     model = Project
#     form_class = ProjectForm
#     template_name = 'createproject.html'
#     success_url = reverse_lazy('dashboard')

#     def form_valid(self, form):
#         slug = slugify(form.cleaned_data['title'])
#         count = 1
#         while Project.objects.filter(slug=slug).exists():
#             slug = f"{slug}-{count}"
#             count += 1
#         form.instance.slug = slug
#         return super().form_valid(form)

# class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Project
#     form_class = ProjectForm
#     success_url = reverse_lazy('dashboard')
#     template_name = 'commodity_update.html'

#     def test_func(self):
#         return self.request.user.is_staff or self.request.user.is_superuser

# @staff_member_required(login_url='/login')
# def projectdelete(request, project_slug):
#     project = get_object_or_404(Category, slug=project_slug)
#     try:
#         project.delete()
#         messages.success(request, 'project deleted successfully')
#     except Exception as e:
#         messages.error(request, f'Error deleting project: {str(e)}')
#     return redirect('/dashboard')

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

from django.contrib.auth import get_user_model

@staff_member_required(login_url='/login')
def dashboard(request):
    # commodity = Commodity.objects.all()
    slides = Slide.objects.all()
    posts = Post.objects.all()
    categories = Category.objects.all()
    # projects = Project.objects.all()
    try:
        consortium = About.objects.get(id=1)
    except About.DoesNotExist:
        consortium = None
    organizations = Organization.objects.all()

    User = get_user_model()
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
                # 'commodity': commodity,
                'categories': categories,
                # 'projects' : projects,
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
    albums = Album.objects.all()
    context = {
        'photos': photos,
        'albums': albums
        }
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

class albumupdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy('dashboard')
    template_name = 'createcategory.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

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
    form_class = PhotoForm
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
        consortium = About.objects.get(id=1)
    except About.DoesNotExist:
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
    cnx = mysql.connector.connect(user='root', password='',
                              host='localhost', database='test101')

    # create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # execute a SELECT query to fetch data from a table
    query = "SELECT * FROM commodity"
    cursor.execute(query)
    commodity = cursor.fetchall()
    context = {'commodity': commodity}
    return render(request, 'dash-commodities.html', context)

def dashcommunity(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    context = {'posts': posts, 'categories': categories}
    return render(request, 'dash-community.html', context)

def dashproject(request):
    cnx = mysql.connector.connect(user='root', password='',
                              host='localhost', database='test101')

    # create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # execute a SELECT query to fetch data from a table
    query = "SELECT * FROM project"
    cursor.execute(query)
    projects = cursor.fetchall()
    context = {'projects': projects}
    return render(request, 'dash-projects.html', context)

def dashservices(request):
    cnx = mysql.connector.connect(user='root', password='',
                              host='localhost', database='test101')

    # create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # execute a SELECT query to fetch data from a table
    query = "SELECT * FROM commodity"
    cursor.execute(query)
    commodity = cursor.fetchall()
    context = {'services': services}
    return render(request, 'dash-services.html', context)

def dashuser(request):
    User = get_user_model()
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