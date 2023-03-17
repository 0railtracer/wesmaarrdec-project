from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Slide(models.Model):
    # slide_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    detail = models.TextField()
    image = models.ImageField(upload_to='Slide/', blank=False, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    # class Meta:
    #     # managed = False
    #     # db_table = 'cmscore_slide'

    def __str__(self):
        return self.name

class Commodity(models.Model):
    # com_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    detail = models.TextField()
    image = models.ImageField(upload_to='Commodities/', blank=False, null=True)
    slide = models.BooleanField(default=False)
    produced_by = models.CharField(max_length=255, blank=True, null=True)
    geolat = models.FloatField(blank=True, null=True)
    geolong = models.FloatField(blank=True, null=True)
    # iec = models.ForeignKey('IecMaterial', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Commodities'
        # managed = False
        # db_table = 'commodity'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/%s/' % self.slug
    
class Consortium(models.Model):
    # consortium_id = models.AutoField(primary_key=True)
    consortium_code = models.CharField(max_length=50)
    consortium_name = models.CharField(max_length=255)
    consortium_address = models.CharField(max_length=255)
    geolat = models.FloatField(blank=True, null=True)
    geolong = models.FloatField(blank=True, null=True)
    consortium_logo = models.ImageField(upload_to='Consortium', blank=False, null=True)
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    consortium_desc = models.TextField(blank=True, null=True)
    consortium_objectives = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    fb_url = models.CharField(max_length=255, blank=True, null=True)
    yt_url = models.CharField(max_length=255, blank=True, null=True)
    telno = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)
   
   
    # class Meta:
    #     managed = False
        # db_table = 'consortium'

    def __str__(self):
        return self.consortium_code
    
    def save(self, *args, **kwargs):
        if self.pk is None and Consortium.objects.exists():
            # Only allow one object to be created
            raise ValidationError("You can only create one Consortium object")
        super().save(*args, **kwargs)
    
    
class Organization(models.Model):
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    detail = models.TextField()
    image1 = models.ImageField(upload_to='Organization/', blank=False, null=True)
    image2 = models.ImageField(upload_to='Organization/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Project(models.Model):
    ONGOING = 'ongoing'
    FINISHED = 'finished'

    CHOICE_STATUS = (
        (ONGOING, 'ongoing'),
        (FINISHED, 'finished')
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    researcher = models.TextField()
    status = models.CharField(max_length=20, choices=CHOICE_STATUS, default=ONGOING)
    image1 = models.ImageField(upload_to='Project/', blank=False, null=True)
    image2 = models.ImageField(upload_to='Project/', blank=False, null=True)
    slide = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return '/%s/' % self.slug

class Album(models.Model):
    # album_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, blank=True, null=True)
    event_id = models.IntegerField(blank=True, null=True)
    proj_id = models.IntegerField(blank=True, null=True)
    prog_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField( auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField( auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    # class Meta:
    #     managed = False
        # db_table = 'album'

    def __str__(self):
        return self.name
    
    def get_cover_image_url(self):
        try:
            return self.photos.first().img.url
        except AttributeError:
            return None
    
class AlbumPhoto(models.Model):
    # photo_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, blank=True, null=True)
    img = models.ImageField(upload_to='AlbumPhoto', blank=False, null=True)
    slide = models.BooleanField(default=False)
    carousel = models.BooleanField(default=False)
    album = models.ForeignKey(Album, models.DO_NOTHING, related_name='photos', blank=True, null=True)
    created_at = models.DateTimeField( auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField( auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    # class Meta:
    #     managed = False
        # db_table = 'album_photo'

    def __str__(self):
        return self.name
    
class Content(models.Model):
    content_title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255)
    content_detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content_title
    
