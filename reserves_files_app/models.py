import uuid

from django.db import models
from django.utils import timezone


class Match( models.Model ):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False )
    filename = models.CharField( max_length=255 )
    course_code = models.CharField( max_length=50 )
    path = models.TextField()
    # created = models.DateTimeField( auto_now_add=True )
    created = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return str( self.filename )

    class Meta:
        ordering = ['-created']
        verbose_name_plural = "Matches"

    ## end Match()
