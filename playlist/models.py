from django.db import models

class ListItems(models.Model):
	list_id=models.CharField(max_length=250,null=True,blank=True)
	
	def __unicode__(self):
		return str(self.list_id)
