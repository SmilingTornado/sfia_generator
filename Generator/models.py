from django.db import models

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.name.__str__()

class Level(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    description = models.TextField(blank = True, null = True)

class SkillJSON(models.Model):
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.file.name.__str__()