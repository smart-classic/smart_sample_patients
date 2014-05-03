from testdata import PROCEDURES_FILE
import argparse
import csv


class Procedure: 
    """Create instances of Procedure; also maintains complete procedure lists by patient id"""

    procedures = {} # Dictionary of procedure lists, by patient id 

    @classmethod
    def load(cls):
      """Loads patient Procedure observations"""
      
      # Loop through procedures and build patient procedure lists:
      procs = csv.reader(open(PROCEDURES_FILE,'U'),dialect='excel-tab')
      header = next(procs) 
      for proc in procs:
          cls(dict(zip(header,proc))) # Create a procedure instance 

    def __init__(self,p):
        self.pid = p['PID']
        self.date = p['DATE']
        self.snomed= p['SNOMED'] 
        self.name = p['NAME']
        self.notes = p['NOTES']
        # Append procedure to the patient's procedure list:
        if self.pid in  self.__class__.procedures:
          self.__class__.procedures[self.pid].append(self)
        else: self.__class__.procedures[self.pid] = [self]

    def asTabString(self):
       """Returns a tab-separated string representation of a procedure"""
       dl = [self.pid, self.date, self.snomed, self.name[:20]]
       s = ""
       for v in dl:
         s += "%s\t"%v 
       return s[0:-1] # Throw away the last tab

if __name__== '__main__':

  parser = argparse.ArgumentParser(description='Test Data Procedures Module')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--procedures', 
          action='store_true', help='list all procedures')
  group.add_argument('--pid',nargs='?', const='1520204',
     help='display procedures for a given patient id (default=1520204)')
  args = parser.parse_args()
 
  Procedure.load()
  if args.pid:
    if not args.pid in Procedure.procedures:
      parser.error("No results found for pid = %s"%args.pid)
    procs = Procedure.procedures[args.pid]
