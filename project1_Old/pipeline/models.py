from django.db import models


class Frontpage(models.Model):
	frontpage_text = models.CharField(max_length=200)
	frontpage_url = models.CharField(max_length=200)

	def __unicode__(self): # __str__ on Python 3
		return self.frontpage_text


class Pipeline(models.Model):
	project_code_text = models.CharField(max_length=200)
	project_name = models.CharField(max_length=200)
	start_date = models.DateTimeField('start_date')
	end_date = models.DateTimeField('end_date')
	project_leader = models.CharField(max_length=200)
	project_staffing = models.CharField(max_length=200)
	project_status = models.CharField(max_length=200)
	project_team = models.CharField(max_length=200)

	def __unicode__(self): # __str__ on Python 3
		return self.project_name