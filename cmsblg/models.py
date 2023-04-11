from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    # blgcat_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'
        # managed = False
        # db_table = 'cmsblg_category'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % self.slug

class Post(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )
    # blgpost_id = models.AutoField(primary_key=True)
    # author = models.ForeignKey(User, null=True, blank=True, related_name='posts', on_delete=models.CASCADE )
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    intro = models.TextField()
    body = models.TextField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
        # managed = False
        # db_table = 'cmsblg_post'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)

# class Comment(models.Model):
#     post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
#     name = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
#     email = models.EmailField()
#     body = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.body
    
    #upgrade comment model
class Comment(models.Model):
    # name = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    # created_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'

    @property
    def is_parent(self):
        return not self.parent
    
    class Meta:
        ordering = ['-created_at']
        # managed = False
        # db_table = 'cmsblg_comment'

class Fact(models.Model):
    # faq_id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    img = models.ImageField(upload_to='Fact', blank=False, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    # class Meta:
    #     managed = False
        # db_table = 'cmsblg_faq'

    def __str__(self):
        return self.question