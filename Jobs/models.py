from django.db import models

class Upload_Resume(models.Model):
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    
