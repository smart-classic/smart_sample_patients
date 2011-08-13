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
<!DOCTYPE rdf:RDF [
    <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >
    <!ENTITY sp "http://smartplatforms.org/terms#" >
    <!ENTITY cemterms "http://smartplatforms.org/cemterms#" >
    <!ENTITY smartplatforms "http://smartplatforms.org/" >
    <!ENTITY dcterms "http://purl.org/dc/terms/" >
]>


<rdf:RDF xmlns="&smartplatforms;cemterms#"
     xml:base="&smartplatforms;cemterms#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:dcterms="http://purl.org/dc/terms/"
     xmlns:sp="http://smartplatforms.org/terms#"
     xmlns:cem="http://smartplatforms.org/cemterms#"
     xmlns:foaf="http://xmlns.com/foaf/0.1/" 
>
  <sp:Demographics>
    <foaf:familyName>$family_name</foaf:familyName>
    <sp:zipcode>$zipcode</sp:zipcode>
    <foaf:givenName>$given_name</foaf:givenName>
    <foaf:gender>$gender</foaf:gender>
    <sp:birthday>$birthday</sp:birthday>
  </sp:Demographics>

""")

footer = """
</rdf:RDF>
"""

med = Template("""
<OrderMedAmb>
  <orderable>
    <Orderable>
      <rdf:type rdf:resource="&cemterms;OrderMedAmb.orderable" />
      <frequency>
        <Frequency>
          <frequencyItem>
            <FrequencyItem>
              <periodicFrequencyLowerLimit>
                <PeriodicFrequencyLowerLimit>
                  <sp:valueAndUnit>
                    <sp:ValueAndUnit>
                      <sp:unit rdf:datatype="&rdfs;Literal">$frequency_u</sp:unit>
		      <sp:value rdf:datatype="&rdfs;Literal">$frequency_v</sp:value>
                    </sp:ValueAndUnit>
                  </sp:valueAndUnit>
                </PeriodicFrequencyLowerLimit>
             </periodicFrequencyLowerLimit>
            </FrequencyItem>
          </frequencyItem>
        </Frequency>
      </frequency>
      <orderableItem>
        <OrderableItem>
          <rdf:type rdf:resource="&cemterms;OrderMedAmb.orderable.orderableItem" />
          <sp:code>
            <sp:Code rdf:about="http://rxnav.nlm.nih.gov/REST/rxcui/$rxnorm_uri">
              <rdf:type rdf:resource="http://smartplatforms.org/cemterms#OrderableItem_DOMAIN_ECID" />
              <dcterms:title>$rxnorm_title</dcterms:title>
              <sp:system>http://rxnav.nlm.nih.gov/REST/rxcui/</sp:system>
              <dcterms:identifier>$rxnorm_uri</dcterms:identifier>
            </sp:Code>
          </sp:code>
          <orderedDoseLowerLimit>
            <OrderedDoseLowerLimit>
              <sp:valueAndUnit>
                <sp:ValueAndUnit>
		  <sp:value rdf:datatype="&rdfs;Literal">$dose_v</sp:value>
                  <sp:unit rdf:datatype="&rdfs;Literal">$dose_u</sp:unit>
                </sp:ValueAndUnit>
              </sp:valueAndUnit>
            </OrderedDoseLowerLimit>
          </orderedDoseLowerLimit>
        </OrderableItem>
      </orderableItem>
    </Orderable>
  </orderable>
</OrderMedAmb>
""")

def writePatientFile(f,pid):
   """Writes a patient's RDF out to a file, f"""
   p = Patient.mpi[pid]
   print >>f, header.substitute(given_name=p.fname, family_name=p.lname, zipcode=p.zip, birthday=p.dob, gender=p.gender)

   if  pid in Med.meds: 
       for m in Med.meds[pid]:
           frequency = ""
           try: frequency="%s %s"%(m.freq, m.frequnit)
           except: pass          
           if not m.qtt:
               m.qtt="1"
               m.qttunit="{tab}"


           print >>f,  med.substitute( rxnorm_uri=m.rxn, 
                                            rxnorm_title=m.name, 
                                            dose_v=m.qtt, 
                                            dose_u=m.qttunit, 
                                            frequency_v=m.freq,
                                            frequency_u=m.frequnit)      
   print >>f, footer
