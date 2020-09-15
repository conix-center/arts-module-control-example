import json
import uuid
import requests

class Type():
    rt = 'runtime'
    mod = 'module'

class Result():
    ok = 'ok'
    err = 'error'
    
class Action():
    create = 'create'
    delete = 'delete'
    update = 'update'
    
class FileType():   
    WA = 'WA'
    PY = 'PY'
    
class ARTSResponseMsg(dict):
    def __init__(self, r_uuid, result, details):
        dict.__init__(self, object_id=str(r_uuid), type='arts_resp', data={ 'result': result, 'details': details })

class ARTSRequestMsg(dict):
    def __init__(self, req_uuid, action, type, robj={}): 
        rdata = { 'type': type }
        rdata.update(robj)
        dict.__init__(self, object_id=req_uuid, action=action, type='arts_req', data=rdata)
        

class ARTSRESTRequest():
    def __init__(self, arts_addr): 
        if (not arts_addr.endswith("/")):
            arts_addr += "/"
        self.arts_addr = arts_addr
        
    def getRuntimes(self):
        r = requests.get(self.arts_addr+'runtimes/')
        return r.json()
        
    def getModules(self, rt_uuid=''):
        if len(rt_uuid) > 0:
            r = requests.get(self.arts_addr+'modules/'+rt_uuid+'/')
        else:
            r = requests.get(self.arts_addr+'modules/')
        return r.json()
