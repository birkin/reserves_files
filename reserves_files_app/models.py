import uuid

from django.db import models


class Match( models.Model ):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False )
    filename = models.CharField( max_length=255 )
    course_code = models.CharField( max_length=50 )
    path = models.TextField()
    working_timestamp = models.DateTimeField( auto_now_add=True )
    # working_timestamp = models.DateTimeField(null=True, core=True)

    def __str__(self):
        return str( self.filename )

    # class Meta:
    #     verbose_name_plural = 'matches'

    ## end Match()
