from random import randint
import datetime

# Constants for building test data from data 

# Paths relative source data and mapping files
DATA_PATH  = "../data/"
MAP_PATH   =   "../maps/"
RI_PATH   = "../ri-data/"

# Data file names:
PATIENTS_FILE  = DATA_PATH+'patients.txt'
LABS_FILE   = DATA_PATH+'labs.txt'
MEDS_FILE  = DATA_PATH+'meds.txt'
PROBLEMS_FILE = DATA_PATH+'problems.txt'
REFILLS_FILE = DATA_PATH+'refills.txt'
RI_PATIENTS_FILE = RI_PATH+'ri-patients.txt'

# Mapping file names:
LOINC_FILE = MAP_PATH+'short_loinc.txt'

# Define some values for generating random demographics data
# These values can be freely altered to change locations and names

# Zip Code Choices: Tulsa, OK 
# Note weighting for population density by repeats:
ZIPS = ('74008','74008','74008', # repeated three times--largest population
        '74047','74047', # repeated twice, less population
        '74066','74063','74014','74126','74117','74116','74108')

# Names for randomization, roughly adapted from US Census most common names:
MALES = ('James','John','Robert','Michael','William','David','Richard','Charles',
        'Joseph','Thomas','Christopher','Daniel','Paul','Mark','Donald','George',
        'Kenneth','Steven','Edward','Brian','Ronald','Anthony','Kevin','Jason',
        'Frank','Scott','Eric','Stephan','Joshua','Patrick','Harold','Carl')

FEMALES = ('Mary','Patricia','Linda','Barbara','Elizabeth','Jennifer','Maria',
           'Susan','Margaret','Dorothy','Lisa','Nancy','Karen','Betty','Helen',
           'Sandra','Donna','Carol','Ruth','Sharon','Michelle','Laura','Sarah',
           'Kimberly','Jessica','Shirley','Cynthia','Melissa','Brenda','Amy')

SURNAMES = ('Smith','Johnson','Williams','Jones','Brown','Davis','Miller','Wilson',
          'Moore','Taylor','Anderson','Thomas','Jackson','White','Harris','Gracia',
          'Robinson','Clark','Lewis','Lee','Hall','Allen','Young','Hill','Green',
          'Adams','Baker','Nelson','Campbell','Parker','Collins','Rodgers','Reed',
          'Cook','Morgan','Brooks','Kelly','James','Bennett','Woods','Ross','Long',
          'Hughes','Butler','Coleman','Jenkins','Barnes','Ford','Graham','Owens',
          'Cole','West','Diaz','Gibson','Rice','Shaw','Hunt','Black','Palmer')

# Utility Functions for generating randomized data

def rndDate(y):
   """Returns a random date within a given year."""

   d = datetime.date(y,1,1)      # Start with Jan 1st
   ylen = 365 if y%4 else 366    # Adjust year length for leap years
   r = randint(0,ylen-1)         # Generate random day in year   
   return datetime.date.fromordinal(d.toordinal()+r)

def rndName(gender):
   """Returns a random, gender appropriate, common name tuple: (fn,ln)"""
   fnames = MALES if gender=='M' else FEMALES
   return (fnames[randint(0,len(fnames)-1)],SURNAMES[randint(0,len(SURNAMES)-1)]) 

def rndZip():
  """
  Returns a random zipcode"""
  return ZIPS[randint(0,len(ZIPS)-1)]

def rndAccNum():
  """ Returns a random accession number """
  return "A%d"%randint(100000000,999999999)

