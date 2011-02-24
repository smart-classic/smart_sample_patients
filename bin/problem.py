from testdata import PROBLEMS_FILE
import argparse
import csv


class Problem: 
    """Create instances of Problem; 
also maintains complete problem lists by patient id"""

    problems = {} # Dictionary of problem lists, by patient id 

    @classmethod
    def load(cls):
      """Loads patient Problem observations"""
      
      # Loop through problems and build patient problem lists:
      probs = csv.reader(file(PROBLEMS_FILE,'U'),dialect='excel-tab')
      header = probs.next() 
      for prob in probs:
          cls(dict(zip(header,prob))) # Create a problem instance 

    def __init__(self,p):
        self.pid = p['PID']
        self.start = p['START_DATE']
        self.snomed= p['SNOMED'] 
        self.name = p['NAME']
        # Append problem to the patient's problem list:
        if self.pid in  self.__class__.problems:
          self.__class__.problems[self.pid].append(self)
        else: self.__class__.problems[self.pid] = [self]

    def asTabString(self):
       """Returns a tab-separated string representation of a problem"""
       dl = [self.pid, self.start, self.snomed, self.name[:20]]
       s = ""
       for v in dl:
         s += "%s\t"%v 
       return s[0:-1] # Throw away the last tab

if __name__== '__main__':

  parser = argparse.ArgumentParser(description='Test Data Problems Module')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--problems', 
          action='store_true', help='list all problems')
  group.add_argument('--pid',nargs='?', const='1520204',
     help='display problems for a given patient id (default=1520204)')
  args = parser.parse_args()
 
  Problem.load()
  if args.pid:
    if not args.pid in Problem.problems:
      parser.error("No results found for pid = %s"%args.pid)
    probs = Problem.problems[args.pid]
    for prob in probs: 
      print prob.asTabString()
    

     
