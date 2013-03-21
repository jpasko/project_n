from django.core.management.base import BaseCommand, CommandError
from accounts.models import Domains

class Command(BaseCommand):
    args = 'None'
    help = 'Checks the Domains database; adds any new custom domains to heroku'

    def handle(self, *args, **options):
        all_domains = Domains.objects.all()
        for domain in all_domains:
            self.stdout.write('*.%s\n' % domain.domain)
