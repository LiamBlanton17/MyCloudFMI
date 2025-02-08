from django.db import models

#Create your models here.

class User(models.Model):
    username = models.CharField(unique=True)
    email = models.EmailField(primary_key=True, unique=True)
    password = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    root_path = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True) 
    users = models.ManyToManyField(User, related_name='UserProject')

    def __str__(self):
        return self.name
    
class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='collaborator')
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.project}'
    
    class Meta: 
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"

    class Folder(models.Model):
        name = models.CharField(max_length=255)
        path = models.CharField(max_length=512)
        parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, null=True, related_name='subfolders')
        project = models.ForeignKey(Project, on_delete=models.CASCADE)
        date_created = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Folder: {self.name} ({self.path})"
        
    class File(models.Model):
        name = models.CharField(max_length=255)
        path = models.CharField(max_length=512)
        size = models.PositiveIntegerField() #File size in bytes
        file_type = models.CharField(max_length=50)
        date_created = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"File: {self.name ({self.size} bytes, {self.file_type})}"