from testdata import NOTES_PATH
import argparse
import csv
import os
from common.rdf_tools.util import *

class ClinicalNote: 
    """Create instances of ClinicalNote; also maintains notes by patient id"""

    clinicalNotes = {} # Dictionary of clinicalNote by patient ID

    @classmethod
    def load(cls):
        """Loads patient ClinicalNote"""
      
        try:
          # Loop through clinicalNotes and build patient clinicalNote lists:
          for pid in os.listdir(NOTES_PATH):
              cls.clinicalNotes[pid] = []
              patientpath = os.path.join(NOTES_PATH, pid)
              for notefile in os.listdir(patientpath):
                  noteval = open(os.path.join(patientpath, notefile)).read()
                  notegraph = parse_rdf(noteval)
                  cls.clinicalNotes[pid].append(notegraph)
        except:
            pass