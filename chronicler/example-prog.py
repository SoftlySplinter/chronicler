import time
import random
import sys

def syslogtime():
  return time.strftime("%b  %d %H:%M:%S", time.gmtime())

def main():
  print "[Ctrl + C to exit]"
  while True:
    with open(sys.argv[1], 'a+') as logfile:
      for i in xrange(random.randint(0,5)):
        fac = 2
        sev = 3
        pri = fac * 8 + sev
        logfile.write("<{0}>{1} localhost syslog_test: Log message from fac: {2}, sev: {3}\n".format(pri, syslogtime(), fac, sev))
      for i in xrange(20):
        time.sleep(random.random())

if __name__ == '__main__':
  main()        
