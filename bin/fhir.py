import datetime
from patient import Patient
import rdflib
from med import Med
from problem import Problem
from refill import Refill
from lab import Lab
from immunization import Immunization
from vitals import VitalSigns
import os
import uuid
import csv
import json
import pystache
from lxml import etree
import sys

from jinja2 import Environment, FileSystemLoader
template_env = Environment(loader=FileSystemLoader('fhir_templates'), autoescape=True)
sp= rdflib.Namespace('http://smartplatforms.org/terms#')

def uid():
    return str(uuid.uuid4())

def getVital(v, vt):
  return {
    'date': v.timestamp[:10],
    'code': vt['uri'].split('/')[-1],
    'units': vt['unit'],
    'value': float(getattr(v, vt['name'])),
    'scale': 'Qn',
    'name': vt['name']
    }

class FHIRSamplePatient(object):
  def __init__(self, pid, path):
    self.path = path
    self.pid = pid
    
    return
    """if self.pid in Med.meds:
      for m in Med.meds[self.pid]:
        # build the med, setting some defaults
        med_data = {
            'medid': uid(),
            'drugname': m.name,
            'drugcode': m.rxn,
            'medto': m.end if hasattr(m, "end") else None,
            'medfrom': m.start,
            'instructions': m.sig,
            'freq': m.freq,
            'frequ': m.frequnit,
            'quant': m.qtt,
            'quantu': m.qttunit
            }

            add these in later
            'frequencyValue': m.freq,
            'frequencyUnits': m.frequnit,
            'quantityValue': m.qtt,
            'quantityUnits': m.qttunit,
            """

  def writePatientData(self):

    pfile = open(os.path.join(self.path, "patient-%s.fhir-bundle.xml"%self.pid), "w")
    pid = self.pid
    p = Patient.mpi[pid]

    now = datetime.datetime.now().isoformat()
    id = "patient-%s"%pid
    print >>pfile, """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>SMART patient bundle for transactional posting</title>
  <id>urn:uuid:%s</id>
  <updated>%s</updated>
"""%(uid(), now)

    template = template_env.get_template('patient.xml')
    print >>pfile, template.render(dict(globals(), **locals()))

    bps = []
    othervitals = []

    if self.pid in VitalSigns.vitals:
      for v in  VitalSigns.vitals[pid]:
          for vt in VitalSigns.vitalTypes:
              try: 
                  othervitals.append(getVital(v, vt))
              except: pass
          try: 
              systolic = getVital(v, VitalSigns.systolic)
              diastolic = getVital(v, VitalSigns.diastolic)
              bp = systolic
              bp['systolic'] = int(systolic['value'])
              bp['diastolic'] = int(diastolic['value'])
              bps.append(bp)
          except: pass

    template = template_env.get_template('blood_pressure.xml')
    for bp in bps:
        id = "bp-%s"%uid()
        print >>pfile, template.render(dict(globals(), **locals()))

    template = template_env.get_template('observation.xml')
    for o in othervitals:
        id = "vital-%s"%uid()
        print >>pfile, template.render(dict(globals(), **locals()))

    if self.pid in Lab.results:  
      for o in Lab.results[pid]:
        id = "lab-%s"%uid()
        print >>pfile, template.render(dict(globals(), **locals()))

    medtemplate = template_env.get_template('medication.xml')
    dispensetemplate = template_env.get_template('medication_dispense.xml')
    if self.pid in Med.meds:  
      for m in Med.meds[pid]:
        medid = id = "med-%s"%uid()
        print >>pfile, medtemplate.render(dict(globals(), **locals()))

        for f in Refill.refill_list(m.pid, m.rxn):
          id = "dispense-%s"%uid()
          print >>pfile, dispensetemplate.render(dict(globals(), **locals()))

    template = template_env.get_template('condition.xml')
    if self.pid in Problem.problems:  
      for c in Problem.problems[pid]:
        id = "problem-%s"%uid()
        print >>pfile, template.render(dict(globals(), **locals()))

    print >>pfile, "\n</feed>"
    pfile.close()
