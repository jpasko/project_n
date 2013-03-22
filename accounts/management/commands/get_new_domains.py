from django.core.management.base import BaseCommand, CommandError
from accounts.models import Domains

class Command(BaseCommand):
    args = 'None'
    help = 'Checks the Domains database; adds any new custom domains to heroku'

    def handle(self, *args, **options):
        new_domains = Domains.objects.filter(pending=True)
        for domain in new_domains:
            domain.pending = False
            domain.save()
            self.stdout.write('*.%s\n' % domain.domain)
