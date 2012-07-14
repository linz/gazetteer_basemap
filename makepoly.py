#!/usr/bin/python
import sys
import os.path
import os
import ogr
import math
import numpy as np
import logging
import argparse
from collections import namedtuple

# logging.basicConfig(level=logging.INFO)

class Ring( object ):

    class Intersection( object ):

        def __init__(self,no,band,nextpt,dir,xy,used,offset):
            self.no = no
            self.band = band
            self.nextpt = nextpt
            self.dir = dir
            self.xy = xy
            self.used = used
            self.offset = offset

    def __init__( self, pts ):
        self._pts = pts

    def __len__( self ):
        return len(self._pts)

    def __getitem__( self, i ):
        return self._pts[i]

    def split( self, axis, bandsize, bandtol=0.25, npttol=1000 ):
        pts = self._pts

        axis = 1 if axis else 0
        axis2 = 1-axis
        imax = len(pts)-1
        vals = pts[:,axis]
        vmin = np.amin(vals)
        vmax = np.amax(vals)
        logging.info("Range: %f %f",vmax,vmin)
        if vmax-vmin < bandsize:
            yield self
            return
        nband = math.ceil((vmax-vmin)/bandsize)
        logging.info("Bands: %d",nband)
        vorigin = (vmin+vmax)/2.0-(bandsize*nband)/2.0
        bands = np.floor(((vals-vorigin)/bandsize)).astype(int)

        if logging.root.isEnabledFor(logging.INFO):
            logging.info("Ring points (no,band,x,y)")
            for i in range(len(pts)):
                logging.info( "%d %d %f %f",i,bands[i],pts[i][0],pts[i][1])

        # Find all intersections of the edge with the band limits
        # The intersection band lies on the boundary between band-1 and band
        # nextpt is the next point on the boundary following the intersection
        # dir is the direction to the next point (+1 => next band is band, -1=next band is band)
        # xy is the intersection point
        # used are two booleans defining whether the intersection has been used in 
        # forming the final polygons (used[0] = used in polygon from previous node, 
        # used[1] = used in polygon to next node).

        Intersection = Ring.Intersection
        nint = 0
        intlist = []
        for i in range(len(bands)-1):
            if bands[i] == bands[i+1]:
                continue
            b0 = bands[i]
            b1 = bands[i+1]
            step = 1 if b1 > b0 else -1
            offset = 1 if b1  > b0 else 0
            for b in range(b0+offset,b1+offset,step):
                v = vorigin+bandsize*b
                xy = (pts[i]*(pts[i+1,axis]-v)+pts[i+1]*(v-pts[i,axis]))/(pts[i+1,axis]-pts[i,axis])
                nextpt = i+1
                if nextpt == imax:
                    nextpt = 0
                its = Intersection(nint,b,nextpt,step,xy,[False,False],bandsize+1)
                intlist.append(its)
                nint += 1

        # Form the list of intersections on each band boundary

        intersections={}
        for its in intlist:
            b=its.band
            if b not in intersections:
                intersections[b] = []
            intersections[b].append(its)
        logging.info("Intersections")
        for b in intersections:
            intersections[b].sort(key=lambda x: x.xy[axis2])
            if logging.root.isEnabledFor(logging.INFO):
                logging.info("Band %d: %d intersections",b,len(intersections[b]))
                for its in intersections[b]:
                    logging.info("   %s",str(its))
            

        # Allow minor incursions from one band into the next to avoid pointless
        # small geometries

        if bandtol >= 1.0:
            bandtol = 0.0
        tol = bandtol*bandsize
        if tol > 0.0 and npttol > 0:
            # Calculate the tolerance for potential moved segments
            for i in range(-1,len(intlist)-1):
                offset = bandsize+1
                its0 = intlist[i]
                its1 = intlist[i+1]
                if its0.dir == its1.dir:
                    continue
                # If the join between the two sections is not on land then 
                # it can't be cut out
                blist = intersections[its0.band]
                ib0=blist.index(its0)
                ib1=blist.index(its1)
                if ib0/2 != ib1/2:
                    continue

                npt = its1.nextpt-its0.nextpt
                if npt < 0:
                    npt += imax
                if npt <= npttol:
                    if its0.nextpt < its1.nextpt:
                        offset = np.amax((vals[its0.nextpt:its1.nextpt]-its0.xy[axis])*its0.dir)
                    else:
                        offset = max(
                            np.amax((vals[its0.nextpt:]-its0.xy[axis])*its0.dir),
                            np.amax((vals[:its1.nextpt]-its0.xy[axis])*its0.dir)
                            if its1.nextpt > 0 else 0.0
                            )
                its0.offset=offset

            # Now find sections that can be amalgamated into adjacent bands

            while True:
                imin = None
                minoffset = tol
                for i in range(-1,len(intlist)-1):
                    if intlist[i].offset < minoffset:
                        imin=i
                        minoffset = intlist[i].offset
                if imin == None:
                    break
                its0 = intlist[imin]
                npt0 = its0.nextpt
                its1 = intlist[imin+1]
                npt1 = its1.nextpt
                aband = its0.band-1 if its0.dir > 0 else its0.band
                if npt0 < npt1:
                    bands[npt0:npt1]=aband
                else:
                    bands[npt0:]=aband
                    bands[:npt1]=aband
                # If have amalagamated into single ring, then just return self
                if len(intlist) <= 2:
                    yield self
                    return
                # Otherwise need to remove these entries from the list
                logging.info("Amalgamating from %s",str(its0))
                logging.info("Amalgamating to %s",str(its1))
                intlist.remove(its0)
                intlist.remove(its1)
                blist = intersections[its0.band]
                blist.remove(its0)
                blist.remove(its1)
                itsp = intlist[imin-1]
                ip0 = intlist.index(itsp)
                offset = max(itsp.offset,its1.offset)
                if offset < bandsize:
                    ip1 = 0 if ip0 == len(intlist)-1 else ip0+1
                    npt = intlist[ip1].nextpt - itsp.nextpt
                    if npt < 0:
                        npt += imax
                    if npt > npttol:
                        offset = bandsize+1
                itsp.offset=offset

            if logging.root.isEnabledFor(logging.INFO):
                logging.info("Ring points (no,band,x,y)")
                for i in range(len(pts)):
                    logging.info( "%d %d %f %f",i,bands[i],pts[i][0],pts[i][1])

        # Dump all the rings formed by this splitting.  Set bands to -1 as each point is used.

        # Form an array to track which elements are used
        used = bands < 0
        for i0 in range(imax):
            if used[i0]:
                continue
            logging.info("Starting split ring at node %d",i0)
            # Starting point found
            ringpts = [pts[i0]]
            band = bands[i0]
            i1 = i0
            while True:
                i1 += 1
                if i1 == imax:
                    i1 = 0
                band1 = bands[i1]
                # Jumping to new band .. need to get back to correct band
                # Can use intersections for band if band1 > band, or band-1 if band1 < band
                if band1 != band:
                    iband = band+1 if band1 > band else band
                    itslist = intersections[iband]
                    for ii in range(len(itslist)):
                        if itslist[ii].nextpt == i1:

                            its1 = itslist[ii]
                            logging.info("Entering intersection %d",its1.no)
                            assert not its1.used[0],"Re-entering intersection %d" % (its1.no,)
                            ringpts.append(its1.xy)
                            its1.used[0] = True

                            iinext = ii + 1 if ii % 2 == 0 else ii-1
                            its2 = itslist[iinext]
                            logging.info( "Leaving intersection %d",its2.no)
                            assert not its2.used[1],"Re-exiting intersection %d" % (its2.no,)
                            ringpts.append(its2.xy)
                            its2.used[1] = True
                            # Set nextpt-1 so that will reuse
                            i1 = its2.nextpt-1
                            break
                    continue
                logging.info("Adding node %d",i1)
                assert not used[i1], "Re-using node %d" % (i1,)
                ringpts.append(pts[i1])
                used[i1] = True
                if i1 == i0:
                    break
            yield Ring(np.array(ringpts))

        # Now look for rings with no existing nodes... these can only be simple
        # quadrilaterals...

        for its0 in intlist:
            if its0.used[0]:
                continue
            logging.info("Forming internal ring based on intersection %d",its0.no)
            i0 = intersections[its0.band].index(its0)
            i1 = i0+1 if i0%2 == 0 else i0-1
            its1 = intersections[its0.band][i1]
            itsband = intersections[its1.band + its1.dir]
            its2 = None
            its3 = None
            for i2 in range(len(itsband)):
                if itsband[i2].nextpt == its1.nextpt:
                    its2 = itsband[i2]
                    i3 = i2+1 if i2 % 2 == 0 else i2-1
                    its3 = itsband[i3]
                    break
            assert its2 != None,"Cannot form intersections ring following %d %d" % (its0.no,its1.no)
            logging.info("Adding intersections %d %d %d",its1.no,its2.no,its3.no)
            assert its3.nextpt == its0.nextpt,"Intersections ring next point error %d to %d" % (its3.no,its0.no)
            assert not (its1.used[1] or its2.used[0] or its3.used[1]),"Intersections ring reusing intersection %d %d %d" % (its1.no,its2.no,its3.no)
            yield Ring(np.array([its0.xy,its1.xy,its2.xy,its3.xy,its0.xy]))

class LineSet( object ):

    class End( object ):

        def __init__( self, lineid, forward, line  ):
            self.lineid = lineid
            self.forward = forward
            self.xy = line[0] if forward else line[-1]
            self.otherEnd = None
            self.nearest=None

        def __str__( self, showlink=True ):
            nrstr=''
            if showlink and self.nearest:
                nrstr=self.nearest.__str__(False)
            return "%d %s (%.2f,%.2f)%s" % (self.lineid,self.forward,self.xy[0],self.xy[1],nrstr)

    def __init__( self ):
        self._lines = []
        self._ends = None

    def __len__( self ):
        return len( self._lines )

    def append( self, line ):
        self._lines.append( line )
        self._ends = None

    def ends( self, tolerance ):
        if self._ends:
            return self._ends
        # Form a list of ends
        endlist=[]
        for id, line in enumerate(self._lines):
            end1 = LineSet.End(id,True,line)
            end2 = LineSet.End(id,False,line)
            end1.otherEnd = end2
            end2.otherEnd = end1
            endlist.extend((end1, end2))

        # Sort in one direction
        endlist.sort(key=lambda end:end.xy[0])

        # Find a next endpoint within a tolerance 
        tol2 = tolerance*tolerance
        for i,end in enumerate(endlist):
            if end.nearest:
                continue
            xmax = end.xy[0]+tolerance
            nearest = None
            ndist = tol2
            for end2 in endlist[i+1:]:
                if end2.xy[0] > xmax:
                    break
                dist = np.sum(np.square(end.xy-end2.xy))
                if dist <= ndist:
                    ndist = dist
                    nearest = end2
                    xmax = end.xy[0] + math.sqrt(dist)
            if nearest:
                if nearest.nearest:
                    raise ValueError('Lines don\'t form simple rings (error at %f %f)'%(end.xy[0],end.xy[1]))
                nearest.nearest=end
                end.nearest=nearest
            else:
                raise ValueError('Lines don''t join at %f %f)'%(end.xy[0],end.xy[1]))


        self._ends = endlist
        return endlist

    def formRings( self, tolerance ):
        rings = []
        usedlines=[]
        for start in self.ends(tolerance):
            if not start.forward or start.lineid in usedlines:
                continue
            ring = [start]
            usedlines.append(start.lineid)
            while True:
                next = ring[-1].otherEnd.nearest
                if not next:
                    raise ValueError( "Topology error - no connection at (%f,%f)" % (ring[-1].xy[0],ring[-1].xy[1]))
                if next == start:
                    rings.append(ring)
                    break
                if next.lineid in usedlines:
                    raise ValueError( "Topology error :-(")
                usedlines.append(next.lineid)
                ring.append(next)
        return rings

    def buildRing( self, ends ):
        npt = sum((self._lines[x.lineid].shape[0] for x in ends))
        npt -= len(ends)-1
        ring = np.empty((npt,2))
        npt = 0
        start=0
        for r in ends:
            l = self._lines[r.lineid]
            if not r.forward:
                l=l[::-1]
            l=l[start:]
            start = 1
            npt1 = npt+l.shape[0]
            ring[npt:npt1] = l
            npt = npt1
        return Ring(ring)

####################################################

parser = argparse.ArgumentParser(description="Compile linestrings forming ring in shapefile into polygons\n"+
        "Polygons may be split into tiles.")

parser.add_argument('input_file',type=str,help="Input shape file")
parser.add_argument('output_file',type=str,help="Output shape file")
parser.add_argument('-s','--tilesize',type=float,help='Size of tile to divide into',default=100000.0)
parser.add_argument('-t','--tolerance',type=float,help='Endpoint tolerance forming rings',default=0.1)
parser.add_argument('-w','--where',type=str,help='Condition (field=value) used to select line strings')
args=parser.parse_args()

infile = args.input_file
outfile = args.output_file

f = ogr.Open(infile)
if f == None:
    print "Cannot open input file",infile
    sys.exit()
layer = f.GetLayer(0)

cfield=None
cvalue=None
if args.where:
    cfield,cvalue=args.where.split('=',2)

lines = LineSet()
nptt=0
while True:
    feat = layer.GetNextFeature()
    if not feat:
        break
    if cfield:
        value=feat.GetFieldAsString(cfield)
        if value != cvalue:
            continue
    geom = feat.GetGeometryRef()
    if geom.GetGeometryType() != ogr.wkbLineString:
        raise ValueError('Geometries must be line strings')
    npt = geom.GetPointCount()
    ls = np.empty((npt,2))
    for i in range(npt):
        ls[i,0]=geom.GetX(i)
        ls[i,1]=geom.GetY(i)
    lines.append(ls)
    nptt+=npt
    # print "Line with",npt,"points"
    #print ls
print len(lines),'strings'
print nptt,'points'

rings = lines.formRings(args.tolerance)
print len(rings)," rings found"

if not rings:
    print "No output generated"

if os.path.exists(outfile):
    os.unlink(outfile)

drv = f.GetDriver()
outf = drv.CreateDataSource(outfile)
if outf == None:
    print "Cannot open output file",outfile

outl = outf.CreateLayer(os.path.basename(outfile),layer.GetSpatialRef(),ogr.wkbPolygon)
defn = outl.GetLayerDefn()


tilesize=args.tilesize
npoly = 0

for r in rings:
    ring = lines.buildRing(r)
    for band in ring.split(1,tilesize):
        for tile in band.split(0,tilesize):
            geom = ogr.Geometry(ogr.wkbPolygon)
            gring = ogr.Geometry(ogr.wkbLinearRing)
            for i in range(len(tile)):
                gring.AddPoint(tile[i][0],tile[i][1])
            geom.AddGeometryDirectly(gring)
            feat = ogr.Feature(defn)
            feat.SetGeometry(geom)
            outl.CreateFeature(feat)
            feat.Destroy()
            npoly += 1

print npoly,"polygons created"
