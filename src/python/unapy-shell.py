#!/usr/bin/python
"""
https://github.com/django/django/blob/master/django/core/management/commands/shell.py

Modified a bit...
"""
import code, os
# Set up a dictionary to serve as the environment for the shell, so
# that tab completion works on objects that are imported at runtime.
# See ticket 5082.
imported_objects = {}
use_plain = False
try: # Try activating rlcompleter, because it's handy.
    import readline
except ImportError:
    pass
else:
    # We don't have to wrap the following import in a 'try', because
    # we already know 'readline' was imported successfully.
    import rlcompleter
    readline.set_completer(rlcompleter.Completer(imported_objects).complete)
    readline.parse_and_bind("tab:complete")

# We want to honor both $PYTHONSTARTUP and .pythonrc.py, so follow system
# conventions and get $PYTHONSTARTUP first then import user.
if not use_plain:
    pythonrc = os.environ.get("PYTHONSTARTUP")
    if pythonrc and os.path.isfile(pythonrc):
        try:
            execfile(pythonrc)
        except NameError:
            pass
    # This will import .pythonrc.py as a side-effect
    import user
import unapy
from unapy import cli
from unapy.commands import at as AT
imported_objects.update({
  'AT': AT,
  'unapy': unapy,
  'cli': cli,
  'link': cli.get_link( ),
})
code.interact(local=imported_objects)

#####
# EOF
