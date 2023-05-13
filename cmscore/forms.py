from django.forms import ModelForm
from django import forms
from .models import *
from cmsblg.models import *
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'intro', 'body', 'image']
        labels = {
            'title': 'Title',
            'category': 'Category',
            'intro': 'Introduction',
            'body': 'Content',
            'image': 'Image'
        }
    
class ConsortiumForm(ModelForm):
    class Meta:
        model = About
        fields = '__all__'
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
        fields = '__all__'
        labels = '__all__'

class PhotoForm(forms.ModelForm):
    class Meta:
        model = AlbumPhoto
        fields = '__all__'
        labels = '__all__'
        widgets = {
                'slide': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_slide'}),
                'carousel': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_carousel'}),
        }

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'
        labels = '__all__'