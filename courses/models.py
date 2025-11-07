from django.db import models
from users.models import Student,Instructor
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify




class Subject(models.Model):
    title = models.CharField(max_length=250)
    slug  = models.SlugField(max_length=250, unique=True)
    
    
    class Meta:
        ordering = ['title']
        
    def __str__(self) -> str:
        return str(self.title)   
    
 



class Course(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AV', 'Available'
        DEREFT    = 'DF', 'Draft'
    instructor = models.ForeignKey(Instructor, related_name='courses_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug  = models.SlugField(max_length=250, unique=True, blank=True, null=True) 
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.AVAILABLE)
    students = models.ManyToManyField(Student, related_name='enrolled_courses', blank=True)

    class Meta:

        ordering = ['-created']

        
    def __str__(self) -> str:
        return str(self.title)  
    
    
    def save(self,*args,**kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            counter = 0
            unique_slug = base_slug
            
            while Course.objects.filter(slug=unique_slug).exists():
                counter += 1
                unique_slug = f"{base_slug} - {counter}"
            
            self.slug = unique_slug
        super().save(*args,**kwargs)



class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)    
    title  = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return str(self.title) 
    
    
    
    


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('text', 'file', 'image', 'video')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    
    



class ItemBase(models.Model):
    instructor = models.ForeignKey(Instructor, related_name='%(class)s_related', on_delete=models.CASCADE)    
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
    def __str__(self) -> str:
        return str(self.title)




class Text(ItemBase):
    content = models.TextField()  

class File(ItemBase):
    file = models.FileField(upload_to='files')    
    
class Image(ItemBase):
    image = models.ImageField(upload_to='images')  
    
class Video(ItemBase):
    video = models.URLField()      