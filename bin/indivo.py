from string import Template
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



header = Template("""
from indivo.models import *
a = Account.objects.order_by('?')[0]
record = Record(owner=a, label='$label')
record.save()
problems = []
meds = []
labs = []
demographics = []
""")

footer = """
# so we know which record we're adding this to
print "adding SMART data to Record %s - %s" % (record.id, record.label)

from indivo.views.documents.document import _document_create

# create some demographics for that poor record
demographics_doc = _document_create(record.owner, demographics[0], None, record)
from indivo.views.documents.special_documents import set_special_doc
set_special_doc(record, 'demographics', demographics_doc)

for doc in problems + meds + labs:
    print doc
    _document_create(record.owner, doc, None, record)
"""

demographics = Template("""
<Demographics xmlns="http://indivo.org/vocab/xml/documents#">
    <dateOfBirth>$dob</dateOfBirth>
    <gender>$gender</gender>
    <language>EN</language>
</Demographics>
""")

med = Template("""
<Medication xmlns="http://indivo.org/vocab/xml/documents#">
  <dateStarted>$startDate</dateStarted>
  <name type="http://rxnav.nlm.nih.gov/REST/rxcui/" value="$rxnorm">$name</name>
  <dose>
    <value>$quantityValue</value>
    <unit type="http://unitsofmeasure.org/" value="$quantityUnits" />
  </dose>
  <frequency type="http://unitsofmeasure.org/" value="$frequency">$frequency</frequency>

  <prescription>
    <dispenseAsWritten>true</dispenseAsWritten>
    <instructions>$instructions</instructions>
  </prescription>
</Medication>
""")


problem = Template("""
<Problem xmlns="http://indivo.org/vocab/xml/documents#">
  <dateOnset>${onset}T00:00:00Z</dateOnset>
  <name type="http://www.ihtsdo.org/snomed-ct/concepts/" value="$snomed">$name</name>
</Problem>
""")

lab = Template("""
<Lab xmlns="http://indivo.org/vocab/xml/documents#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dateMeasured>${date}T00:00:00Z</dateMeasured>
  <labType>general</labType>

  <labTest xsi:type="SingleResultLabTest">
    <dateMeasured>${date}T00:00:00Z</dateMeasured>
    <name type="http://loinc.org/codes/"  value="$loinc"><![CDATA[$name]]></name>
    <final>true</final>
    <result xsi:type="ResultInRange">
      <valueAndUnit>
        <value>$value</value>
        <unit type="http://unitsofmeasure.org/#" value="$units">$units</unit>
      </valueAndUnit>
    </result>    
  </labTest>
</Lab>
""")

def addElement(f, category, value):
   print >>f, "%s.append(\"\"\"%s\"\"\".encode())\n"%(category, value)


def writePatientFile(f,pid):
   """Writes a patient's RDF out to a file, f"""
   p = Patient.mpi[pid]
   print >>f, header.substitute(label="%s %s"%(p.fname, p.lname))
   addElement(f, "demographics", demographics.substitute(dob=p.dob, gender=p.gender))

   if pid in Lab.results:  # No problems to add
      
      for l in Lab.results[pid]:
         if l.scale != 'Qn': continue
         addElement(f, "labs",  lab.substitute(date=l.date,
                                            loinc=l.code,
                                            name=l.name,
                                            value=l.value,
                                            units=l.units))
                                            
                        

   if pid in Problem.problems: 
      for p in Problem.problems[pid]:
         addElement(f, "problems",  problem.substitute(onset=p.start, snomed=p.snomed, name=p.name))


   if  pid in Med.meds: 
      for m in Med.meds[pid]:
         frequency = ""
         try: frequency="%s %s"%(m.freq, m.frequnit)
         except: pass

         if not m.qtt:
            m.qtt="1"
            m.qttunit="{tablet}"

            addElement(f, "meds",  med.substitute(startDate=m.start,
                                            rxnorm=m.rxn, 
                                            name=m.name, 
                                            quantityValue=m.qtt, 
                                            quantityUnits=m.qttunit, 
                                            frequency=frequency,
                                            instructions=m.sig))
      
   print >>f, footer
