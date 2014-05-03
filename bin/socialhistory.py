from testdata import SOCIALHISTORY_FILE
import argparse
import csv


class SocialHistory: 
    """Create instances of SocialHistory; 
also maintains socialHistory by patient id"""

    socialHistories = {} # Dictionary of socialHistory by patient ID

    @classmethod
    def load(cls):
      """Loads patient SocialHistory"""
      
      # Loop through socialHistories and build patient socialHistory lists:
      histories = csv.reader(open(SOCIALHISTORY_FILE,'U'),dialect='excel-tab')
      header = next(histories) 
      for history in histories:
          cls(dict(zip(header,history))) # Create a socialHistory instance 

    def __init__(self,p):
        self.pid = p['PID']
        self.smokingStatusCode = p['SMOKINGSTATUSCODE']

        # Append socialHistory to the patient's socialHistory list:
        if self.pid in  self.__class__.socialHistories:
          raise "Found >1 socialHistory for a patient"
        else: self.__class__.socialHistories[self.pid] = self

    def asTabString(self):
       """Returns a tab-separated string representation of a socialHistory"""
       dl = [self.pid, self.start, self.snomed, self.name[:20]]
       s = ""
       for v in dl:
         s += "%s\t"%v 
       return s[0:-1] # Throw away the last tab

if __name__== '__main__':
  parser = argparse.ArgumentParser(description='Test Data SocialHistories Module')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--socialHistories', 
          action='store_true', help='list all socialHistories')
  group.add_argument('--pid',nargs='?', const='1520204',
     help='display socialHistories for a given patient id (default=1520204)')
  args = parser.parse_args()
 
  SocialHistory.load()
  if args.pid:
    if not args.pid in SocialHistory.socialHistories:
      parser.error("No results found for pid = %s"%args.pid)
    histories = SocialHistory.socialHistories[args.pid]
