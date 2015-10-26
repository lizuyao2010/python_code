import sys,os,linecache
import signal,functools #下面会用到的两个库 

def trace(f):
  def globaltrace(frame, why, arg):
    if why == "call": return localtrace
    return None
  def localtrace(frame, why, arg):
    if why == "line":
      # record the file name and line number of every trace
      filename = frame.f_code.co_filename
      lineno = frame.f_lineno
      bname = os.path.basename(filename)
      print "{}({}): {}".format(  bname,
                    lineno,
                    linecache.getline(filename, lineno)),
    return localtrace
  def _f(*args, **kwds):
    sys.settrace(globaltrace)
    result = f(*args, **kwds)
    sys.settrace(None)
    return result
  return _f



class TimeoutError(Exception): pass #定义一个Exception，后面超时抛出 

def timeout(seconds, error_message = 'Function call timed out'):
  def decorated(func):
    def _handle_timeout(signum, frame):
      raise TimeoutError(error_message)
    def wrapper(*args, **kwargs):
      signal.signal(signal.SIGALRM, _handle_timeout)
      signal.alarm(seconds)
      try:
        result = func(*args, **kwargs)
      finally:
        signal.alarm(0)
      return result
    return functools.wraps(func)(wrapper)
  return decorated