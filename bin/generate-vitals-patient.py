import random

f = """male,2,0.88,90,42
male,2.5,0.92,92,48
male,2.6666666666666665,0.96,94,45
male,3.1666666666666665,0.99,98,52
male,4,1.06,102,56
male,4.5,1.1,104,62
male,5,1.12,106,64
male,5.25,1.14,105,65
male,5.25,1.14,107,67
male,5.5,1.16,113,71
male,5.75,1.18,113,72
male,5.916666666666667,1.19,112,73
male,6.25,1.22,112,71
male,6.5,1.23,110,69
male,6.75,1.24,106,65
male,7,1.24,104,63
male,7.25,1.28,106,65
male,7.5,1.29,106,68
male,7.75,1.31,106,63
male,7,1.32,108,69"""

ll = f.split("\n");
stats = [[float(x) for x in l.split(',')[1:]] for l in ll]

start = stats[0][1]
finish = stats[-1][1]

def interpolate(t):
  for i in range(1, len(stats)):
    if stats[i-1][0] <= t and stats[i][0] > t:
      return ((t-stats[i-1][0])*1.0 / (stats[i][0]-stats[i-1][0]), stats[i-1], stats[i])

  assert false, "couldn't interpolate %s"%t

def fuzz(ratio, t1, t2):
  ret = []
  for i in range(len(t1)):
    v = (1.0-ratio) * t1[i] + 1.0*ratio* t2[i]
    if i >1:  # don't allow date or height to jitter randomly
      v += random.gauss(0, (t1[i] - t2[i])/3)
    ret.append(v)
  return ret


from string import Template

from datetime import datetime, timedelta
birthday = datetime.now() - timedelta(days=stats[-1][0]*365)
def add_years(d1, y):
  return d1 + timedelta(days=365*y)

encounter_types = {"ambulatory": "ambulatory encounter",
        "inpatient": "inpatient encounter"}

def choose_encounter_type():
    n = random.uniform(0, 1)
    if n < .25:
        return "inpatient"
    return "ambulatory"


limbs = {"368209003": "right arm",
        "61396006": "left thigh"}
def choose_limb():
    n = random.uniform(0, 1)
    if n < .8:
        return "368209003"
    return "61396006"

methods = { "auscultation": "http://smartplatforms.org/terms/codes/BloodPressureMethod#auscultation",
            "machine": "http://smartplatforms.org/terms/codes/BloodPressureMethod#machine"
}
def choose_method():
    n = random.uniform(0, 1)
    if n < .5:
        return "auscultation"
    return "machine"
    
def register_code (code):
    if code not in codes:
        codes.append (code)
 
def getCodeFragment (code):

    if code.lower() == "inpatient":
    
        return """
  <spcode:EncounterType rdf:about="http://smartplatforms.org/terms/codes/EncounterType#inpatient">
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
    <dcterms:title>Inpatient encounter</dcterms:title>
    <sp:system>http://smartplatforms.org/terms/codes/EncounterType#</sp:system>
    <dcterms:identifier>inpatient</dcterms:identifier> 
  </spcode:EncounterType>
"""

    elif code.lower() == "ambulatory":
    
        return """
  <spcode:EncounterType rdf:about="http://smartplatforms.org/terms/codes/EncounterType#ambulatory">
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
    <dcterms:title>ambulatory encounter</dcterms:title>
    <sp:system>http://smartplatforms.org/terms/codes/EncounterType#</sp:system>
    <dcterms:identifier>ambulatory</dcterms:identifier> 
  </spcode:EncounterType>
"""

    elif code.lower() == "368209003":
    
        return """
  <spcode:BloodPressureBodySite rdf:about="http://purl.bioontology.org/ontology/SNOMEDCT/368209003">
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
    <dcterms:title>right arm</dcterms:title>
    <sp:system>http://purl.bioontology.org/ontology/SNOMEDCT/</sp:system>
    <dcterms:identifier>368209003</dcterms:identifier> 
  </spcode:BloodPressureBodySite>
"""
    
    elif code.lower() == "61396006":
    
        return """
  <spcode:BloodPressureBodySite rdf:about="http://purl.bioontology.org/ontology/SNOMEDCT/61396006">
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
    <dcterms:title>left thigh</dcterms:title>
    <sp:system>http://purl.bioontology.org/ontology/SNOMEDCT/</sp:system>
    <dcterms:identifier>61396006</dcterms:identifier> 
  </spcode:BloodPressureBodySite>
"""
    
    elif code.lower() == "auscultation":
    
        return """
  <spcode:BloodPressureMethod rdf:about="http://smartplatforms.org/terms/codes/BloodPressureMethod#auscultation">
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
    <dcterms:title>auscultation</dcterms:title>
    <sp:system>http://smartplatforms.org/terms/codes/BloodPressureMethod#</sp:system>
    <dcterms:identifier>auscultation</dcterms:identifier> 
  </spcode:BloodPressureMethod>
"""
    
    elif code.lower() == "machine":
    
            return """
  <spcode:BloodPressureMethod rdf:about="http://smartplatforms.org/terms/codes/BloodPressureMethod#machine">
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
    <dcterms:title>machine</dcterms:title>
    <sp:system>http://smartplatforms.org/terms/codes/BloodPressureMethod#</sp:system>
    <dcterms:identifier>machine</dcterms:identifier> 
  </spcode:BloodPressureMethod>
"""
def codesToRDF (codes):
    out = ""
    
    for c in codes:
        out += getCodeFragment(c)
        
    return out

header = """<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
  xmlns:sp="http://smartplatforms.org/terms#"
  xmlns:spcode="http://smartplatforms.org/terms/codes/"
  xmlns:foaf="http://xmlns.com/foaf/0.1/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:v="http://www.w3.org/2006/vcard/ns#">

<sp:MedicalRecord rdf:nodeID="patient">

</sp:MedicalRecord>
 
<sp:Demographics>
 <sp:belongsTo rdf:nodeID="patient"/>

 <v:n>
    <v:Name>
        <v:given-name>Allen</v:given-name>
        <v:family-name>Vitalis</v:family-name>
    </v:Name>
 </v:n>
 
 <v:adr>
    <v:Address>
      <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Home" />
      <v:street-address>83 Main St</v:street-address>
      <v:extended-address>Apt 6</v:extended-address>
      <v:locality>Medford</v:locality>
      <v:region>MA</v:region>
      <v:postal-code>02155</v:postal-code>
      <v:country>USA</v:country>
    </v:Address>
 </v:adr>
 
  <v:adr>
    <v:Address>
      <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Home" />
      <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Pref" />
      <v:street-address>17 Oak Rd</v:street-address>
      <v:locality>Belmont</v:locality>
      <v:region>MA</v:region>
      <v:postal-code>02478</v:postal-code>
      <v:country>USA</v:country>
    </v:Address>
 </v:adr>
 
 <v:tel>
    <v:Tel>
      <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Home" />
      <rdf:type rdf:resource="http://www.w3.org/2006/vcard/ns#Pref" />
      <rdf:value>800-834-9386</rdf:value>
    </v:Tel>
 </v:tel>
 
 <foaf:gender>male</foaf:gender>
 <v:bday>%s</v:bday>
 <v:email>allen.vitalis@example.com</v:email>
 
 <sp:medicalRecordNumber>
   <sp:Code>
    <dcterms:title>My Hospital Record 99912345</dcterms:title> 
    <dcterms:identifier>99912345</dcterms:identifier> 
    <sp:system>My Hospital Record</sp:system> 
   </sp:Code>
 </sp:medicalRecordNumber>
</sp:Demographics>
"""%birthday.strftime("%Y-%m-%d")

footer = """</rdf:RDF>"""

procedures = """
 <sp:Procedure>
    <sp:belongsTo rdf:nodeID="patient"/>
    <dcterms:date>2011-02-15</dcterms:date>
    <sp:procedureName>
      <sp:CodedValue>
          <dcterms:title></dcterms:title>
          <sp:code>
            <spcode:Procedure rdf:about="http://purl.bioontology.org/ontology/SNOMEDCT/80146002">
              <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
              <sp:system>http://purl.bioontology.org/ontology/SNOMEDCT/</sp:system>
              <dcterms:identifier>80146002</dcterms:identifier>
              <dcterms:title>Appendectomy</dcterms:title>
            </spcode:Procedure>    
          </sp:code>
      </sp:CodedValue>
    </sp:procedureName>
    <sp:provider>
      <sp:Provider>
        <v:n>
          <v:Name>
           <v:given-name>Joshua</v:given-name>
           <v:family-name>Mandel</v:family-name>
          </v:Name>
        </v:n>
      </sp:Provider>
    </sp:provider>
 </sp:Procedure>
"""

immunizations = """
   <sp:Immunization>
      <sp:belongsTo rdf:nodeID="patient"/>
	  <dcterms:date>2010-05-12T04:00:00Z</dcterms:date>

	  <sp:administrationStatus>
	    <sp:CodedValue>
	      <dcterms:title>Not Administered</dcterms:title>
	      <sp:code>
	        <sp:Code rdf:about="http://smartplatforms.org/terms/codes/ImmunizationAdministrationStatus#notAdministered">
	          <rdf:type rdf:resource="http://smartplatforms.org/terms/codes/ImmunizationAdministrationStatus" /> 
	          <dcterms:title>Not Administered</dcterms:title>
	          <sp:system>http://smartplatforms.org/terms/codes/ImmunizationAdministrationStatus#</sp:system>
	          <dcterms:identifier>notAdministered</dcterms:identifier>
	        </sp:Code>
	      </sp:code>
	    </sp:CodedValue>
	  </sp:administrationStatus>

	  <sp:refusalReason>
	    <sp:CodedValue>
	      <dcterms:title>Allergy to vaccine/vaccine components, or allergy to eggs</dcterms:title>
	      <sp:code>
	        <sp:Code rdf:about="http://smartplatforms.org/terms/codes/ImmunizationRefusalReason#allergy">
	          <rdf:type rdf:resource="http://smartplatforms.org/terms/codes/ImmunizationRefusalReason" /> 
	          <dcterms:title>Allergy to vaccine/vaccine components, or allergy to eggs</dcterms:title>
	          <sp:system>http://smartplatforms.org/terms/codes/ImmunizationRefusalReason#</sp:system>
	          <dcterms:identifier>allergy</dcterms:identifier>
	        </sp:Code>
	      </sp:code>
	    </sp:CodedValue>
	  </sp:refusalReason>

	  <sp:productName>
	    <sp:CodedValue>
	      <dcterms:title>typhoid, oral</dcterms:title>
	      <sp:code>
	        <sp:Code rdf:about="http://www2a.cdc.gov/nip/IIS/IISStandards/vaccines.asp?rpt=cvx#25">
	          <rdf:type rdf:resource="http://smartplatforms.org/terms/codes/ImmunizationProduct" /> 
	          <dcterms:title>typhoid, oral</dcterms:title>
	          <sp:system>http://www2a.cdc.gov/nip/IIS/IISStandards/vaccines.asp?rpt=vg#</sp:system>
	          <dcterms:identifier>25</dcterms:identifier>
	        </sp:Code>
	      </sp:code>
	    </sp:CodedValue>
	  </sp:productName>

	  <sp:productClass>
	    <sp:CodedValue>
	      <dcterms:title>TYPHOID</dcterms:title>
	      <sp:code>
	        <sp:Code rdf:about="http://www2a.cdc.gov/nip/IIS/IISStandards/vaccines.asp?rpt=vg#TYPHOID">
	          <rdf:type rdf:resource="http://smartplatforms.org/terms/codes/ImmunizationClass" /> 
	          <dcterms:title>TYPHOID</dcterms:title>
	          <sp:system>http://www2a.cdc.gov/nip/IIS/IISStandards/vaccines.asp?rpt=vg#</sp:system>
	          <dcterms:identifier>TYPHOID</dcterms:identifier>
	        </sp:Code>
	      </sp:code>
	    </sp:CodedValue>
	  </sp:productClass>

   </sp:Immunization>
"""

notes = """
<sp:ClinicalNote>
  <sp:belongsTo rdf:nodeID="patient"/>
  <dcterms:date>2012-05-17</dcterms:date>
  <dcterms:title>Telephone note</dcterms:title>
  <dcterms:format>
    <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/text/plain">
      <rdfs:label>text/plain</rdfs:label>
    </dcterms:MediaTypeOrExtent>
  </dcterms:format>
  <sp:provider>
    <sp:Provider>
      <v:n>
        <v:Name>
          <v:given-name>Joshua</v:given-name>
          <v:family-name>Mandel</v:family-name>
        </v:Name>
      </v:n>
    </sp:Provider>
  </sp:provider>
  <sp:resource>
    <sp:Resource>
        <sp:content>
            <sp:Content>
               <sp:encoding>UTF-8</sp:encoding>
               <sp:value>Patient's mother telephoned to say that he no longer needs documentation of a sports physical for school</sp:value>
            </sp:Content>
        </sp:content>
    </sp:Resource>
  </sp:resource>
</sp:ClinicalNote>
"""

medications = """  <sp:Medication>
 <sp:belongsTo rdf:nodeID="patient"/>
    <sp:startDate>2006-10-08</sp:startDate>
    <sp:instructions>7 mL bid x 10 days</sp:instructions>
    <sp:drugName>
      <sp:CodedValue>
        <dcterms:title>Cefdinir 25 MG/ML Oral Suspension</dcterms:title>
        <sp:code rdf:resource="http://purl.bioontology.org/ontology/RXNORM/309054"/>
      </sp:CodedValue>
    </sp:drugName>
    <sp:quantity>
      <sp:ValueAndUnit>
        <sp:unit>mL</sp:unit>
        <sp:value>7</sp:value>
      </sp:ValueAndUnit>
    </sp:quantity>
    <sp:frequency>
      <sp:ValueAndUnit>
        <sp:unit>/d</sp:unit>
        <sp:value>2</sp:value>
      </sp:ValueAndUnit>
    </sp:frequency>
  </sp:Medication>
  
  <sp:Medication>
 <sp:belongsTo rdf:nodeID="patient"/>
    <sp:drugName>
      <sp:CodedValue>
        <dcterms:title>Permethrin 10 MG/ML Topical Lotion</dcterms:title>
        <sp:code rdf:resource="http://purl.bioontology.org/ontology/RXNORM/312320"/>
      </sp:CodedValue>
    </sp:drugName>
    <sp:instructions>apply x1 as directed</sp:instructions>
    <sp:startDate>2009-08-03</sp:startDate>
  </sp:Medication>
  
  <sp:Code rdf:about="http://purl.bioontology.org/ontology/RXNORM/309054">
    <dcterms:title>Cefdinir 25 MG/ML Oral Suspension</dcterms:title>
    <dcterms:identifier>309054</dcterms:identifier>
    <rdf:type rdf:resource="http://smartplatforms.org/terms/codes/RxNorm_Semantic"/>
    <sp:system>http://purl.bioontology.org/ontology/RXNORM/</sp:system>
  </sp:Code>
  
  <sp:Code rdf:about="http://purl.bioontology.org/ontology/RXNORM/312320">
    <dcterms:title>Permethrin 10 MG/ML Topical Lotion</dcterms:title>
    <dcterms:identifier>312320</dcterms:identifier>
    <rdf:type rdf:resource="http://smartplatforms.org/terms/codes/RxNorm_Semantic"/>
    <sp:system>http://purl.bioontology.org/ontology/RXNORM/</sp:system>
  </sp:Code>"""

problems = """  <sp:Problem>
 <sp:belongsTo rdf:nodeID="patient"/>
    <sp:startDate>2008-10-06</sp:startDate>
    <sp:problemName>
      <sp:CodedValue>
        <sp:code rdf:resource="http://purl.bioontology.org/ontology/SNOMEDCT/425229001"/>
        <dcterms:title>foreign body in larynx</dcterms:title>
      </sp:CodedValue>
    </sp:problemName>
  </sp:Problem>
  
  <sp:Problem>
 <sp:belongsTo rdf:nodeID="patient"/>
    <sp:startDate>2006-07-18</sp:startDate>
    <sp:problemName>
      <sp:CodedValue>
        <sp:code rdf:resource="http://purl.bioontology.org/ontology/SNOMEDCT/65363002"/>
        <dcterms:title>otitis media</dcterms:title>
      </sp:CodedValue>
    </sp:problemName>
  </sp:Problem>
 
  <sp:Code rdf:about="http://purl.bioontology.org/ontology/SNOMEDCT/65363002">
    <sp:system>http://purl.bioontology.org/ontology/SNOMEDCT/</sp:system>
    <rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
    <dcterms:title>otitis media</dcterms:title>
    <dcterms:identifier>65363002</dcterms:identifier>
  </sp:Code>
  
  <sp:Code rdf:about="http://purl.bioontology.org/ontology/SNOMEDCT/425229001">
    <sp:system>http://purl.bioontology.org/ontology/SNOMEDCT/</sp:system>
    <rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
    <dcterms:title>foreign body in larynx</dcterms:title>
    <dcterms:identifier>425229001</dcterms:identifier>
  </sp:Code>"""

allergies = """  <sp:AllergyExclusion>
 <sp:belongsTo rdf:nodeID="patient"/>
    <dcterms:date>2008-05-05</dcterms:date>
    <sp:allergyExclusionName>
      <sp:CodedValue>
        <sp:code rdf:resource="http://purl.bioontology.org/ontology/SNOMEDCT/160244002"/>
        <dcterms:title>no known allergies</dcterms:title>
      </sp:CodedValue>
    </sp:allergyExclusionName>
  </sp:AllergyExclusion>
  
  <sp:Code rdf:about="http://purl.bioontology.org/ontology/SNOMEDCT/160244002">
    <sp:system>http://purl.bioontology.org/ontology/SNOMEDCT/</sp:system>
    <dcterms:title>no known allergies</dcterms:title>
    <rdf:type rdf:resource="http://smartplatforms.org/terms/codes/AllergyExclusion"/>
    <dcterms:identifier>160244002</dcterms:identifier>
  </sp:Code>"""
  
labs = """  <sp:LabResult>
 <sp:belongsTo rdf:nodeID="patient"/>
    <dcterms:date>2007-04-21</dcterms:date>
    <sp:narrativeResult>
      <sp:NarrativeResult>
        <sp:value>Normal</sp:value>
      </sp:NarrativeResult>
    </sp:narrativeResult>
    <sp:labName>
      <sp:CodedValue>
        <sp:code rdf:resource="http://purl.bioontology.org/ontology/LNC/38478-4"/>
        <dcterms:title>Biotinidase DBS Ql</dcterms:title>
      </sp:CodedValue>
    </sp:labName>
  </sp:LabResult>
  
  <sp:LabResult>
    <sp:belongsTo rdf:nodeID="patient"/>
    <dcterms:date>2007-09-08</dcterms:date>
    <sp:narrativeResult>
      <sp:NarrativeResult>
        <sp:value>Normal</sp:value>
      </sp:NarrativeResult>
    </sp:narrativeResult>
    <sp:labName>
      <sp:CodedValue>
        <sp:code rdf:resource="http://purl.bioontology.org/ontology/LNC/29571-7"/>
        <dcterms:title>Phe DBS Ql</dcterms:title>
      </sp:CodedValue>
    </sp:labName>
  </sp:LabResult>
  
  <spcode:LOINC rdf:about="http://purl.bioontology.org/ontology/LNC/29571-7">
    <dcterms:identifier>29571-7</dcterms:identifier>
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
    <dcterms:title>Phe DBS Ql</dcterms:title>
    <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
  </spcode:LOINC>
  
  <spcode:LOINC rdf:about="http://purl.bioontology.org/ontology/LNC/38478-4">
    <dcterms:identifier>38478-4</dcterms:identifier>
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
    <dcterms:title>Biotinidase DBS Ql</dcterms:title>
    <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
  </spcode:LOINC>"""
 
docs = """
    <sp:Document>
      <sp:belongsTo rdf:nodeID="patient"/>
      <sp:fileName>report4521.pdf</sp:fileName>
      <dcterms:title>A sample clinical report about the patient</dcterms:title>
      <dcterms:date>2010-05-12T04:00:00Z</dcterms:date>
      <dcterms:format>
        <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/pdf">
            <rdfs:label>application/pdf</rdfs:label>
        </dcterms:MediaTypeOrExtent>
      </dcterms:format>
      <sp:provider>
        <sp:Provider>
          <v:n>
            <v:Name>
             <v:given-name>John</v:given-name>
             <v:family-name>Smith</v:family-name>
            </v:Name>
          </v:n>
        </sp:Provider>
      </sp:provider>
      <sp:documentType>
          <sp:CodedValue>
            <dcterms:title>A report about the patient</dcterms:title>
            <sp:code>
              <spcode:DocumentType rdf:about="http://smartplatforms.org/terms/codes/DocumentType#report">
                <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" />
                <dcterms:title>A report about the patient</dcterms:title>
                <sp:system>http://smartplatforms.org/terms/codes/DocumentType#</sp:system>
                <dcterms:identifier>report</dcterms:identifier>
              </spcode:DocumentType>
            </sp:code>
          </sp:CodedValue>
      </sp:documentType>
    </sp:Document>
    <sp:Document>
      <sp:belongsTo rdf:nodeID="patient"/>
      <sp:fileName>reportScan713.png</sp:fileName>
      <dcterms:title>Image of a report received from NGD about the patient</dcterms:title>
      <dcterms:date>2010-05-12T04:00:00Z</dcterms:date>
      <dcterms:format>
        <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/image/png">
            <rdfs:label>image/png</rdfs:label>
        </dcterms:MediaTypeOrExtent>
      </dcterms:format>
      <sp:provider>
        <sp:Provider>
          <v:n>
            <v:Name>
             <v:given-name>John</v:given-name>
             <v:family-name>Smith</v:family-name>
            </v:Name>
          </v:n>
        </sp:Provider>
      </sp:provider>
      <sp:documentType>
          <sp:CodedValue>
            <dcterms:title>A digital image pertaining to the patient record</dcterms:title>
            <sp:code>
              <spcode:DocumentType rdf:about="http://smartplatforms.org/terms/codes/DocumentType#image">
                <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" />
                <dcterms:title>A digital image pertaining to the patient record</dcterms:title>
                <sp:system>http://smartplatforms.org/terms/codes/DocumentType#</sp:system>
                <dcterms:identifier>image</dcterms:identifier>
              </spcode:DocumentType>
            </sp:code>
          </sp:CodedValue>
      </sp:documentType>
      <sp:documentType>
          <sp:CodedValue>
            <dcterms:title>A report about the patient</dcterms:title>
            <sp:code>
              <spcode:DocumentType rdf:about="http://smartplatforms.org/terms/codes/DocumentType#report">
                <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" />
                <dcterms:title>A report about the patient</dcterms:title>
                <sp:system>http://smartplatforms.org/terms/codes/DocumentType#</sp:system>
                <dcterms:identifier>report</dcterms:identifier>
              </spcode:DocumentType>
            </sp:code>
          </sp:CodedValue>
      </sp:documentType>
    </sp:Document>
    <sp:Document>
      <sp:belongsTo rdf:nodeID="patient"/>
      <sp:fileName>notes6267.txt</sp:fileName>
      <dcterms:title>Notes about the patient</dcterms:title>
      <dcterms:date>2011-05-18T06:30:00Z</dcterms:date>
      <dcterms:format>
        <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/text/plain">
            <rdfs:label>text/plain</rdfs:label>
        </dcterms:MediaTypeOrExtent>
      </dcterms:format>
      <sp:provider>
        <sp:Provider>
          <v:n>
            <v:Name>
             <v:given-name>Peter</v:given-name>
             <v:family-name>Peterson</v:family-name>
            </v:Name>
          </v:n>
        </sp:Provider>
      </sp:provider>
      <sp:documentType>
          <sp:CodedValue>
            <dcterms:title>A clinical note about the patient</dcterms:title>
            <sp:code>
              <spcode:DocumentType rdf:about="http://smartplatforms.org/terms/codes/DocumentType#note">
                <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" />
                <dcterms:title>A clinical note about the patient</dcterms:title>
                <sp:system>http://smartplatforms.org/terms/codes/DocumentType#</sp:system>
                <dcterms:identifier>note</dcterms:identifier>
              </spcode:DocumentType>
            </sp:code>
          </sp:CodedValue>
      </sp:documentType>
    </sp:Document>
    <sp:ImagingStudy>
      <sp:belongsTo rdf:nodeID="patient"/>
      <dcterms:title>Knee MRI showing tissue damage</dcterms:title>
      <dcterms:date>2013-05-26T04:00:00Z</dcterms:date>
      <sp:accessionNumber>87654321</sp:accessionNumber>
      <sp:modality>
          <sp:CodedValue>
            <dcterms:title>Magnetic Resonance</dcterms:title>
            <sp:code>
              <spcode:DocumentType rdf:about="http://smartplatforms.org/terms/codes/ModalityType#MR">
                <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" />
                <dcterms:title>Magnetic Resonance</dcterms:title>
                <sp:system>http://smartplatforms.org/terms/codes/ModalityType#</sp:system>
                <dcterms:identifier>MR</dcterms:identifier>
              </spcode:DocumentType>
            </sp:code>
          </sp:CodedValue>
      </sp:modality>
      <sp:series>
      	<sp:Series>
          <sp:images rdf:parseType="Resource">
            <rdf:first>
                <sp:MedicalImage>
                  <sp:belongsTo rdf:nodeID="patient"/>
                  <sp:imagingStudy rdf:nodeID="patient" />
                  <sp:fileName>IM-0002-0001.dcm</sp:fileName>
                  <dcterms:title>Knee MRI showing tissue damage</dcterms:title>
                  <dcterms:date>2006-05-24T12:14:01.3421Z</dcterms:date>
                  <dcterms:format>
                    <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/dicom">
                        <rdfs:label>application/dicom</rdfs:label>
                    </dcterms:MediaTypeOrExtent>
                  </dcterms:format>
                </sp:MedicalImage>
            </rdf:first>
            <rdf:rest rdf:parseType="Resource">
                <rdf:first>
                    <sp:MedicalImage>
                      <sp:belongsTo rdf:nodeID="patient"/>
                      <sp:imagingStudy rdf:nodeID="patient" />
                      <sp:fileName>IM-0002-0001.dcm</sp:fileName>
                      <dcterms:title>Knee MRI showing tissue damage</dcterms:title>
                      <dcterms:date>2006-05-24T12:14:02.3421Z</dcterms:date>
                      <dcterms:format>
                        <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/dicom">
                            <rdfs:label>application/dicom</rdfs:label>
                        </dcterms:MediaTypeOrExtent>
                      </dcterms:format>
                    </sp:MedicalImage>
                </rdf:first>
                <rdf:rest rdf:parseType="Resource">
                    <rdf:first>
                        <sp:MedicalImage>
                          <sp:belongsTo rdf:nodeID="patient"/>
                          <sp:imagingStudy rdf:nodeID="patient" />
                          <sp:fileName>IM-0002-0001.dcm</sp:fileName>
                          <dcterms:title>Knee MRI showing tissue damage</dcterms:title>
                          <dcterms:date>2006-05-24T12:14:03.3421Z</dcterms:date>
                          <dcterms:format>
                            <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/dicom">
                                <rdfs:label>application/dicom</rdfs:label>
                            </dcterms:MediaTypeOrExtent>
                          </dcterms:format>
                        </sp:MedicalImage>
                    </rdf:first>
                    <rdf:rest rdf:resource="http://www.w3.org/1999/02/22-rdf-syntax-ns#nil"/>
                </rdf:rest>
            </rdf:rest>
          </sp:images>
      	</sp:Series>
      </sp:series>
      <sp:series>
      	<sp:Series>
          <sp:images rdf:parseType="Resource">
            <rdf:first>
                <sp:MedicalImage>
                  <sp:belongsTo rdf:nodeID="patient"/>
                  <sp:imagingStudy rdf:resource="http://sandbox-api.smartplatforms.org/records/99912345/imaging_studies/455" />
                  <sp:fileName>IM-0002-0001.dcm</sp:fileName>
                  <dcterms:title>Knee MRI showing tissue damage</dcterms:title>
                  <dcterms:date>2006-05-24T12:14:041.3421Z</dcterms:date>
                  <dcterms:format>
                    <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/dicom">
                        <rdfs:label>application/dicom</rdfs:label>
                    </dcterms:MediaTypeOrExtent>
                  </dcterms:format>
                </sp:MedicalImage>
            </rdf:first>
            <rdf:rest rdf:parseType="Resource">
                <rdf:first>
                    <sp:MedicalImage>
                      <sp:belongsTo rdf:nodeID="patient"/>
                      <sp:imagingStudy rdf:resource="http://sandbox-api.smartplatforms.org/records/99912345/imaging_studies/455" />
                      <sp:fileName>IM-0002-0001.dcm</sp:fileName>
                      <dcterms:title>Knee MRI showing tissue damage</dcterms:title>
                      <dcterms:date>2006-05-24T12:14:05.3421Z</dcterms:date>
                      <dcterms:format>
                        <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/dicom">
                            <rdfs:label>application/dicom</rdfs:label>
                        </dcterms:MediaTypeOrExtent>
                      </dcterms:format>
                    </sp:MedicalImage>
                </rdf:first>
                <rdf:rest rdf:resource="http://www.w3.org/1999/02/22-rdf-syntax-ns#nil"/>
            </rdf:rest>
          </sp:images>
      	</sp:Series>
      </sp:series>
    </sp:ImagingStudy>
    <sp:ImagingStudy>
      <sp:belongsTo rdf:nodeID="patient"/>
      <dcterms:title>Chest CT scan to study bone structure</dcterms:title>
      <dcterms:date>2013-05-27T02:30:00Z</dcterms:date>
      <sp:accessionNumber>98765432</sp:accessionNumber>
      <sp:modality>
          <sp:CodedValue>
            <dcterms:title>Computed Tomography</dcterms:title>
            <sp:code>
              <spcode:DocumentType rdf:about="http://smartplatforms.org/terms/codes/ModalityType#CT">
                <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" />
                <dcterms:title>Computed Tomography</dcterms:title>
                <sp:system>http://smartplatforms.org/terms/codes/ModalityType#</sp:system>
                <dcterms:identifier>CT</dcterms:identifier>
              </spcode:DocumentType>
            </sp:code>
          </sp:CodedValue>
      </sp:modality>
      <sp:series>
      	<sp:Series>
          <dcterms:title>Upper chest area</dcterms:title>
          <sp:images rdf:parseType="Resource">
            <rdf:first>
                <sp:MedicalImage>
                  <sp:belongsTo rdf:nodeID="patient"/>
                  <sp:imagingStudy rdf:resource="http://sandbox-api.smartplatforms.org/records/99912345/imaging_studies/456" />
                  <sp:fileName>IM-0002-0001.dcm</sp:fileName>
                  <dcterms:title>Image from chest CT scan to study bone structure</dcterms:title>
                  <dcterms:date>2004-09-30T12:14:02.3421Z</dcterms:date>
                  <dcterms:format>
                    <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/dicom">
                        <rdfs:label>application/dicom</rdfs:label>
                    </dcterms:MediaTypeOrExtent>
                  </dcterms:format>
                </sp:MedicalImage>
            </rdf:first>
            <rdf:rest rdf:parseType="Resource">
                <rdf:first>
                    <sp:MedicalImage>
                      <sp:belongsTo rdf:nodeID="patient"/>
                      <sp:imagingStudy rdf:nodeID="patient" />
                      <sp:fileName>IM-0002-0001.dcm</sp:fileName>
                      <dcterms:title>Image from chest CT scan to study bone structure</dcterms:title>
                      <dcterms:date>2004-09-30T12:14:03.3421Z</dcterms:date>
                      <dcterms:format>
                        <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/dicom">
                            <rdfs:label>application/dicom</rdfs:label>
                        </dcterms:MediaTypeOrExtent>
                      </dcterms:format>
                    </sp:MedicalImage>
                </rdf:first>
                <rdf:rest rdf:parseType="Resource">
                    <rdf:first>
                        <sp:MedicalImage>
                          <sp:belongsTo rdf:nodeID="patient"/>
                          <sp:imagingStudy rdf:nodeID="patient" />
                          <sp:fileName>IM-0002-0001.dcm</sp:fileName>
                          <dcterms:title>Image from chest CT scan to study bone structure</dcterms:title>
                          <dcterms:date>2004-09-30T12:14:04.3421Z</dcterms:date>
                          <dcterms:format>
                            <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/dicom">
                                <rdfs:label>application/dicom</rdfs:label>
                            </dcterms:MediaTypeOrExtent>
                          </dcterms:format>
                        </sp:MedicalImage>
                    </rdf:first>
                    <rdf:rest rdf:resource="http://www.w3.org/1999/02/22-rdf-syntax-ns#nil"/>
                </rdf:rest>
            </rdf:rest>
          </sp:images>
      	</sp:Series>
      </sp:series>
      <sp:series>
      	<sp:Series>
          <dcterms:title>Lower chest area</dcterms:title>
          <sp:images rdf:parseType="Resource">
            <rdf:first>
                <sp:MedicalImage>
                  <sp:belongsTo rdf:nodeID="patient"/>
                  <sp:imagingStudy rdf:nodeID="patient" />
                  <sp:fileName>IM-0002-0001.dcm</sp:fileName>
                  <dcterms:title>Image from chest CT scan to study bone structure</dcterms:title>
                  <dcterms:date>2004-09-30T12:14:00.6848Z</dcterms:date>
                  <sp:dicomStudyUID>53722</sp:dicomStudyUID>
                  <sp:dicomSeriesUID>748225</sp:dicomSeriesUID>
                  <sp:dicomImageUID>60937345</sp:dicomImageUID>
                  <dcterms:format>
                    <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/dicom">
                        <rdfs:label>application/dicom</rdfs:label>
                    </dcterms:MediaTypeOrExtent>
                  </dcterms:format>
                </sp:MedicalImage>
            </rdf:first>
            <rdf:rest rdf:parseType="Resource">
                <rdf:first>
                    <sp:MedicalImage>
                      <sp:belongsTo rdf:nodeID="patient"/>
                      <sp:imagingStudy rdf:nodeID="patient" />
                      <sp:fileName>IM-0002-0001.dcm</sp:fileName>
                      <dcterms:title>Image from chest CT scan to study bone structure</dcterms:title>
                      <dcterms:date>2004-09-30T12:14:01.3421Z</dcterms:date>
                      <dcterms:format>
                        <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/application/dicom">
                            <rdfs:label>application/dicom</rdfs:label>
                        </dcterms:MediaTypeOrExtent>
                      </dcterms:format>
                    </sp:MedicalImage>
                </rdf:first>
                <rdf:rest rdf:resource="http://www.w3.org/1999/02/22-rdf-syntax-ns#nil"/>
            </rdf:rest>
          </sp:images>
      	</sp:Series>
      </sp:series>
    </sp:ImagingStudy>    
    <sp:Photograph>
      <sp:belongsTo rdf:nodeID="patient"/>
      <sp:fileName>photo831.jpg</sp:fileName>
      <dcterms:title>Head photograph of the patient</dcterms:title>
      <dcterms:date>2010-05-12T04:00:00Z</dcterms:date>
      <dcterms:format>
        <dcterms:MediaTypeOrExtent rdf:about="http://purl.org/NET/mediatypes/image/jpeg">
            <rdfs:label>image/jpeg</rdfs:label>
        </dcterms:MediaTypeOrExtent>
      </dcterms:format>
    </sp:Photograph>
    """

extravitals = """
 <sp:VitalSignSet>
 <sp:belongsTo rdf:nodeID="patient"/>
    <dcterms:date>2010-08-12T04:00:00Z</dcterms:date>
    <sp:encounter>
      <sp:Encounter>
      <sp:belongsTo rdf:nodeID="patient"/>
      <sp:startDate>2010-08-12T04:00:00Z</sp:startDate>
      <sp:endDate>2010-08-12T04:20:00Z</sp:endDate>
      <sp:encounterType>
        <sp:CodedValue>
         <dcterms:title>ambulatory encounter</dcterms:title>
          <sp:code>
           <spcode:EncounterType rdf:about="http://smartplatforms.org/terms/codes/EncounterType#ambulatory" >
             <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
             <dcterms:title>ambulatory encounter</dcterms:title>
             <sp:system>http://smartplatforms.org/terms/codes/EncounterType#</sp:system>
             <dcterms:identifier>ambulatory</dcterms:identifier> 
           </spcode:EncounterType>    
          </sp:code>
        </sp:CodedValue>
      </sp:encounterType>
    </sp:Encounter>
    </sp:encounter>
    <sp:headCircumference>
      <sp:VitalSign>
       <sp:vitalName>
        <sp:CodedValue>
          <dcterms:title>Head circumference</dcterms:title>
          <sp:code>    
            <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/8287-5">
              <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
              <dcterms:title>Head circumference</dcterms:title>
              <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
              <dcterms:identifier>8287-5</dcterms:identifier> 
            </spcode:VitalSign>
          </sp:code>
        </sp:CodedValue>
      </sp:vitalName>
      <sp:value>51.2</sp:value>
      <sp:unit>cm</sp:unit>
     </sp:VitalSign>
    </sp:headCircumference>
    <sp:height>
      <sp:VitalSign>
       <sp:vitalName>
        <sp:CodedValue>
          <dcterms:title>body height</dcterms:title>
          <sp:code>
            <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/8302-2">
              <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
              <dcterms:title>body height</dcterms:title>
              <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
              <dcterms:identifier>8302-2</dcterms:identifier> 
            </spcode:VitalSign>    
          </sp:code>
        </sp:CodedValue>
      </sp:vitalName>
      <sp:value>119</sp:value>
      <sp:unit>cm</sp:unit>
     </sp:VitalSign>
    </sp:height>
    <sp:weight>
      <sp:VitalSign>
       <sp:vitalName>
        <sp:CodedValue>
          <dcterms:title>body weight</dcterms:title>
          <sp:code>    
            <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/3141-9">
              <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
              <dcterms:title>body weight</dcterms:title>
              <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
              <dcterms:identifier>3141-9</dcterms:identifier> 
            </spcode:VitalSign>
          </sp:code>
        </sp:CodedValue>
      </sp:vitalName>
      <sp:value>23</sp:value>
      <sp:unit>kg</sp:unit>
     </sp:VitalSign>
    </sp:weight>
    <sp:bodyMassIndex>
      <sp:VitalSign>
       <sp:vitalName>
        <sp:CodedValue>
          <dcterms:title>body mass index</dcterms:title>
          <sp:code>
            <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/39156-5">
              <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
              <dcterms:title>body mass index</dcterms:title>
              <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
              <dcterms:identifier>39156-5</dcterms:identifier> 
            </spcode:VitalSign>        
          </sp:code>
        </sp:CodedValue>
      </sp:vitalName>
      <sp:value>16.2</sp:value>
      <sp:unit>kg/m2</sp:unit>
     </sp:VitalSign>
    </sp:bodyMassIndex>
    <sp:respiratoryRate>
      <sp:VitalSign>
       <sp:vitalName>
        <sp:CodedValue>
          <dcterms:title>respiration rate</dcterms:title>
          <sp:code>
            <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/9279-1">
              <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
              <dcterms:title>respiration rate</dcterms:title>
              <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
              <dcterms:identifier>9279-1</dcterms:identifier> 
            </spcode:VitalSign>    
          </sp:code>
        </sp:CodedValue>
      </sp:vitalName>
      <sp:value>16</sp:value>
      <sp:unit>{breaths}/min</sp:unit>
     </sp:VitalSign>
    </sp:respiratoryRate>
    <sp:heartRate>
      <sp:VitalSign>
       <sp:vitalName>
        <sp:CodedValue>
          <dcterms:title>heart rate</dcterms:title>
          <sp:code>
             <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/8867-4">
               <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
               <dcterms:title>heart rate</dcterms:title>
               <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
               <dcterms:identifier>8867-4</dcterms:identifier> 
             </spcode:VitalSign>
          </sp:code>
        </sp:CodedValue>
      </sp:vitalName>
      <sp:value>90</sp:value>
      <sp:unit>{beats}/min</sp:unit>
     </sp:VitalSign>
    </sp:heartRate>
    <sp:oxygenSaturation>
      <sp:VitalSign>
       <sp:vitalName>
        <sp:CodedValue>
          <dcterms:title>oxygen saturation</dcterms:title>
          <sp:code>
            <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/2710-2">
              <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
              <dcterms:title>oxygen saturation</dcterms:title>
              <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
              <dcterms:identifier>2710-2</dcterms:identifier> 
            </spcode:VitalSign>        
          </sp:code>
        </sp:CodedValue>
      </sp:vitalName>
      <sp:value>99</sp:value>
      <sp:unit>%{HemoglobinSaturation}</sp:unit>
     </sp:VitalSign>
    </sp:oxygenSaturation>
    <sp:temperature>
      <sp:VitalSign>
       <sp:vitalName>
        <sp:CodedValue>
          <dcterms:title>body temperature</dcterms:title>
          <sp:code>
            <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/8310-5">
              <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
              <dcterms:title>body temperature</dcterms:title>
              <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
              <dcterms:identifier>8310-5</dcterms:identifier> 
            </spcode:VitalSign>        
          </sp:code>
        </sp:CodedValue>
      </sp:vitalName>
      <sp:value>37</sp:value>
      <sp:unit>Cel</sp:unit>
     </sp:VitalSign>
    </sp:temperature>
 </sp:VitalSignSet>
"""

vitals_codes = """
  <spcode:BloodPressureBodyPosition rdf:about="http://purl.bioontology.org/ontology/SNOMEDCT/33586001">
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
    <dcterms:title>sitting</dcterms:title>
    <sp:system>http://purl.bioontology.org/ontology/SNOMEDCT/</sp:system>
    <dcterms:identifier>33586001</dcterms:identifier> 
  </spcode:BloodPressureBodyPosition>

  <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/8462-4">
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
    <dcterms:title>intravascular diastolic</dcterms:title>
    <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
    <dcterms:identifier>8462-4</dcterms:identifier> 
  </spcode:VitalSign>

  <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/8480-6">
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
    <dcterms:title>intravascular systolic</dcterms:title>
    <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
    <dcterms:identifier>8480-6</dcterms:identifier> 
  </spcode:VitalSign>

  <spcode:VitalSign rdf:about="http://purl.bioontology.org/ontology/LNC/8302-2">
    <rdf:type rdf:resource="http://smartplatforms.org/terms#Code" /> 
    <dcterms:title>body height</dcterms:title>
    <sp:system>http://purl.bioontology.org/ontology/LNC/</sp:system>
    <dcterms:identifier>8302-2</dcterms:identifier> 
  </spcode:VitalSign>
"""

def tordf(v, include_height=False, include_bp=False):
  h = Template("""<sp:height>
      <sp:VitalSign>
       <sp:vitalName>
        <sp:CodedValue>
          <sp:code rdf:resource="http://purl.bioontology.org/ontology/LNC/8302-2"/>
          <dcterms:title>body height</dcterms:title>
        </sp:CodedValue>
      </sp:vitalName>
      <sp:value>$height</sp:value>
      <sp:unit>cm</sp:unit>
     </sp:VitalSign>
    </sp:height>
""")

  bp = Template("""    <sp:bloodPressure>
      <sp:BloodPressure>
       <sp:systolic>
         <sp:VitalSign>
          <sp:vitalName>
           <sp:CodedValue>
             <sp:code rdf:resource="http://purl.bioontology.org/ontology/LNC/8480-6"/>
             <dcterms:title>systolic blood pressure</dcterms:title>
           </sp:CodedValue>
         </sp:vitalName>
         <sp:value>$sbp</sp:value>
         <sp:unit>mm[Hg]</sp:unit>
        </sp:VitalSign>
       </sp:systolic>
       <sp:diastolic>
         <sp:VitalSign>
          <sp:vitalName>
           <sp:CodedValue>
             <sp:code rdf:resource="http://purl.bioontology.org/ontology/LNC/8462-4"/>
             <dcterms:title>diastolic blood pressure</dcterms:title>
           </sp:CodedValue>
         </sp:vitalName>
         <sp:value>$dbp</sp:value>
         <sp:unit>mm[Hg]</sp:unit>
        </sp:VitalSign>
       </sp:diastolic>
       <sp:bodyPosition>
         <sp:CodedValue>
           <sp:code rdf:resource="http://purl.bioontology.org/ontology/SNOMEDCT/33586001"/>
           <dcterms:title>sitting</dcterms:title>
         </sp:CodedValue>
       </sp:bodyPosition>
       <sp:bodySite>
         <sp:CodedValue>
           <sp:code rdf:resource="http://purl.bioontology.org/ontology/SNOMEDCT/$limb"/>
           <dcterms:title>$limbn</dcterms:title>
         </sp:CodedValue>
       </sp:bodySite>
       <sp:method>
         <sp:CodedValue>
           <sp:code rdf:resource="$method"/>
           <dcterms:title>$methodn</dcterms:title>
         </sp:CodedValue>
       </sp:method>
      </sp:BloodPressure>
    </sp:bloodPressure>
""")

  r = Template("""
 <sp:VitalSignSet>
    <sp:belongsTo rdf:nodeID="patient"/>
    <dcterms:date>$vitals_date</dcterms:date>
    <sp:encounter>
     <sp:Encounter>
        <sp:belongsTo rdf:nodeID="patient"/>
        <sp:startDate>$encounter_start_date</sp:startDate>
        <sp:endDate>$encounter_end_date</sp:endDate>
          <sp:encounterType>
        <sp:CodedValue>
          <sp:code rdf:resource="http://smartplatforms.org/terms/codes/EncounterType#$encounter_type"/>
          <dcterms:title>$encounter_type_name</dcterms:title>
        </sp:CodedValue>
          </sp:encounterType>
     </sp:Encounter>
    </sp:encounter>
$h
$bp
 </sp:VitalSignSet>
""")

  et = choose_encounter_type()
  etn = encounter_types[et]
  register_code (et)

  limb = choose_limb()
  limbn = limbs[limb]
  register_code (limb)

  methodn = choose_method()
  method = methods[methodn]
  register_code (methodn)


  if include_height:
    h = h.substitute(height=v[1] * 100)
  else: h = ""

  if include_bp:
    bp = bp.substitute(sbp=v[2], dbp=v[3],  limb=limb, limbn=limbn, method=method,methodn=methodn)
  else: bp=""


  return r.substitute(vitals_date=add_years(birthday, v[0]).isoformat(),
            encounter_start_date=add_years(birthday, v[0]).isoformat(),
            encounter_end_date=add_years(birthday, v[0]).isoformat(),
            encounter_type=et,
            encounter_type_name=etn,
            h=h, bp=bp)


codes = []
a = []
for p in range(50):
  t = random.uniform(stats[0][0], stats[-1][0])
  r,t1,t2 = interpolate(t)
  v = fuzz(r,t1,t2)
  a.append(v)

print header
a.sort(key=lambda x: x[0])
for l in a:
  include_height=(random.random()<0.2)
  include_bp=not include_height
  print tordf(l, include_height, include_bp)
print codesToRDF (codes)
print vitals_codes
print medications
print problems
print procedures
print immunizations
print allergies
print labs
print extravitals
print docs
print notes
print footer
