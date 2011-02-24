from testdata import REFILLS_FILE
import argparse
import csv


class Refill: 
    """Create instances of a med refill; 
also maintains complete refills lists by patient id"""

    refills = {} # Dictionary of refills, by patient id 

    @classmethod
    def load(cls):
      """Loads med refills"""
      
      # Loop through refills and build med refill list:
      refills = csv.reader(file(REFILLS_FILE,'U'),dialect='excel-tab')
      header = refills.next() 
      for refill in refills:
          cls(dict(zip(header,refill))) # Create a refill instance 

    @classmethod
    def refill_list(cls,pid,rxn):
       """Return a refill history for patient, pid, and for med, rxn""" 
       refills = {}
       if not pid in cls.refills: return []
       for med in cls.refills[pid]:
         if int(med.q) and med.rxn==rxn: # non-zero quantity
           refills[rxn+med.date]=med # and only one rnx per day
       return refills.values()

    def __init__(self,p):
        self.pid = p['PID']
        self.date = p['DATE']
        self.rxn= p['RXN'] 
        self.days = p['DAYS']
        self.q = p['Q']
        # Append refill to the refills list:
        if self.pid in  self.__class__.refills:
          self.__class__.refills[self.pid].append(self)
        else: self.__class__.refills[self.pid] = [self]

    def asTabString(self):
       """Returns a tab-separated string representation of a refill"""
       dl = [self.pid, self.date, self.rxn, self.days,self.refills]
       s = ""
       for v in dl:
         s += "%s\t"%v 
       return s[0:-1] # Throw away the last tab

if __name__== '__main__':

  parser = argparse.ArgumentParser(description='Test Data Refills Module')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--refills', 
          action='store_true', help='list all refills')
  group.add_argument('--pid',nargs='?', const='1288992',
     help='display refills for a given patient id (default=1288992)')
  args = parser.parse_args()
 
  Refill.load()
  if args.pid:
    if not args.pid in Refill.refills:
      parser.error("No results found for pid = %s"%args.pid)
    refills = Refill.refills[args.pid]
    for refill in refills: 
      print refill.asTabString()
    

     
