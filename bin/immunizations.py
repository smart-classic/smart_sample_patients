from testdata import IMMUNIZATIONS_FILE
import argparse
import csv


class Immunizations: 
    """Create instances of Immunizations list entries; 
also maintains complete Immunizations lists by patient id"""

    immunizations = {} # Dictionary of Immunization lists, by patient id 

    @classmethod
    def load(cls):
      """Loads patient Immunizations observations"""
      
      # Loop through Immunizations and build patient Immunizations lists:
      Immunizations = csv.reader(file(IMMUNIZATIONS_FILE,'U'),dialect='excel-tab')
      header = Immunizations.next() 
      for Immunization in Immunizations:
          cls(dict(zip(header,Immunization))) # Create a Immunization instance (saved in Immunizations.immunizations)

    def __init__(self,m):
        for f in m:
            setattr(self, f.lower(), m[f])

        self.sourcerow = m

        # Append Immunization to the patient's Immunization list:
        if self.pid in  self.__class__.immunizations:
          self.__class__.immunizations[self.pid].append(self)
        else: self.__class__.immunizations[self.pid] = [self]

    def asTabString(self):
        return self.sourcerow

if __name__== '__main__':
  print "As main"
  parser = argparse.ArgumentParser(description='Test Data Vitals Module')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--Immunizations', action='store_true', help='list all Immunizations')
  group.add_argument('--pid',nargs='?', default='1614502',
     help='display Immunizations for a given patient id (default=1614502)')
  args = parser.parse_args()
  print args 
  Immunizations.load()
  if args.pid:
    if not args.pid in Immunizations.immunizations:
      parser.error("No results found for pid = %s"%args.pid)
    Immunizations = Immunizations.immunizations[args.pid]
    for Immunization in Immunizations: 
      print Immunization.asTabString()
    

     
