from testdata import PATIENTS_FILE
from patient import Patient
from med import Med
from problem import Problem
from procedure import Procedure
from refill import Refill
from vitals import VitalSigns
from immunization import Immunization
from lab import Lab
from allergy import Allergy
from socialhistory import SocialHistory
from familyhistory import FamilyHistory
import argparse
import sys
import os

# Some constant strings:
FILE_NAME_TEMPLATE = "p%s.xml"  # format for output files: p<patient id>.xml

def initData():
   """Load data and mappings from Raw data files and mapping files"""
   Patient.load()
   Med.load()
   Problem.load()
   Lab.load()
   Refill.load()
   VitalSigns.load()
   Immunization.load()
   Procedure.load()
   SocialHistory.load()
   FamilyHistory.load()
   Allergy.load()

def displayPatientSummary(pid):
   """writes a patient summary to stdout"""
   if not pid in Patient.mpi: return
   print Patient.mpi[pid].asTabString()
   print "PROBLEMS: ",
   if not pid in Problem.problems: print "None",
   else: 
     for prob in Problem.problems[pid]: print prob.name+"; ",
   print "\nMEDICATIONS: ",
   if not pid in Med.meds: print "None",
   else:
     for med in Med.meds[pid]: 
       print med.name+"{%d}; "%len(Refill.refill_list(pid,med.rxn)),
   print "\nLABS: ",
   if not pid in Lab.results: print "None",
   else:
     print "%d results"%len(Lab.results[pid])
   print "\n"

if __name__=='__main__':

  parser = argparse.ArgumentParser(description='Test Data Generator')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--summary', metavar='pid',nargs='?', const="all", 
     help="displays patient summary (default is 'all')")
  group.add_argument('--write-fhir',dest='writeFHIR', metavar='dir', nargs='?', const='.',
     help="writes patient XML files to an FHIR sample data directory dir (default='.')")
  group.add_argument('--patients', action='store_true',
         help='Generates new patient data file (overwrites existing one)')

  args = parser.parse_args()

  # Print a patient summary: 
  if args.summary:
    initData()
    if args.summary=='all': # Print a summary of all patients
      for pid in Patient.mpi: displayPatientSummary(pid)
      parser.exit()
    else: # Just print a single patient's summary
      if not args.summary in Patient.mpi:
        parser.error("Patient ID = %s not found"%args.summary)
      else: displayPatientSummary(args.summary)
    parser.exit()

  if args.writeFHIR:
    import fhir
    print "Writing files to %s:"%args.writeFHIR
    initData()
    path = args.writeFHIR
    if not os.path.exists(path):
      parser.error("Invalid path: '%s'.Path must already exist."%path)
    for pid in Patient.mpi:
      fhir.FHIRSamplePatient(pid, path).writePatientData()
      # Show progress with '.' characters
      sys.stdout.flush()
    parser.exit(0,"\nDone writing %d patient FHIR files!"%len(Patient.mpi))

  # Generate a new patients data file, re-randomizing old names, dob, etc:
  Patient.generate()  
  parser.exit(0,"Patient data written to: %s\n"%PATIENTS_FILE)

  parser.error("No arguments given")
