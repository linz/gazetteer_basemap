#!/usr/bin/python
# Copyright 2012 Crown copyright (c)
#  Land Information New Zealand and the New Zealand Government.
#  All rights reserved
# 
#  This program is released under the terms of the new BSD license. See 
#  the LICENSE file for more information.

'''
Joins polygons from the topo data set that have been split on map cuts.

Assumes 
1) any polygon edge (internal or external) that runs E-W or N-S is a potential map cut
2) any polygons sharing a potential map cut are to be joined.

Uses two tolerances in matching edges:
    normal_tolerance is the tolerance normal to the map cut
    parallel_tolerance is the tolerance parallel to the map cut
Two edges are assumed to be the same if their endpoint coordinates match to within both
tolerances.
'''

import sys
import os.path
import os
import ogr
import math
import numpy as np
import logging
import argparse
from collections import namedtuple

#logging.basicConfig(level=logging.INFO)

class mapedge(namedtuple('mapedge','id axis vx vy0 vy1')):

    def __str__( self ):
        if self.axis==0:
            return str(self.id)+';LINESTRING('+str(self.vx)+' '+str(self.vy0)+','+str(self.vx)+' '+str(self.vy1)+')'
        else:
            return str(self.id)+';LINESTRING('+str(self.vy0)+' '+str(self.vx)+','+str(self.vy1)+' '+str(self.vx)+')'

parser=argparse.ArgumentParser('Rejoin polygons broken on map cuts in a shapfile')
parser.add_argument('input_file',type=str,help="Input shape file name")
parser.add_argument('output_file',type=str,help="Output shape file name")
parser.add_argument('-n', '--normal_tolerance',type=float,default=0.1,help="Cross sheet boundary tolerance")
parser.add_argument('-p', '--parallel_tolerance',type=float,default=0.1,help="Along sheet boundary tolerance")
parser.add_argument('-r', '--map_',type=float,default=0.1,help="Along sheet boundary tolerance")
parser.add_argument('-d', '--debug',action='store_true',help="Generate debug output")

args = parser.parse_args()

infile = args.input_file
outfile = args.output_file
ntolerance = args.normal_tolerance
ptolerance = args.parallel_tolerance
debug = args.debug

f = ogr.Open(infile)
if f == None:
    print "Cannot open input file",infile
    sys.exit()
layer = f.GetLayer(0)

nptt=0
id=0

xedges = []
yedges = []

print "Reading",infile
if debug:
    print "EDGE;TYPE;ID;WKT"
while True:
    feat = layer.GetNextFeature()
    if not feat:
        break
    poly = feat.GetGeometryRef()
    if poly.GetGeometryType() != ogr.wkbPolygon:
        raise ValueError('Geometries must be polygons')
    for geom in (poly.GetGeometryRef(i) for i in range(poly.GetGeometryCount())):
        npt = geom.GetPointCount()
        if npt == 0:
            raise ValueError("not a ring")
        nptt += npt
        x0 = geom.GetX(0)
        y0 = geom.GetY(0)
        for i in range(1,npt):
            x1 = geom.GetX(i)
            y1 = geom.GetY(i)
            if abs(x0-x1) < ntolerance:
                edge=mapedge(id,0,x0,min(y0,y1),max(y0,y1))
                xedges.append(edge)
                if debug:
                    print 'EDGE;X;'+str(edge)
            if abs(y0-y1) < ntolerance:
                edge=mapedge(id,1,y0,min(x0,x1),max(x0,x1))
                yedges.append(edge)
                if debug:
                    print 'EDGE;Y;'+str(edge)
            x0 = x1
            y0 = y1
    id+=1
    # print "Line with",npt,"points"
    #print ls
print id,'polygons'
print nptt,'points'
print len(xedges),'possible x edges'
print len(yedges),'possible y edges'

print "Sorting possible matched edges"
xedges.sort(key=lambda edge: edge.vy0)
yedges.sort(key=lambda edge: edge.vy0)

print "Identifying common edges"
mergeid=np.arange(id)
nmerging=0

for edges in xedges, yedges:
    nedge = len(edges)
    for i1 in range(nedge):
        e1 = edges[i1]
        #if i1 % 1000 == 0:
        #    print i1,"tested - merging",nmerging
        vymax = e1.vy0+ptolerance
        i2 = i1+1
        while i2 < nedge:
            e2 = edges[i2]
            i2 += 1
            if e2.vy0 > vymax:
                break
            if abs(e1.vy1-e2.vy1) > ptolerance:
                continue
            if abs(e1.vx-e2.vx) > ntolerance:
                continue
            id1=e1.id
            id2=e2.id
            if id1 == id2:
                continue
            if debug:
                print "Merging",id1,id2
                print 'EDGE;J;'+str(e1)
            nmerging+=1
            end1 = id1
            while mergeid[end1] != end1:
                end1 = mergeid[end1]
            end2 = id2
            while mergeid[end2] != end2:
                end2 = mergeid[end2]
            mid = max(end1,end2)
            for end in id1, id2:
                while True:
                   end1 = mergeid[end]
                   mergeid[end] = mid
                   if end1 == end:
                       break
                   end = end1

changed = True
while changed:
    changed = False
    print "Forming merged sets"
    for id1 in range(id-1,-1,-1):
        id2 = mergeid[id1]
        if id2 == id1:
            continue
        if id2 != mergeid[id2]:
            changed=True
            mid = max(id2,mergeid[id2])
            if debug:
                print "Remerging:",id1,id2,mid
            mergeid[id1] = mid
            mergeid[id2] = mid

if os.path.exists(outfile):
    os.unlink(outfile)

drv = f.GetDriver()
drv = f.GetDriver()
outf = drv.CreateDataSource(outfile)
if outf == None:
    print "Cannot open output file",outfile
    sys.exit()

outl = outf.CreateLayer(os.path.basename(outfile),layer.GetSpatialRef(),ogr.wkbPolygon)
defn = outl.GetLayerDefn()

layer.ResetReading()

ncopied = 0
nmerged = 0
nmerging = 0
geoms={}

print "Copying features"

id = 0
while True:
    feat = layer.GetNextFeature()
    if not feat:
        break
    poly = feat.GetGeometryRef()
    poly = poly.Clone()
    mid = mergeid[id]
    if mid != id:
        nmerging += 1
        if mid not in geoms:
            geoms[mid]=[]
        geoms[mid].append(poly)
    else:
        merged = False
        ncopied += 1
        if id in geoms:
            nmerging += 1
            nmerged += 1
            ncopied -= 1
            glist = geoms[id]
            del geoms[id]
            merged = True
            glist.append(poly)
            # print "Merging",len(glist),"polygons" 
            while len(glist) > 1:
                glist2 = []
                for i in range(0,len(glist)-1,2):
                    glist2.append(glist[i].Union(glist[i+1]))
                if len(glist) % 2 == 1:
                    glist2.append(glist[-1])
                glist = glist2
            poly = glist[0]
            # print "Merged"
        feat = ogr.Feature(defn)
        feat.SetGeometry( poly )
        outl.CreateFeature(feat)
    id+=1

print ncopied,"features copied directly"
print nmerging,"features merged to form",nmerged,"features"
