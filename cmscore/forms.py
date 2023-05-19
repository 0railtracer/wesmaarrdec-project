from django.forms import ModelForm
from django import forms
from .models import *
from cmsblg.models import *
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory


def generate_unique_slug(model, title):
    slug = slugify(title)
    unique_slug = slug
    num = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug

class PostImagesForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'delete'}))

    class Meta:
        model = PostImages
        fields = ['images']
        widgets = {
            'images': forms.FileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        }

PostImagesFormSet = inlineformset_factory(Post, PostImages, form=PostImagesForm, extra=1, can_delete=True)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'intro', 'body']
        labels = {
            'title': 'Title',
            'category': 'Category',
            'intro': 'Introduction',
            'body': 'Content'
        }

    def form_valid(self, form):
        form.instance.author = self.request.user
        slug = slugify(form.cleaned_data['title'])
        count = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{slug}-{count}"
            count += 1
        form.instance.slug = slug
        return super().form_valid(form)

class ConsortiumForm(ModelForm):
    class Meta:
        model = About
        fields = ['About_name','About_image','consortium_desc', 'consortium_objectives','vision','mission']
        labels = '__all__'
        
class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        labels = {
            'dostpcaarrd_ExDi_name': 'DOST-PCAARRD/EXECUTIVE-DIRECTOR',
            'dostpcaarrd_ExDi_img': 'DOST-PCAARRD/EXECUTIVE-DIRECTOR_2X2-IMG',
            'wmsupres_rrdcchair_exdi_name': 'WMSU-President/RDCC-CHAIR/EXCECUTIVE-DIRECTOR',
            'wmsupres_rrdcchair_exdi_img': 'WMSU-President/RDCC-CHAIR/EXCECUTIVE-DIRECTOR_2X2-IMG',
            'depu_di_name': 'RRDCC-VICE-CHAIR/DEPUTY-DIRECTOR',
            'depu_di_img': 'RRDCC-VICE-CHAIR/DEPUTY-DIRECTOR_2X2-IMG',
            'EXBM_ZSCMST_name': 'EXECUTIVE-BOARD-MEMBER-ZSCMST',
            'EXBM_ZSCMST_img': 'EXECUTIVE-BOARD-MEMBER-ZSCMST_2X2-IMG',
            'EXBM_DA_RFO_IX_name': 'EXECUTIVE-BOARD-MEMBER-DA_RFO_IX',
            'EXBM_DA_RFO_IX_img': 'EXECUTIVE-BOARD-MEMBER-DA_RFO_IX_2X2-IMG',
            'EXMB_DA_BAR_name': 'EXECUTIVE-BOARD-MEMBER-DA_BAR',
            'EXBM_DA_BAR_img': 'EXECUTIVE-BOARD-MEMBER-DA_BAR_2X2-IMG',
            'EXBM_JHCSC_name': 'EXECUTIVE-BOARD-MEMBER-JHCSC',
            'EXBM_JHCSC_img': 'EXECUTIVE-BOARD-MEMBER-JHCSC_2X2-IMG',
            'EXBM_PHILFIDA_name': 'EXECUTIVE-BOARD-MEMBER-PHILFIDA',
            'EXBM_PHILFIDA_img': 'EXECUTIVE-BOARD-MEMBER-PHILFIDA_2X2-IMG',
            'WESMAARRDEC_Dir_name': 'WESMAARRDEC-DIRECTOR',
            'WESMAARRDEC_Dir_img': 'WESMAARRDEC-DIRECTOR_2X2-IMG',
            'Clus_Coord_R_and_D_name': 'CLUSTER-COORDINATOR-RESEARCH-AND-DEVELOPMENT',
            'Clus_Coord_R_and_D_img': 'CLUSTER-COORDINATOR-RESEARCH-AND-DEVELOPMENT_2X2-IMG',
            'Clus_Coord_Tech_Trans_name': 'CLUSTER-COORDINATOR-TECHNOLOGY-TRANSFER',
            'Clus_Coord_Tech_Trans_img': 'CLUSTER-COORDINATOR-TECHNOLOGY-TRANSFER_2X2-IMG',
            'Clus_Coord_ICT_name': 'CLUSTER-COORDINATOR-INFORMATION-COMMUNICATION-TECHNOLOGY',
            'Clus_Coord_ICT_img': 'CLUSTER-COORDINATOR-INFORMATION-COMMUNICATION-TECHNOLOGY_2X2-IMG',
            'Clus_Coord_Sci_Com_name': 'CLUSTER-COORDINATOR-SCIENCE-COMMUNITCATION',
            'Clus_Coord_Sci_Com_img': 'CLUSTER-COORDINATOR-SCIENCE-COMMUNITCATION_2X2-IMG',
            'Management_sup1_name': 'STAFF-SECRETARIAT-1',
            'Management_sup1_img': 'STAFF-SECRETARIAT-1_2X2-IMG',
            'Management_sup2_name': 'STAFF-SECRETARIAT-2',
            'Management_sup2_img': 'STAFF-SECRETARIAT-2_2X2-IMG',
            'Management_sup3_name': 'STAFF-SECRETARIAT-3',
            'Management_sup3_img': 'STAFF-SECRETARIAT-3_2X2-IMG',
            'Management_sup4_name': 'STAFF-SECRETARIAT-4',
            'Management_sup4_img': 'STAFF-SECRETARIAT-4_2X2-IMG',
        }

# class CommodityForm(ModelForm):
#     class Meta:
#         model = Commodity
#         fields = ['name', 'detail', 'image']
#         labels = {
#             'name': 'Name',
#             'detail': 'Detail',
#             'image': 'Image',
#         }

class SlideForm(ModelForm):
    class Meta:
        model = Slide
        fields = '__all__'

# class ProjectForm(ModelForm):
#     class Meta:
#         model = Project
#         fields = ['title', 'description', 'researcher', 'image1', 'image2', 'status']
#         labels = {
#             'title': 'Title',
#             'description': 'Description',
#             'researcher': 'Researcher',
#             'status': 'Status',
#             'image1': 'Image1',
#             'image2': 'Image2',
#         }

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'caption', 'event_id', 'proj_id', 'prog_id', 'project', 'program']
        labels = {
            'name': 'Name',
            'caption': 'Caption',
            'event_id': 'Event Id',
            'proj_id': 'Project Id',
            'prog_id': 'Program Id',
            'project': 'Related Project',
            'program': 'Related Program',
        }

class AlbumPhotoImagesForm(forms.ModelForm):
    class Meta:
        model = AlbumPhotoImages
        fields = ['images']
        widgets = {
            'images': forms.FileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        }
        
AlbumPhotoImagesFormSet = inlineformset_factory(AlbumPhoto, AlbumPhotoImages, form=AlbumPhotoImagesForm, extra=1, can_delete=True)

class PhotoForm(forms.ModelForm):
    class Meta:
        model = AlbumPhoto
        fields = ['name','caption','carousel','events','news','album']
        labels = '__all__'
        widgets = {
                'carousel': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_carousel'}),
                'events': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_events'}),
                'news': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_news'}),
        }

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['name', 'content_type', 'content_detail']
        labels = '__all__'

class LoginbgForm(forms.ModelForm):
    class Meta:
        model = Loginbg
        fields = '__all__'
        labels = '__all__'