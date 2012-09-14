from common.rdf_tools.util import *
from common.rdf_tools import rdf_ontology
import argparse

cv = rdf_ontology.SMART_Class["http://smartplatforms.org/terms#CodedValue"]

def code(g, uri):
    types = filter(lambda x: x[2] != owl.NamedIndividual, 
                cv.graph.triples((uri, rdf.type, None)))

    assert len(types)>0, "No types for %s"%uri.n3()

    g.add((uri, rdf.type, sp.Code))
    for t in types:
        t = t[2]
        g.add((uri, rdf.type, t))
    
    if "#" in str(uri):
        sep="#"
    else:
        sep="/"
        
    (sys, ident) = str(uri).rsplit(sep,1)
        
    g.add((uri, sp.system, Literal(sys+sep)))
    g.add((uri, dcterms.identifier, Literal(ident)))

    titles = list(cv.graph.triples((uri, dcterms.title, None)))
    assert len(titles) == 1, "did not find exactly one title: %s"%titles
    title = titles[0][2]
    g.add((uri, dcterms.title, title))

    return uri

def coded_value(g, uri):
    code(g, uri)

    titles = list(g.triples((uri, dcterms.title, None)))
    assert len(titles) == 1, "did not find exactly one title: %s"%titles
    title = titles[0][2]

    cvnode = BNode()
    g.add((cvnode, rdf.type, sp.CodedValue))
    g.add((cvnode, dcterms.title, title))
    g.add((cvnode, sp.code, uri))

    return cvnode

if __name__== '__main__':

  parser = argparse.ArgumentParser(description='Ontology Codes Module')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--uri', action='store_true', help='Get CodedValue for URI',
          default='http://smartplatforms.org/terms/codes/ImmunizationRefusalReason#documentedImmunityOrPreviousDisease')
  args = parser.parse_args()
 
  if args.uri:
      g = rdflib.Graph()
      coded_value(g, URIRef(args.uri))
      print g.serialize()
