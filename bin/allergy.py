from testdata import ALLERGIES_FILE
import argparse
import csv


class Allergy: 
    """Create instances of Allergy; 
also maintains complete allergy lists by patient id"""

    allergies = {} # Dictionary of allergy lists, by patient id 

    @classmethod
    def load(cls):
      """Loads patient Allergy observations"""
      
      # Loop through allergies and build patient allergy lists:
      probs = csv.reader(open(ALLERGIES_FILE,'U'),dialect='excel-tab')
      header = next(probs) 
      for prob in probs:
          cls(dict(zip(header,prob))) # Create a allergy instance 

    def __init__(self,p):
        self.pid = p['PID']
        self.statement = p['STATEMENT']
        self.type = p['TYPE']
        self.allergen = p['ALLERGEN']
        self.system = p['SYSTEM']
        self.code = p['CODE']
        self.start = p['START_DATE']
        self.end = p['END_DATE']
        self.reaction= p['REACTION']
        self.snomed= p['SNOMED'] 
        self.severity= p['SEVERITY']
        
        if self.severity == 'mild':
            self.severity_code = 255604002
        elif self.severity == 'moderate':
            self.severity_code = 6736007
        elif self.severity == 'severe':
            self.severity_code = 24484000
        elif self.severity == 'life threatening':
            self.severity_code = 442452003
        elif self.severity == 'fatal':
            self.severity_code = 399166001
        
        # Append allergy to the patient's allergy list:
        if self.pid in  self.__class__.allergies:
          self.__class__.allergies[self.pid].append(self)
        else: self.__class__.allergies[self.pid] = [self]

    def asTabString(self):
       """Returns a tab-separated string representation of a allergy"""
       dl = [self.pid, self.start, self.allergen[:20]]
       s = ""
       for v in dl:
         s += "%s\t"%v 
       return s[0:-1] # Throw away the last tab

if __name__== '__main__':

  parser = argparse.ArgumentParser(description='Test Data Allergies Module')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--allergies', 
          action='store_true', help='list all allergies')
  group.add_argument('--pid',nargs='?', const='1520204',
     help='display allergies for a given patient id (default=1520204)')
  args = parser.parse_args()
 
  Allergy.load()
  if args.pid:
    if not args.pid in Allergy.allergies:
      parser.error("No results found for pid = %s"%args.pid)
    probs = Allergy.allergies[args.pid]
    

     
