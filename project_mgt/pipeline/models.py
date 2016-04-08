from django.db import models

class Pipeline(models.Model):
    project_code_text = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    start_date = models.DateField('start_date')
    end_date = models.DateField('end_date')
    project_leader = models.CharField(max_length=200)
    project_staffing = models.CharField(max_length=200)
    project_status = models.CharField(max_length=200)
    project_team = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):  # __str__ on Python 3
        return u'%s %s %s' % (self.id, self.project_name, self.active)