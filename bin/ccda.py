from patient import Patient
import rdflib
from med import Med
from problem import Problem
from refill import Refill
from lab import Lab
from immunizations import Immunizations
from vitals import VitalSigns
import ontology_service
import os
import uuid
import csv
import json
import pystache
from lxml import etree
import sys

template = open("med-template.ccda.xml").read()
renderer = pystache.Renderer(decode_errors="replace")
sp= rdflib.Namespace('http://smartplatforms.org/terms#')

def coded_value(self, raw_uri):
  """ Look up a URI in the ontology service. """
  g = rdflib.Graph()
  uri = rdflib.URIRef(raw_uri)
  cv = ontology_service.coded_value(g, rdflib.URIRef(uri))
  code = str(list(g.triples((uri, sp.code, None)))[0][2])
  title = str(list(g.triples((uri, DCTERMS.title, None)))[0][2])
  sep = "#" if "#" in str(uri) else "/"
  sys, ident = str(uri).rsplit(sep, 1)
  return {'title': str(title), 'code':str(code)}

class CCDASamplePatient(object):
  def __init__(self, pid, path):
    self.path = path
    self.pid = pid
    p = Patient.mpi[pid]

    birthdate  = p.dob

    self.jpatient = jpatient = {
        'patient': {
          'gendercode': p.gender[0].title(),
          'genderdisplay': p.gender.title(),
          'birthdate': p.dob,
          'GivenName': p.fname,
          'Surname': p.lname,
          'TelephoneNumber': p.home,
          'City': p.city,
          'State': p.region,
          'ZipCode': p.pcode,
          'StreetAddress': p.street
          },
        'pid': pid,
        'docid':str(uuid.uuid4()),
        'meds': [],
        'labs': [],
        'vitals': []
        }


    def getVital(vt):
      return {
          'timestamp': v.timestamp,
          'code': vt['uri'].split('/')[-1],
          'unit': vt['unit'],
          'value': getattr(v, vt['name']),
          'title': vt['name'],
          'vitalid': str(uuid.uuid4())
          }

    if self.pid in VitalSigns.vitals:
      for v in  VitalSigns.vitals[pid]:
        measurements = []
        for vt in VitalSigns.vitalTypes + [VitalSigns.systolic, VitalSigns.diastolic]:
          measurements.append(getVital(vt))
        jpatient['vitals'].append({
        'timestamp': measurements[0]['timestamp'],
        'measurements': measurements})

    if self.pid in Lab.results:  
      labs = []
      for l in Lab.results[pid]:
        if l.scale == 'Qn':
          result_data = {
              'val': l.value,
              'units': l.units,
              'low_val': l.low,
              'high_val': l.high,
              }
        else:
          # no results, don't add this lab
           continue

        # TODO mplement non-PQ labs 
        """
        elif l.scale == 'Ord':
        """
        lab_data = {
            'code': l.code,
            'name': l.name,
            'date': l.date,
            'acc_num': l.acc_num,
            'labid': str(uuid.uuid4()),
            'lorgid': str(uuid.uuid4()),
            'val': result_data['val'],
            'units': result_data['units']
            }
        jpatient['labs'].append(lab_data)

    if self.pid in Med.meds:
      for m in Med.meds[self.pid]:
        # build the med, setting some defaults
        med_data = {
            'medid': str(uuid.uuid4()),
            'drugname': m.name,
            'drugcode': m.rxn,
            'medto': m.end if hasattr(m, "end") else None,
            'medfrom': m.start,
            'instructions': m.sig
            }

        """
            add these in later
            'frequencyValue': m.freq,
            'frequencyUnits': m.frequnit,
            'quantityValue': m.qtt,
            'quantityUnits': m.qttunit,
            """
        jpatient['meds'].append(med_data)

        print json.dumps(jpatient, indent=2)
        """
       """

  def writePatientData(self):
    o = open(os.path.join(self.path, "p%s.ccda.xml"%self.pid), "w")
    print >>o, renderer.render(template, self.jpatient)
    o.close()
