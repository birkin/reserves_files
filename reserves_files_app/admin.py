from django.contrib import admin
from reserves_files_app.models import Match


class MatchAdmin( admin.ModelAdmin ):

    list_display = ['id', 'filename', 'course_code', 'path', 'working_timestamp']

    readonly_fields = [ 'working_timestamp', 'id' ]

    search_fields = [ 'id', 'filename', 'course_code', 'path', 'working_timestamp' ]

    date_hierarchy = 'working_timestamp'

    save_on_top = True



admin.site.register( Match, MatchAdmin )
