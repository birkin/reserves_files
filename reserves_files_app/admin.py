from django.contrib import admin
from reserves_files_app.models import Match


class MatchAdmin( admin.ModelAdmin ):

    list_display = ['id', 'filename', 'course_code', 'created']

    list_filter = [ 'course_code' ]

    readonly_fields = [ 'created', 'id' ]

    search_fields = [ 'id', 'filename', 'course_code', 'created' ]

    date_hierarchy = 'created'

    save_on_top = False

    exclude = [ 'path' ]


admin.site.register( Match, MatchAdmin )
