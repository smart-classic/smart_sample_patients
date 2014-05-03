import datetime
from patient import Patient
from med import Med
from problem import Problem
from refill import Refill
from lab import Lab
from immunization import Immunization
from vitals import VitalSigns
import os
import uuid

from jinja2 import Environment, FileSystemLoader
template_env = Environment(loader=FileSystemLoader('fhir_templates'), autoescape=True)

base=0
def uid(resource_type=None):
    global base
    base += 1
    if (resource_type == None):
      return str(base)
    else:
      return "%s/%s"%(resource_type, str(base))

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

  def writePatientData(self):

    pfile = open(os.path.join(self.path, "patient-%s.fhir-bundle.xml"%self.pid), "w")
    p = Patient.mpi[self.pid]

    now = datetime.datetime.now().isoformat()
    id = "Patient/%s"%self.pid
    pid = id

    print("""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>SMART patient bundle for transactional posting</title>
  <id>urn:uuid:%s</id>
  <updated>%s</updated>
"""%(uid(), now), end="", file=pfile);

    template = template_env.get_template('patient.xml')
    print(template.render(dict(globals(), **locals())), end="", file=pfile)

    bps = []
    othervitals = []

    if self.pid in VitalSigns.vitals:
      for v in  VitalSigns.vitals[self.pid]:
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

    for bp in bps:
        systolicid = uid("Observation")
        diastolicid = uid("Observation")
        id = uid("Observation")
        template = template_env.get_template('blood_pressure.xml')
        print(template.render(dict(globals(), **locals())), end="", file=pfile)

        id = systolicid
        o = {
                "date": bp['date'],
                "code": "8480-6",
                "name": "Systolic blood pressure",
                "scale": "Qn",
                "value": bp['systolic'],
                "units": "mm[Hg]"
        }
        template = template_env.get_template('observation.xml')
        print(template.render(dict(globals(), **locals())), end="", file=pfile)

        id = diastolicid
        o = {
                "date": bp['date'],
                "code": "8462-4",
                "name": "Diastolic blood pressure",
                "scale": "Qn",
                "value": bp['diastolic'],
                "units": "mm[Hg]"
        }
        template = template_env.get_template('observation.xml')
        print(template.render(dict(globals(), **locals())), end="", file=pfile)

    template = template_env.get_template('observation.xml')
    for o in othervitals:
        id = uid("Observation")
        print(template.render(dict(globals(), **locals())), end="", file=pfile)

    if self.pid in Lab.results:  
      for o in Lab.results[self.pid]:
        id = uid("Observation")
        print(template.render(dict(globals(), **locals())), end="", file=pfile)

    medtemplate = template_env.get_template('medication.xml')
    dispensetemplate = template_env.get_template('medication_dispense.xml')
    if self.pid in Med.meds:  
      for m in Med.meds[self.pid]:
        medid = id = uid("MedicationPrescription")
        print(medtemplate.render(dict(globals(), **locals())), end="", file=pfile)

        for f in Refill.refill_list(m.pid, m.rxn):
          id = uid("MedicationDispense")
          print(dispensetemplate.render(dict(globals(), **locals())), end="", file=pfile)

    template = template_env.get_template('condition.xml')
    if self.pid in Problem.problems:  
      for c in Problem.problems[self.pid]:
        id = uid("Condition")
        print(template.render(dict(globals(), **locals())), end="", file=pfile)

    print ("\n</feed>", end="", file=pfile)
    pfile.close()
