from django.db import models
import constants


class Tag(models.Model):
    class Meta:
        verbose_name_plural = 'Tags'
    
    class Types(models.TextChoices):
        EXAM = 'EXAM', 'exam'
        STREAM = 'STREAM', 'stream'
        SKILL = 'SKILL', 'skill'
    
    name = models.CharField(max_length=25, unique=True, null=False, default='default-tag')
    type = models.CharField(max_length=20, choices=Types.choices, default=Types.SKILL)
    # courses[]

    def __str__(self):
        return f"Tag: {self.name}"
 

class Exam(Tag):
    class Meta:
        proxy = True
        verbose_name_plural = 'Exams'

    def save(self, *args, **kwargs):
        self.type = Tag.Types.EXAM
        return super().save(*args, **kwargs)
    
    class ExamManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(type=Tag.Types.EXAM)

    objects = ExamManager()


class Stream(Tag):
    class Meta:
        proxy = True
        verbose_name_plural = 'Streams'

    def save(self, *args, **kwargs):
        self.type = Tag.Types.STREAM
        return super().save(*args, **kwargs)
    
    class StreamManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(type=Tag.Types.STREAM)

    objects = StreamManager()


class Skill(Tag):
    class Meta:
        proxy = True
        verbose_name_plural = 'Skills'

    def save(self, *args, **kwargs):
        self.type = Tag.Types.SKILL
        return super().save(*args, **kwargs)
    
    class SkillManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(type=Tag.Types.SKILL)

    objects = SkillManager()


class Location(models.Model):
    class Meta:
        verbose_name_plural = 'Locations'
        
    name = models.CharField(max_length=255, unique=True, null=False)
    image = models.ImageField(upload_to=constants.IMAGE_UPLOAD_PATH, blank=True, null=True)
    
    def __str__(self):
        return f"Location: {self.name}"


class Interest(models.Model):
    class Meta:
        verbose_name_plural = 'Interests'
        
    name = models.CharField(max_length=25, unique=True, null=False, default='default-interest')
    image = models.ImageField(upload_to=constants.IMAGE_UPLOAD_PATH, blank=True, null=True)
    
    def __str__(self):
        return f"Interest: {self.name}"
   

class EducationLevel(models.Model):
    class Meta:
        verbose_name_plural = 'Education Levels'
        
    name = models.CharField(max_length=25, unique=True, null=False, default='default-edu-level')
    image = models.ImageField(upload_to=constants.IMAGE_UPLOAD_PATH, blank=True, null=True)
    
    def __str__(self):
        return f"Education Level: {self.name}"