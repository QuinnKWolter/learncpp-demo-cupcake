"""Linux child-process limits, applied before exec without thread-unsafe preexec_fn."""
import math
import os
import resource
import sys

seconds = math.ceil(float(sys.argv[1])) + 1
resource.setrlimit(resource.RLIMIT_CPU, (seconds, seconds))
resource.setrlimit(resource.RLIMIT_AS, (768 * 1024**2, 768 * 1024**2))
# Allows compiler artifacts; the parent's watchdog enforces the smaller output limit.
resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024**2, 16 * 1024**2))
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
os.execvpe(sys.argv[2], sys.argv[2:], os.environ)
