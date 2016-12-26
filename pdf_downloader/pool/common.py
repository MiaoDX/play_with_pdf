#-*- coding: utf-8 -*-
def show_state(func):        
  
    def run(*argv):
        print "Enter %s ..." % func.__name__
        if argv:
            ret = func(*argv)
        else:
            ret = func()
        print "Goodby from  %s." % func.__name__
        return ret

    return run