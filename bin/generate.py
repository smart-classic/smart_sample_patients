from rdflib import ConjunctiveGraph, Namespace, BNode, Literal, RDF, URIRef
from testdata import PATIENTS_FILE
from patient import Patient
from med import Med
from problem import Problem
from refill import Refill
from lab import Lab
import argparse
import sys
import os

# Some constant strings:
FILE_NAME_TEMPLATE = "p%s.xml"  # format for output files: p<patient id>.xml

SP_DEMOGRAPHICS = "http://smartplatforms.org/records/%s/demographics"
RXN_URI="http://rxnav.nlm.nih.gov/REST/rxcui/%s"
NUI_URI="http://rxnav.nlm.nih.gov/REST/rxcui?idtype=NUI&id=%s"
UNII_URI="http://fda.gov/UNII/%s"
SNOMED_URI="http://www.ihtsdo.org/snomed-ct/concepts/%s"
LOINC_URI="http://loinc.org/codes/%s"

# First Declare Name Spaces
SP = Namespace("http://smartplatforms.org/terms#")
DC = Namespace("http://purl.org/dc/elements/1.1/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
RDFS=Namespace("http://www.w3.org/2000/01/rdf-schema#")


class PatientGraph:
   """ Represents a patient's RDF graph"""

   def codedValue(self,uri,title,system,identifier):
     """ Adds a CodedValue to the graph and returns node"""
     cNode=BNode()
     self.g.add((cNode,RDF.type,SP['CodedValue']))
     self.g.add((cNode,SP['code'],URIRef(uri)))
     self.g.add((cNode,DCTERMS['title'],Literal(title)))
     return cNode 

   def valueAndUnit(self,value,units):
     """Adds a ValueAndUnit node to a graph; returns the node"""
     vNode = BNode()
     self.g.add((vNode,RDF.type,SP['ValueAndUnit']))
     self.g.add((vNode,SP['value'],Literal(value)))
     self.g.add((vNode,SP['unit'],Literal(units)))
     return vNode

   def __init__(self,p):
      """Create an instance of a RDF graph for patient instance p""" 
      self.pid=p.pid
      # Create a RDF graph and namespaces:
      g = ConjunctiveGraph()
      self.g = g  # Keep a reference to this graph as an instance var

      # Bind Namespaces to the graph:
      g.bind('rdfs',RDFS)
      g.bind('sp',SP)
      g.bind('dc',DC)
      g.bind('dcterms',DCTERMS)
      g.bind('foaf',FOAF)

      # Now add the patient demographic triples:
      pNode = BNode()
      g.add((pNode,RDF.type,SP.Demographics))
      g.add((pNode,FOAF['givenName'],Literal(p.fname)))
      g.add((pNode,FOAF['familyName'],Literal(p.lname)))
      g.add((pNode,FOAF['gender'],Literal(p.gender)))
      g.add((pNode,SP['zipcode'],Literal(p.zip)))
      g.add((pNode,SP['birthday'],Literal(p.dob)))

   def addMedList(self):
      """Adds a MedList to a patient's graph"""

      g = self.g
      if not self.pid in Med.meds: return  # No meds for this patient
      for m in Med.meds[self.pid]:
        mNode = BNode()
        g.add((mNode,RDF.type,SP['Medication']))
        g.add((mNode,SP['drugName'],self.codedValue(RXN_URI%m.rxn,m.name,RXN_URI%"",m.rxn)))
        g.add((mNode,SP['startDate'],Literal(m.start)))
        g.add((mNode,SP['instructions'],Literal(m.sig))) 
        if m.qtt:
          g.add((mNode,SP['quantity'],self.valueAndUnit(m.qtt,m.qttunit)))
        if m.freq:
          g.add((mNode,SP['frequency'],self.valueAndUnit(m.freq,m.frequnit)))

        # Now,loop through and add fulfillments for each med
        for fill in Refill.refill_list(m.pid,m.rxn):
          rfNode = BNode()
          g.add((rfNode,RDF.type,SP['Fulfillment']))
          g.add((rfNode,DC['date'],Literal(fill.date)))
          g.add((rfNode,SP['dispenseQuantity'],Literal(fill.q))) 
          g.add((rfNode,SP['dispenseDaysSupply'],Literal(fill.days)))
          g.add((mNode,SP['fulfillment'],rfNode))

   def addProblemList(self):
      """Add problems to a patient's graph"""
      g = self.g
      if not self.pid in Problem.problems: return # No problems to add
      for prob in Problem.problems[self.pid]:
        pnode = BNode()
        g.add((pnode,RDF.type,SP['Problem']))
        g.add((pnode,SP['onset'],Literal(prob.start)))      
        g.add((pnode,SP['problemName'],
            self.codedValue(SNOMED_URI%prob.snomed,prob.name,SNOMED_URI%"",prob.snomed)))

   def addLabResults(self):
       """Adds Lab Results to the patient's graph"""
       g = self.g
       if not self.pid in Lab.results: return  #No labs
       for lab in Lab.results[self.pid]:
         lNode = BNode()
         g.add((lNode,RDF.type,SP['LabResult']))
         g.add((lNode,SP['labName'],
            self.codedValue(LOINC_URI%lab.code,lab.name,LOINC_URI%"",lab.code)))

         if lab.scale=='Qn':
           qNode = BNode()
           g.add((qNode,RDF.type,SP['QuantitativeResult']))
           g.add((qNode,SP['valueAndUnit'],
             self.valueAndUnit(lab.value,lab.units)))

           # Add Range Values
           rNode = BNode()
           g.add((rNode,RDF.type,SP['ValueRange']))
           g.add((rNode,SP['minimum'],
                   self.valueAndUnit(lab.low,lab.units)))
           g.add((rNode,SP['maximum'],
                   self.valueAndUnit(lab.high,lab.units)))
           g.add((qNode,SP['normalRange'],rNode)) 
           g.add((lNode,SP['quantitativeResult'],qNode))

         if lab.scale=='Ord': # Handle an Ordinal Result  
           qNode = BNode()
           g.add((qNode,RDF.type,SP['NarrativeResult']))
           g.add((qNode,SP['value'],Literal(lab.value)))
           g.add((lNode,SP['narrativeResult'],qNode))

         aNode = BNode()
         g.add((aNode,RDF.type,SP['Attribution']))
         g.add((aNode,SP['startTime'],Literal(lab.date)))
         g.add((lNode,SP['specimenCollected'],aNode))

         g.add((lNode,SP['externalID'],Literal(lab.acc_num)))      

   def addAllergies(self):
         """A totally bogus method: doesn't read from an allergy file!"""
         g = self.g

         if int(self.pid)%100 < 85:  # no allergies for ~ 85% of population
           aExcept = BNode()
           g.add((aExcept,RDF.type,SP['AllergyException']))
           g.add((aExcept,SP['exception'],
               self.codedValue(SNOMED_URI%'160244002','No known allergies',SNOMED_URI%'','160244002')))

         else:  # Sprinkle in some sulfa allergies, for pid ending 85 and up
           aNode = BNode()
           g.add((aNode,RDF.type,SP['Allergy']))
           g.add((aNode,SP['severity'],
              self.codedValue(SNOMED_URI%'255604002','Mild',SNOMED_URI%'','255604002')))
           g.add((aNode,SP['reaction'],
              self.codedValue(SNOMED_URI%'271807003','Skin Rash',SNOMED_URI%'','271807003')))
           g.add((aNode,SP['category'],
              self.codedValue(SNOMED_URI%'416098002','Drug Allergy', SNOMED_URI%'','416098002')))
           g.add((aNode,SP['class'],
              self.codedValue(NUI_URI%'N0000175503','Sulfonamide Antibacterial',NUI_URI%''.split('&')[0], 'N0000175503')))
 
           if int(self.pid)%2: # And throw in some peanut allergies if odd pid...
             aNode = BNode()
             g.add((aNode,RDF.type,SP['Allergy'])) 
             g.add((aNode,SP['severity'],
               self.codedValue(SNOMED_URI%'24484000','Severe',SNOMED_URI%'','24484000')))
             g.add((aNode,SP['reaction'],
               self.codedValue(SNOMED_URI%'39579001','Anaphylaxis',SNOMED_URI%'','39579001')))
             g.add((aNode,SP['category'],
               self.codedValue(SNOMED_URI%'414285001','Food Allergy',SNOMED_URI%'','414285001')))
             g.add((aNode,SP['substance'],
               self.codedValue(UNII_URI%'QE1QX6B99R','Peanut',UNII_URI%'','QE1QX6B99R')))

   def toRDF(self,format="pretty-xml"):
         return self.g.serialize(format=format)

def initData():
   """Load data and mappings from Raw data files and mapping files"""
   Patient.load()
   Med.load()
   Problem.load()
   Lab.load()
   Refill.load()

def writePatientGraph(f,pid):
   """Writes a patient's RDF out to a file, f"""
   p = Patient.mpi[pid]
   g = PatientGraph(p)
   g.addMedList()
   g.addProblemList()
   g.addLabResults()
   g.addAllergies()
   print >>f, g.toRDF()

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
  group.add_argument('--rdf', metavar='pid', nargs='?', const='1520204',
     help='display RDF for a patient (default=1520204)')
  group.add_argument('--write', metavar='dir', nargs='?', const='.',
     help="writes all patient RDF files to directory dir (default='.')")
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
 
  # Display a single patient's RDF
  if args.rdf:
    initData()
    if not args.rdf in Patient.mpi:
      parser.error("Patient ID = %s not found."%args.rdf)
    else:
      writePatientGraph(sys.stdout,args.rdf)
      parser.exit()
 
  # Write all patient RDF files out to a directory
  if args.write:
    print "Writing files to %s:"%args.write
    initData()
    path = args.write
    if not os.path.exists(path):
      parser.error("Invalid path: '%s'.Path must already exist."%path)
    if not path.endswith('/'): path = path+'/' # Works with DOS? Who cares??
    for pid in Patient.mpi:
      f = open(path+FILE_NAME_TEMPLATE%pid,'w')
      writePatientGraph(f,pid)
      f.close()
      # Show progress with '.' characters
      print ".", 
      sys.stdout.flush()
    parser.exit(0,"\nDone writing %d patient RDF files!"%len(Patient.mpi))

  # Generate a new patients data file, re-randomizing old names, dob, etc:
  Patient.generate()  
  parser.exit(0,"Patient data written to: %s\n"%PATIENTS_FILE)

  parser.error("No arguments given")
