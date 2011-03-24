"""
Example SMArt REST Application: 

 * Required "admin" app privileges on smart container
 * Pushes data into the container using "Stage 1 Write API"

Josh Mandel
Children's Hospital Boston, 2011
"""

from smart_client.smart import SmartClient
from smart_client.common.util import *
import argparse, sys, os

# Basic configuration:  the consumer key and secret we'll use
# to OAuth-sign requests.
SMART_SERVER_OAUTH = {'consumer_key': 'smart-connector@apps.smartplatforms.org', 
                      'consumer_secret': 'smartapp-secret'}


# The SMArt contianer we're planning to talk to
SMART_SERVER_PARAMS = {
    'api_base' :          'http://localhost:7000'
}


def submit_data(args):
    client = get_smart_client()
    data = args.datafile.read() 
    method = getattr(client, args.method.lower())

#    print client.get(args.path)
    response = method(args.path, data)
    print response



"""Convenience function to initialize a new SmartClient"""
def get_smart_client(resource_tokens=None):
    ret = SmartClient(SMART_SERVER_OAUTH['consumer_key'], 
                       SMART_SERVER_PARAMS, 
                       SMART_SERVER_OAUTH,
                       resource_tokens)    
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test Data Writer')
    parser.add_argument('--path',dest='path', nargs='?',  help="specify path to post to, relative to container base (e.g. '/records/1234/medications/')", required=True)
    parser.add_argument('--method',dest='method', nargs='?',  help="specify HTTP method, defaults to POST", default='POST',choices=['POST','PUT'])
    parser.add_argument('--data', dest='datafile', nargs='?',  help="specify data to transmit, defaults to stdin", default=sys.stdout, type=argparse.FileType('r'))
    args = parser.parse_args()

    submit_data(args)
    

