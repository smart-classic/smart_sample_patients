from string import Template
from patient import Patient
from med import Med
from problem import Problem
from refill import Refill
from lab import Lab
import os

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
        <unit type="http://unitsofmeasure.org/" value="$units">$units</unit>
      </valueAndUnit>
      <normalRange>
        <minimum>$low</minimum>
        <maximum>$high</maximum>
        <unit type="http://unitsofmeasure.org/" value="$units">$units</unit>
      </normalRange>
    </result>    
  </labTest>
</Lab>
""")

contact = Template("""
<Contact xmlns="http://indivo.org/vocab/xml/documents#">
  <name>
    <fullName>$fullname</fullName>
    <givenName>$firstname</givenName>
    <familyName>$lastname</familyName>
  </name>
  <email type="personal">
    <emailAddress>$email</emailAddress>
  </email>
  <address type="home">
    <streetAddress>$street</streetAddress>
    <postalCode>$postal</postalCode>
    <locality>$city</locality>
    <region>$state</region>
    <country>$country</country>
  </address>
  <phoneNumber type="home">$hphone</phoneNumber>
  <phoneNumber type="cell">$cphone</phoneNumber>
</Contact>
""")

def writePatientData(sample_data_dir, pid):
   """Writes a patient's data to an Indivo sample data profile under 'sample_data_dir'."""
   p = Patient.mpi[pid]
   fullname = '%s %s'%(p.fname, p.lname)

   print "adding SMART data to data profile %s: %s"%(pid, fullname)

   # Build up XML for all of the patient's data
   problems = []
   meds = []
   labs = []

   demographics_doc = demographics.substitute(dob=p.dob, gender=p.gender)

   contact_data = {
       'fullname': fullname,
       'firstname': p.fname,
       'lastname': p.lname,
       'email': p.email,
       'street': p.street,
       'postal': p.zip,
       'city': p.city,
       'state': p.region,
       'country': p.country,
       'hphone': p.home,
       'cphone':p.cell,
       }
   contact_doc = contact.substitute(**contact_data)

   if pid in Lab.results:
      
      for l in Lab.results[pid]:
         if l.scale != 'Qn': continue
         labs.append(lab.substitute(date=l.date,
                                    loinc=l.code,
                                    name=l.name,
                                    value=l.value,
                                    units=l.units,
                                    low=l.low,
                                    high=l.high))                        

   if pid in Problem.problems: 
      for prob in Problem.problems[pid]:
          problems.append(problem.substitute(onset=prob.start, 
                                             snomed=prob.snomed, 
                                             name=prob.name))

   if  pid in Med.meds: 
      for m in Med.meds[pid]:
         frequency = ""
         try: frequency="%s %s"%(m.freq, m.frequnit)
         except: pass

         if not m.qtt:
            m.qtt="1"
            m.qttunit="{tablet}"
            
         meds.append(med.substitute(startDate=m.start,
                                    rxnorm=m.rxn, 
                                    name=m.name, 
                                    quantityValue=m.qtt, 
                                    quantityUnits=m.qttunit, 
                                    frequency=frequency,
                                    instructions=m.sig))
         
   # create a directory for the patient
   OUTPUT_DIR = os.path.join(sample_data_dir, "patient_%s"%pid)

   try:
       os.mkdir(OUTPUT_DIR)

       # create a demographics file
       with open(os.path.join(OUTPUT_DIR, "Demographics.xml"), 'w') as demo:
           demo.write(demographics_doc)

       # create a contact document
       with open(os.path.join(OUTPUT_DIR, "Contact.xml"), 'w') as cont:
           cont.write(contact_doc)

       # create the rest of the data:
       for i, doc in enumerate(problems + meds + labs):
           with open(os.path.join(OUTPUT_DIR, "doc_%s.xml"%i), 'w') as d:
               d.write(doc)

   except OSError:
       print "Patient with id %s already exists, skipping..."%pid
