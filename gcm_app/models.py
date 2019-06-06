from django.db import models


# Model for the Students and Projects
class StudentProject(models.Model):
    PROJECT_TYPES = (
        ('Portfolio', 'Dev Portfolio'),
        ('Passion', 'Passion Project'),
        ('Other', 'Other Project'),
    )
    project_student_name = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200, choices=PROJECT_TYPES)
    project_url = models.CharField(max_length=500)
    project_last_checked = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Student Projects"

    def __str__(self):
        return (self.project_student_name + " : " + self.project_name)
