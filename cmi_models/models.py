from django.db import models
from django.conf import settings
from auth_user.models import User
# Create your models here.

class Consortium(models.Model):
    consortium_id = models.AutoField(primary_key=True)
    consortium_code = models.CharField(max_length=50)
    consortium_name = models.CharField(max_length=255)
    consortium_address = models.CharField(max_length=255)
    geolat = models.FloatField(blank=True, null=True)
    geolong = models.FloatField(blank=True, null=True)
    consortium_logo = models.ImageField(upload_to='consortium_logos/')
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    consortium_desc = models.TextField(blank=True, null=True)
    consortium_objectives = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    fb_url = models.URLField(max_length=255, blank=True, null=True)
    yt_url = models.URLField(max_length=255, blank=True, null=True)
    telno = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.consortium_code
    
    def snippet(self):
        return self.consortium_desc[:120] + '...'

    def snippetname (self):
        return self.consortium_name[:27] + '...'

    class Meta:
        db_table = "consortium"


class CMI(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

    CHOICE_STATUS = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )
    agency_id = models.AutoField(primary_key=True)
    agency_code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    is_cmi= models.BooleanField(default=True)
    consortium_id = models.ForeignKey(Consortium, related_name="+", on_delete=models.CASCADE)
    # consortium_acronym = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    geolat = models.FloatField(blank=True, null=True)
    geolong = models.FloatField(blank=True, null=True)
    logo = models.ImageField(upload_to='cmi_logos/')
    # mission = models.TextField(blank=True, null=True)
    # vision = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    # consortium_objectives = models.TextField(blank=True, null=True)
    # fb_url = models.URLField(max_length=255, blank=True, null=True)
    # yt_url = models.URLField(max_length=255, blank=True, null=True)
    contact_no = models.CharField(max_length=70, blank=True, null=True)
    telno = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, choices=CHOICE_STATUS, default=ACTIVE)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.agency_code
    
    def snippet(self):
        return self.detail[:120] + '...'

    def snippetname (self):
        return self.name[:27] + '...'

    class Meta:
        db_table = "cmi"


class Commodity(models.Model):
    com_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cmi_name = models.ForeignKey(CMI, related_name="commodities",verbose_name = "CMI", on_delete=models.CASCADE)
    detail = models.TextField(null=True, blank=True,)
    img = models.ImageField(upload_to='com_img/')
    produced_by = models.TextField(null=True, blank=True,)
    geolat = models.FloatField(null=True, blank=True,)
    geolong = models.FloatField(null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def snippet(self):
        return self.detail[:120] + '...'


    class Meta:
        db_table = "commodity"


class IecMaterial(models.Model):
    iec_id = models.AutoField(primary_key=True)
    iec_type = models.CharField(max_length=100, null=True, blank=True,)
    title = models.CharField(max_length=255)
    commodity = models.ForeignKey(Commodity, null=True, blank=True, related_name='iecmaterials', on_delete=models.CASCADE)
    target_audience = models.CharField(max_length=100, null=True, blank=True,)
    designed_by = models.CharField(max_length=100, null=True, blank=True,)
    content_by = models.CharField(max_length=100, null=True, blank=True,)
    date_published = models.DateField(blank=True, null=True)
    ip = models.CharField(max_length=30,null=True, blank=True,)
    iec_file = models.FileField(upload_to='iec_files/', blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "iecmaterial"


class Researcher(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    CHOICE_SEX = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    researcher_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100, blank=True, null=True)
    cmi = models.ForeignKey(CMI, null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=CHOICE_SEX, default=FEMALE)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='researcher_photo/', blank=True, null=True)
    pds_file = models.FileField(upload_to='researcher_pds/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.lname) +", "+ (self.fname)
        
    class Meta:
        db_table = "researcher"


class Program(models.Model):
    ONGOING = 'ongoing'
    COMPLETED = 'completed'

    CHOICE_STATUS = (
        (ONGOING, 'ongoing'),
        (COMPLETED, 'completed'),
    )

    prog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=CHOICE_STATUS, default=ONGOING)
    prog_description = models.TextField(blank=True, null=True)
    program_leader = models.ForeignKey(Researcher, related_name='+', on_delete=models.CASCADE)
    commodity = models.ManyToManyField(Commodity, blank=True, related_name="prog_com")
    impl_agency = models.ForeignKey(CMI, null=True, blank=True, related_name='programs', on_delete=models.CASCADE)
    co_impl_agency = models.ManyToManyField(CMI, blank=True)
    funding_agency = models.ForeignKey(CMI, null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    duration = models.IntegerField()
    final_impl_date = models.DateField(blank=True, null=True)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    daterequestedext = models.DateField(blank=True, null=True)
    requested_by = models.ForeignKey(Researcher, null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    ext_duration = models.IntegerField(blank=True, null=True)
    date_uploaded = models.DateField(blank=True, null=True)
    prog_file = models.FileField(upload_to='prog_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.prog_description[:130] + '...'


    class Meta:
        db_table = "program"

class ProgramBudget(models.Model):
    progbdg_id = models.AutoField(primary_key=True)
    prog_id = models.ForeignKey(Program, related_name='prog_budg', on_delete=models.CASCADE)
    yr = models.IntegerField(blank=True, null=True)
    fund_source = models.ForeignKey(CMI, related_name='+', on_delete=models.CASCADE)
    ps = models.FloatField(blank=True, null=True)
    mooe = models.FloatField(blank=True, null=True)
    eo = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    
    class Meta:
        db_table = "program_budget"


class Stakeholder(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    CHOICE_SEX = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    stakeholder_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100, blank=True, null=True)
    cmi = models.ForeignKey(CMI, null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    sex = models.CharField(max_length=10, choices=CHOICE_SEX, default=FEMALE)
    dob = models.DateField(blank=True, null=True)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    email_add = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return (self.lname) +", "+ (self.fname)
        
    class Meta:
        db_table = "stakeholder"

class Sdg(models.Model):
    sdg_no = models.AutoField(primary_key=True)
    sdg_title = models.CharField(max_length=100)
    sdg_desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.sdg_title

    class Meta:
        db_table = "sdg"

    def snippet(self):
        return self.sdg_desc[:90] + '...'


class PriorityArea(models.Model):
    priority_id = models.AutoField(primary_key=True)
    area = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.area

    class Meta:
        db_table = "priority_area"



class Project(models.Model):
    ONGOING = 'ongoing'
    COMPLETED = 'completed'

    CHOICE_STATUS = (
        (ONGOING, 'ongoing'),
        (COMPLETED, 'completed'),
    )

    R_AND_D = 'R&D'
    NON_R_AND_D = 'Non-R&D'

    CHOICE_TYPE = (
        (R_AND_D, 'R&D'),
        (NON_R_AND_D, 'Non-R&D'),
    )
    proj_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    prog_id= models.ForeignKey(Program, null=True, blank=True, related_name='proj_prog', on_delete=models.CASCADE)
    proj_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=CHOICE_STATUS, default=ONGOING)
    proj_type = models.CharField(max_length=20, choices=CHOICE_TYPE, default=R_AND_D, verbose_name = "Project Type")
    #proj_type_sub = models.CharField(max_length=20)
    commodity = models.ManyToManyField(Commodity, blank=True, related_name="proj_com")
    proj_leader = models.ForeignKey(Researcher, related_name='proj_leader', on_delete=models.CASCADE, verbose_name = "Project Leader")
    priority = models.ForeignKey(PriorityArea, null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    sdg_no = models.ForeignKey(Sdg, null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    proj_team = models.ManyToManyField(Researcher, blank=True)
    proj_stakeholder = models.ManyToManyField(Stakeholder, blank=True)
    impl_agency = models.ForeignKey(CMI, related_name='projects', on_delete=models.CASCADE)
    co_impl_agency = models.ManyToManyField(CMI, related_name='co_impl_agency', blank=True)
    coop_agency = models.ManyToManyField(CMI, related_name='coop_agency', blank=True)
    fund_agency = models.ForeignKey(CMI, related_name='+', on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    final_impl_date = models.DateField(blank=True, null=True)
    duration = models.CharField(max_length=100)
    approved_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    approved_date = models.DateField(blank=True, null=True)
    daterequestedext = models.DateField(blank=True, null=True)
    requested_by = models.ForeignKey(Researcher, related_name='+', on_delete=models.CASCADE)
    ext_duration = models.IntegerField(blank=True, null=True)
    proj_file = models.FileField(upload_to='project_files/', blank=True, null=True)
    date_uploaded = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "project"


    def snippet(self):
        return self.proj_description[:130] + '...'


class ProjectImplementingSite(models.Model):
    projimp = models.AutoField(primary_key=True)
    proj_id = models.ForeignKey(Project, related_name='proj_imp', on_delete=models.CASCADE)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    geolat = models.FloatField(blank=True, null=True)
    geolong = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.barangay
    
    class Meta:
        db_table = "proj_imp_site"


class ProjectOutput(models.Model):
    PUBLICATION = 'Publication'
    PATENT = 'Patent'
    PROPERTY = 'Property'
    PRODUCT = 'Product'
    PEOPLE = 'People'
    PLACE_PARTNERSHIP = 'Place and Partnership'

    OUTPUT_TYPE = (
        (PUBLICATION, 'Publication'),
        (PATENT, 'Patent'),
        (PROPERTY, 'Property'),
        (PRODUCT, 'Product'),
        (PEOPLE, 'People'),
        (PLACE_PARTNERSHIP, 'Place and Partnership'),
    )

    projout_id = models.AutoField(primary_key=True)
    proj_id = models.ForeignKey(Project, related_name='proj_output', on_delete=models.CASCADE)
    proj_output_type = models.CharField(max_length=100, choices=OUTPUT_TYPE, default=PUBLICATION)
    proj_output_desc = models.TextField(blank=True, null=True)
    iec_id = models.ForeignKey(IecMaterial, related_name='+', blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "proj_output"

class Secretariat(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    CHOICE_SEX = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )

    secretariat_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100)
    consortium_id = models.ForeignKey(Consortium, related_name='+', on_delete=models.CASCADE)
    email_add = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    date_appointed = models.DateField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=CHOICE_SEX, default=FEMALE)
    bach_deg = models.CharField(max_length=100, blank=True, null=True)
    bdyearcompleted = models.IntegerField(blank=True, null=True)
    mas_deg = models.CharField(max_length=100, blank=True, null=True)
    mdyearcompleted = models.IntegerField(blank=True, null=True)
    doc_deg = models.CharField(max_length=100, blank=True, null=True)
    ddyearcompleted = models.IntegerField(blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='secretariat_photo/', blank=True, null=True)
    pds_file = models.FileField(upload_to='secretariat_pds/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return (self.lname) +", "+ (self.fname)
    
    class Meta:
        db_table = "secretariat"

class Team(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    CHOICE_SEX = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    RRDCC = 'Regional Research and Development Coordinating Committee'
    R_DC = 'Research and Development Cluster'
    TTC = 'Technology Transfer Cluster'
    SCC = 'Science Communication Cluster'
    ICTC = 'Information and Communications Technology Cluster'

    CHOICE_TEAM= (
        (RRDCC, 'RRDCC'),
        (R_DC, 'R&DC'),
        (TTC, 'TTC'),
        (SCC, 'SCC'),
        (ICTC, 'ICTC'),
    )
    member_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100)
    cmi = models.ForeignKey(CMI, related_name='team', verbose_name = "CMI", on_delete=models.CASCADE)
    teams = models.CharField(max_length=60)
    email_add = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    date_appointed = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=CHOICE_SEX, default=FEMALE) 
    specialization = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='team_photo/', blank=True, null=True)
    pds_file = models.FileField(upload_to='pds_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return (self.lname) +", "+ (self.fname)
    
    class Meta:
        db_table = 'team'
