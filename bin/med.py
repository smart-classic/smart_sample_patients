from testdata import MEDS_FILE
import argparse
import csv


class Med: 
    """Create instances of Medication list entries; 
also maintains complete med lists by patient id"""

    meds = {} # Dictionary of med lists, by patient id 

    @classmethod
    def load(cls):
      """Loads patient Med observations"""
      
      # Loop through meds and build patient med lists:
      meds = csv.reader(file(MEDS_FILE,'U'),dialect='excel-tab')
      header = meds.next() 
      for med in meds:
          cls(dict(zip(header,med))) # Create a med instance (saved in Med.meds)


    def __init__(self,m):
        self.pid = m['PT_ID']
        self.start = m['START_DATE']
        self.end = m['END_DATE']
        self.rxn= m['RxNorm'] 
        self.name = m['Name']
        self.sig = m['SIG']
        self.q = m['Q']
        self.days = m['DAYS']
        self.refills = m['REFILLS']
        self.qtt = m['Q_TO_TAKE_VALUE']
        self.qttunit = m['Q_TO_TAKE_UNIT']
        self.freq = m['FREQUENCY_VALUE'] 
        self.frequnit = m['FREQUENCY_UNIT']

        # Append med to the patient's med list:
        if self.pid in  self.__class__.meds:
          self.__class__.meds[self.pid].append(self)
        else: self.__class__.meds[self.pid] = [self]

    def asTabString(self):
       """Returns a tab-separated string representation of a med instance"""
       dl = [self.pid, self.start, self.rxn, self.name[:20], self.sig]
       s = ""
       for v in dl:
         s += "%s\t"%v 
       return s[0:-1] # Throw away the last tab

if __name__== '__main__':

  parser = argparse.ArgumentParser(description='Test Data Meds Module')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--meds', action='store_true', help='list all meds')
  group.add_argument('--pid',nargs='?', const='1520204',
     help='display meds for a given patient id (default=1520204)')
  args = parser.parse_args()
 
  Med.load()
  if args.pid:
    if not args.pid in Med.meds:
      parser.error("No results found for pid = %s"%args.pid)
    meds = Med.meds[args.pid]
    for med in meds: 
      print med.asTabString()
    

     
