#-------------------------------------------------------------------------------
#
#   PyGUI - Facilities for compatibility across Python versions
#
#-------------------------------------------------------------------------------

try:
    from builtins import set
except ImportError:
    from sets import Set as set
