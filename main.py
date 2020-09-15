"""
*TL;DR
Example showing how to create ARTS requests to create/delete modules (WASM or Python programs)
"""

import paho.mqtt.publish as publish
import json 
import time
import pprint

from arts.module import Module
from arts.artsrequests import Action, FileType, ARTSRESTRequest

CFG_FILE = 'config.json' 

class Settings(dict):
    
    def __init__(self, cfg_file):
        with open(CFG_FILE) as json_data_file:
            s_dict = json.load(json_data_file)

        dict.__init__(self, s_dict)

def main():

    # json pretty printer
    pp = pprint.PrettyPrinter(indent=4)

    # load settings from json file
    settings = Settings(CFG_FILE)
    
    # create ARTSRESTRequest object to query arts
    artsRest = ARTSRESTRequest(settings['arts']['rest_url'])
    
    # create environment variables to be passed as a *space-separated* string
    env = 'SCENE=roomtest6 MQTTH=' + settings['mqtt']['host'] + ' REALM=' + settings['arts']['realm']
    
    # create a module object
    # the minimal arguments to create a module are name and filename (env is optional)
    # these are all the arguments that can be passed and their defaults:
    #    mod_name, mod_filename, mod_uuid=uuid.uuid4(), parent_rt=None, mod_ft=FileType.PY, mod_args='', mod_env=''
    #    Note: filetype will be inferred from filename extension (.py or .wasm)
    mod = Module("wiselab/boxes", "boxes.py", mod_env=env)

    # we can create a module object to a running module (for example, to send a delete request), if we know its uuid:
    # mod = Module("wiselab/boxes", "boxes.py", mod_uuid='4264bac8-13ed-453b-b157-49cc2421a112')
    
    # get arts request json string (req_uuid will be used to confirm the request)
    req_uuid, artsModCreateReq = mod.artsReqJson(Action.create)
    print(artsModCreateReq)
    
    # publish request
    publish.single(settings['arts']['ctl'], artsModCreateReq, hostname=settings['mqtt']['host'])

    # TODO: we can check for arts confirmation:
    #  1. subscribe to reg topic (settings['arts']['ctl'])
    #  2. look for message of type "arts_resp", with the object_id set to the value of req_uuid we saved before

    # we can use arts rest interface to query existing modules
    modulesJson = artsRest.getModules()
    print('** These are all the modules known to ARTS:')
    pp.pprint(modulesJson)

    # query for modules of a particular runtime, given its uuid:
    #  modulesJson = artsRest.getRuntimes('a69e075c-51e5-4555-999c-c49eb283dc1d')
    #
    # we can also query arts for runtimes:
    #  runtimesJson = artsRest.getRuntimes()

    # wait for user
    input("Press Enter to kill the module...")
    
    # kill the module
    req_uuid, artsModDeleteReq = mod.artsReqJson(Action.delete)
    print(artsModDeleteReq)
    publish.single(settings['arts']['ctl'], artsModDeleteReq, hostname=settings['mqtt']['host'])
    
if __name__ == "__main__":
    main()
    
