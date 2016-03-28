'''
Executes the given Python source file under the context of the current 
Django settings
'''
import os
import sys
import traceback
from django.utils import termcolors
from django.core.management.base import BaseCommand

style = termcolors.make_style(fg='green', opts=('bold',))

#===============================================================================
class Command(BaseCommand):
    help = ' '.join([line.strip() for line in __doc__.strip().splitlines()])

    #---------------------------------------------------------------------------
    def add_arguments(self, parser):
        parser.add_argument('args', nargs='+')
    
    #---------------------------------------------------------------------------
    def handle(self, *args, **options):
        script = os.path.abspath(os.path.expandvars(os.path.normpath(args[0])))
        sys.stderr.write('Executing script {}\n'.format(script))
        sys.argv = [script] + list(args[1:])
        sys.path.append(os.path.dirname(script))
        execfile(script, {'__name__': '__main__', '__file__': script})

