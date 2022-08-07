from django.db import models


class RequestEntry(models.Model):

    # using = 'ezborrow_legacy'

    TIMEPREF_CHOICES = (
        ('quick', 'Quick'),
        ('long', 'Long'),
        ) # ('db_value', 'display_value')

    LOCATION_CHOICES = (
        ('rock', 'Rock'),
        ('sci', 'SciLi'),
        )

    YESNO_CHOICES = (
        ('y', 'Yes'),
        ('n', 'No'),
        )

    id = models.IntegerField(  primary_key=True )
    title = models.CharField( max_length=255 )
    isbn = models.CharField( max_length=13, blank=True )
    # wc_accession = models.IntegerField()
    wc_accession = models.CharField( max_length=20, blank=True )
    bibno = models.CharField( max_length=10, blank=True )
    pref = models.CharField( max_length=5, choices=TIMEPREF_CHOICES, default='quick' )    # 'time_pref' in copy
    loc = models.CharField( max_length=4, choices=LOCATION_CHOICES, default='rock' )      # 'location' in copy
    alt_edition = models.CharField( max_length=1, choices=YESNO_CHOICES, default='y' )    # 'alternate_edition' in copy
    # time_pref = models.CharField(max_length=5, choices=TIMEPREF_CHOICES, radio_admin=True, default='quick')
    # location = models.CharField(max_length=4, choices=LOCATION_CHOICES, radio_admin=True, default='rock')
    # alternate_edition = models.CharField(max_length=1, choices=YESNO_CHOICES, radio_admin=True, default='y')
    volumes = models.CharField( max_length=255, blank=True)
    sfxurl = models.TextField()
    patronid = models.CharField( max_length=7, blank=True )                               # 'patron_id' in copy
    firstname = models.CharField( max_length=120, blank=True )                            # 'patron_firstname' in copy
    lastname = models.CharField( max_length=120, blank=True )                             # 'patron_lastname' in copy
    barcode = models.CharField( max_length=14, blank=True )                               # 'patron_barcode' in copy
    email = models.CharField( max_length=50, blank=True )                                 # 'patron_email' in copy
    group = models.CharField( max_length=20, blank=True )                                 # 'patron_group' in copy
    request_status = models.CharField( max_length=30, default='Not_Yet_Processed' )
    created = models.DateTimeField( blank=True )

    def __str__(self):
        return str( self.id ) + ' ::: ' + self.title

    class Meta:
        managed = False
        # db_table = 'stats_app_request'
        db_table = 'requests'

    ## end RequestEntry()


class HistoryEntry(models.Model):

    # using = 'ezborrow_legacy'

    SERVICENAME_CHOICES = (
        ('inrhode', 'InRhode'),
        ('borrowdirect', 'BorrowDirect'),
        ('virtualcatalog', 'VirtualCatalog'),
        ('illiad', 'Illiad'),
        )

    SERVICEACTION_CHOICES = (
        ('attempt', 'attempt'),
        ('skip', 'skip'),
        )

    history_id = models.IntegerField(  primary_key=True )
    # request = models.ForeignKey(Request)
    request = models.ForeignKey( RequestEntry, on_delete=models.CASCADE )  # so if a RequestEntry record is deleted, all associated history entries for that requestEntry will also be deleted.
    # request = models.ForeignKey(Request, edit_inline=models.TABULAR, num_in_admin=3)
    svc_name = models.CharField(max_length=20, choices=SERVICENAME_CHOICES, null=True, blank=True)
    svc_action = models.CharField(max_length=30, choices=SERVICEACTION_CHOICES, null=True, blank=True)
    svc_result = models.CharField(max_length=50, null=True, blank=True)
    svc_number = models.CharField(max_length=20, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    working_timestamp = models.DateTimeField(null=True)
    # working_timestamp = models.DateTimeField(null=True, core=True)

    def __str__(self):
        return str( self.working_timestamp )

    class Meta:
        managed = False
        verbose_name_plural = 'history entries'
        # db_table = 'stats_app_historyentry'
        db_table = 'history'

    ## end HistoryEntry()
