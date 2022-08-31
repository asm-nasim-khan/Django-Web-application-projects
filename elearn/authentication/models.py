from django.db import models

class Courses(models.Model):
    name = models.CharField('Course Name',max_length=120)
    language = models.CharField('Language',max_length=20)
    level = models.CharField('Level',max_length=10)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



class Cart(models.Model):
    course = models.CharField('C name',max_length=120)
    course_key = models.ForeignKey(Courses,blank=True,null=True,on_delete=models.CASCADE)
# Create your models here.

