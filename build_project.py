#!/usr/bin/python
import sys
import os
import os.path
import re
import json
import subprocess
import argparse

def expand_string( string, macros, params=None, max=10 ):
    if type(string) == list:
        string=u"\n".join(list)
    elif type(string) not in (str, unicode):
        return string
    pdict = {}
    if type(params) == dict:
        pdict = params
    elif type(params) in (str, unicode) and params != '':
        for ds in params.split(';'):
            m = re.match(r"(\w+)\=(.*)",ds)
            if m:
                pdict[m.group(1)]=m.group(2)
    rdict = {}
    for k in pdict:
        rdict[k] = macros.get(k)
        macros[k] = pdict[k]

    string=re.sub(r"\{(\w+)(?:\:([^{}]*))?\}",
                      lambda x: expand_string(macros.get(x.group(1),""),macros,x.group(2),max-1),
                      string)

    for k in rdict:
        if rdict[k] == None:
            del macros[k]
        else:
            macros[k] = rdict[k]
    return string

def expand_template( template, macros ): 
    if type(template) == list:
        return [expand_template(x,macros) for x in template]
    elif type(template) == dict:
        return {k:expand_template(v,macros) for k,v in template.items()}
    elif type(template) in (str,unicode):
        return expand_string(template,macros)
    else:
        return template


parser = argparse.ArgumentParser('Build a tilemill project')
parser.add_argument('-c','--config',help='Configuration file overriding defaults from build_project.cfg')
parser.add_argument('-p','--project',help='Output project file',default='project.mml')
parser.add_argument('-l','--layers',help='File of layers (overriding configuration)')
parser.add_argument('--clean',action='store_true', help='Clear filecache before starting')
args = parser.parse_args()

prjfile=args.project

if os.path.exists(prjfile):
    os.unlink(prjfile)

cfg = json.load(open('build_project.cfg'))
if args.config:
    cfg2 = json.load(open(args.config))
    updates = ['macros','types']
    for k in cfg2:
        if k in updates:
            cfg[k].update(cfg2[k])
        else:
            cfg[k] = cfg2[k]

if args.layers:
    with open(args.layers) as lfile:
        cfg["layers"] = lfile.readlines()

macros = cfg["macros"]
types=cfg["types"]

if args.clean:
    cleancmd = expand_template(cfg.get('commands',{}).get('clean'),macros)
    if cleancmd:
        print "Executing",cleancmd
        subprocess.call(cleancmd, shell=True)

initcmd = expand_template(cfg.get('commands',{}).get('initiallize'),macros)
if initcmd:
    print "Executing",initcmd
    subprocess.call(initcmd,shell=True)

prj = expand_template(cfg["project_template"],macros)

layers=[]
for l in cfg["layers"]:
     l = l.strip()
     if len(l) == 0 or l.startswith('#'):
         continue
     parts = l.split() 
     if len(parts) < 5:
         raise ValueError('Invalid data in layer: '+l)
     (id,cstr,src,ltype)=parts[:4]
     files = parts[4:]
     cls = cstr.replace('/',' ')
     
     if ltype not in types:
         raise ValueError("Invalid type "+ltype+" in layer: "+l)

     typedef = types[ltype]

     for i, f in enumerate(files):
         fid = id
         if len(files) > 1:
             fid += "%02d"%(i+1)
         macros.update( { 'id': fid, 'classes': cls, 'file': f, 'source': src, 'type': ltype })
         prepcmd = typedef.get("prepare", None)
         testfile = expand_template(typedef.get("test", None),macros)
         if prepcmd and (not testfile or not os.path.exists(testfile)):
             prepcmd = expand_template(prepcmd, macros )
             print "Executing:",prepcmd
             subprocess.call(prepcmd, shell=True)
         if testfile and not os.path.exists(testfile):
             raise ValueError("Cannot find or build file "+testfile)

         layer = expand_template(cfg["layer_template"],macros)
         layer.update(expand_template(typedef.get("layer_template",{}),macros))
         layers.append(layer)

layers.reverse()
prj["Layer"] = layers
json.dump(prj,open(prjfile,"w"),indent=4)

      
    
        
   
    
