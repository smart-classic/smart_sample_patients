from testdata import FAMILYHISTORY_FILE
import argparse
import csv

class FamilyHistory: 
    """Create instances of FamilyHistory and maintain FamilyHistory lists by patient ID"""

    familyHistories = {} # Dictionary of FamilyHistory lists by patient ID

    @classmethod
    def load(cls):
        """Loads patient family histories"""
      
        # Loop through family histories and build patient FamilyHistory lists:
        histories = csv.reader(open(FAMILYHISTORY_FILE,'U'),dialect='excel-tab')
        header = next(histories) 
        for history in histories:
            cls(dict(zip(header,history))) # Create a FamilyHistory instance 

    def __init__(self,fh):
        self.patientid = fh['PATIENT_ID']
        self.relativecode = fh['RELATIVE_CODE']
        self.relativetitle = fh['RELATIVE_TITLE'] 
        self.dateofbirth = fh['DATE_OF_BIRTH']
        self.dateofdeath = fh['DATE_OF_DEATH']
        self.problemcode = fh['PROBLEM_CODE']
        self.problemtitle = fh['PROBLEM_TITLE'] 
        self.heightcm = fh['HEIGHT_CM'] 
        # Append FamilyHistory to the patient's list:
        if self.patientid in self.__class__.familyHistories:
            self.__class__.familyHistories[self.patientid].append(self)
        else:
            self.__class__.familyHistories[self.patientid] = [self]

    def asTabString(self):
       """Returns a tab-separated string representation of a FamilyHistory"""
       dl = [self.patientid, self.relativecode, self.relativetitle, self.dateofbirth,
             self.dateofdeath, self.problemcode, self.problemtitle, self.heightcm]
       s = ""
       for v in dl:
         s += "%s\t"%v 
       return s[0:-1] # Throw away the last tab

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Data FamilyHistory Module')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--familyHistories', 
        action='store_true', help='list all family histories')
    group.add_argument('--patientid', nargs='?', const='613876',
        help='display family histories for a given patient id (default=613876)')
    args = parser.parse_args()
    FamilyHistory.load()
    if args.patientid:
        if not args.patientid in FamilyHistory.familyHistories:
            parser.error("No results found for patientid = %s"%args.patientid)
        histories = FamilyHistory.familyHistories[args.patientid]
