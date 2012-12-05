from django.conf import settings
from django.utils.translation import ugettext_noop as _
from django.db.models import signals 

if "JOININ.notification" in settings.INSTALLED_APPS:
    from JOININ.notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("successful_join", _("Succeed to join a group"),\
        	 _("You have successfully joined in a group."))
        
    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"