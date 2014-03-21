import random
import time

def syslogtime():
  return time.strftime("%b  %d %H:%M:%S", time.gmtime())

def gen(fn, lines):
  with open(fn, "a+") as file:
    for i in xrange(lines):
      fac = random.randint(0,23)
      sev = random.randint(0,7)
      pri = fac * 8 + sev
      file.write("<{0}>{1} localhost syslog_test: Log message from fac: {2}, sev: {3}\n".format(pri, syslogtime(), fac, sev))

def main():
  import sys
  fp = "default.log"
  lines = 100
  if(len(sys.argv) == 2):
    fp = sys.argv[1]
  elif(len(sys.argv) > 2):
    lines = int(sys.argv[1])
    fp = sys.argv[2]
  gen(fp, lines)

if __name__ == "__main__":
  main()
