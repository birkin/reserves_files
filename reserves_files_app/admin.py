from django.contrib import admin
from easyborrow_stats_app.models import RequestEntry, HistoryEntry


# <https://docs.djangoproject.com/en/2.2/topics/db/multi-db/>

class MultiDBModelAdmin(admin.ModelAdmin):

    using = 'ezborrow_legacy'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    ## end class MultiDBModelAdmin()


# class RequestEntryAdmin(admin.ModelAdmin):
class RequestEntryAdmin( MultiDBModelAdmin ):

    list_display = [ 'id', 'title', 'created', 'barcode', 'request_status' ]
    # list_display = [ 'title', 'wc_accession', 'created' ]

    # list_filter = [ 'created' ]

    # date_hierarchy = 'created'  # generates error: "Database returned an invalid datetime value. Are time zone definitions for your database installed?"

    search_fields = [ 'created']

    ordering = [ 'title' ]

    readonly_fields = [ 'created' ]

    # prepopulated_fields = { "slug": ("project_name",) }

    save_on_top = True

    ## end class RequestEntryAdmin()

admin.site.register( RequestEntry, RequestEntryAdmin )


class HistoryEntryAdmin( MultiDBModelAdmin ):

    list_display = [ 'request', 'svc_name', 'svc_action', 'svc_result', 'note', 'working_timestamp' ]

    readonly_fields = [ 'request' ]

    save_on_top = True

    ## end class HistoryEntryAdmin()

admin.site.register( HistoryEntry, HistoryEntryAdmin )

