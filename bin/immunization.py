from testdata import IMMUNIZATIONS_FILE
import argparse
import csv


class Immunization: 
    """Create instances of Immunization list entries; 
also maintains complete Immunization lists by patient id"""

    immunizations = {} # Dictionary of Immunization lists, by patient id 

    @classmethod
    def load(cls):
      """Loads patient Immunization observations"""
      
      # Loop through Immunizations and build patient Immunizations lists:
      iis = csv.reader(open(IMMUNIZATIONS_FILE,'U'),dialect='excel-tab')
      header = next(iis) 
      for i in iis:
          cls(dict(zip(header,i))) # Create a Immunization instance (saved in Immunizations.immunizations)

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
  parser = argparse.ArgumentParser(description='Test Data Vitals Module')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--Immunizations', action='store_true', help='list all Immunizations')
  group.add_argument('--pid',nargs='?', default='1614502',
     help='display Immunizations for a given patient id (default=1614502)')
  args = parser.parse_args()
  Immunization.load()
  if args.pid:
    if not args.pid in Immunization.immunizations:
      parser.error("No results found for pid = %s"%args.pid)
    iis = Immunization.immunizations[args.pid]
