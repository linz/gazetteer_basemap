#!/usr/bin/python
'''

This script prepares the data and project files for a tilemill project.

It uses a JSON formatted configuration file which contains the following components:

cfg.macros:  String substitutions used in the project
cfg.commands.initiallize:  Shell commands run to initiallize the project
cfg.commands.clean:   Shell commands run if the --clean option is specified
cfg.types: A list of types of file (each different type is prepared in a different way and may have
     a different layer template used to install it into the project.mml file)
    cfg.types[i].testfile:  The name of a file that can be used to see if the data is already prepared
    cfg.types[i].prepare:  Shell script run to prepare the data file (s)
    cfg.types[i].layer_template:  Any entries here override the default layers template
cfg.project_template: Project file template
cfg.layer_template: Template for each layer in the project file

An additional configuration file can be specified which can replace or add cfg.macros and cfg.types
items and replace any other item completely.

The template uses a simple string substitution to encode options.  When expanding strings and templates
the value {xxx} is replaced with the macro for xxx from the cfg.macros dictionary.  This happens
recursively.  In addition to the macros, it can also use the id, classes, source, type, and file 
values from each layer as it is processed.  The macro can also define values that will be used when it is 
expanded using {xxx:str1=replacemnt1:str2=replacement2}

The layers.cfg file is a simple text file.  Each uncommented line contains:

id       The id for the layer. If the layer has more than one file then 01, 02, .. is appended to this.
classes  A list of classes to use for the layer in the project file. Classes are separated with a "/"
source   The source for the data (eg topo50, topo500).  This may be used in macros to locate and name the
         file
type     The type of the file, defining which cfg.type method is used to prepare it and add it to the
         project file.  The type can include ":param=value:param=value..."
file..   A space separated list of file names.  Each will be processed in turn.  This is not the actual
         name of the file, but a base name used in the project configuration macros to prepare and 
         install the file.

The layers should be ordered from the bottomost on the basemap to the topmost (ie lowest layers first)

'''
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
    if max <= 0:
        return string
    pdict = {}
    if type(params) == dict:
        pdict = params
    elif type(params) in (str, unicode) and params != '':
        for ds in params.split(':'):
            m = re.match(r"(\w+)\=(.*)",ds)
            if m:
                pdict[m.group(1)]=m.group(2)
    rdict = {}
    for k in pdict:
        rdict[k] = macros.get(k)
        macros[k] = pdict[k]

    string=re.sub(r"\{(\w+)((?:\:\w+\=[^:{}]*))*\}",
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
parser.add_argument('-l','--layers',help='File of layers (overriding configuration)',default='layers.cfg')
parser.add_argument('--clean',action='store_true', help='Clear filecache before starting')
parser.add_argument('--dry-run',action='store_true', help='Dry run - don\'t build data files')
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
        if args.dry_run:
            print "Executing:",cleancmd
        else:
            subprocess.call(cleancmd, shell=True)

initcmd = expand_template(cfg.get('commands',{}).get('initiallize'),macros)
if initcmd:
    if args.dry_run:
        print "Executing:",initcmd
    else:
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
     
     lmacros={}
     if ':' in ltype:
         parts = ltype.split(':')
         for p in parts[1:]:
             if '=' not in p:
                 raise ValueError("Invalid definition of type parameters in "+ltype)
             (k,v) = p.split('=',1)
             lmacros[k] = v
         ltype=parts[0]

     if ltype not in types:
         raise ValueError("Invalid type "+ltype+" in layer: "+l)

     typedef = types[ltype]
     fmacros = macros.copy()
     fmacros.update( { 'id': id, 'classes': cls, 'source': src, 'type': ltype })
     fmacros.update( lmacros )

     for i, f in enumerate(files):
         fmacros['file'] = f
         if len(files) > 1:
             fmacros['id'] = id+"%02d"%(i+1)
         prepcmd = typedef.get("prepare", None)
         testfile = expand_template(typedef.get("testfile", None),fmacros)
         if prepcmd and (not testfile or not os.path.exists(testfile)):
             prepcmd = expand_template(prepcmd, fmacros )
             print "Executing:",prepcmd
             if not args.dry_run:
                 subprocess.call(prepcmd, shell=True)
         if not args.dry_run and testfile and not os.path.exists(testfile):
             raise ValueError("Cannot find or build file "+testfile)

         layer = expand_template(cfg["layer_template"],fmacros)
         layer.update(expand_template(typedef.get("layer_template",{}),fmacros))
         layers.append(layer)

# layers.reverse()
prj["Layer"] = layers
json.dump(prj,open(prjfile,"w"),indent=4)

      
    
        
   
    
