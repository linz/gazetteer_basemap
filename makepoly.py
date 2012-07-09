import sys
import os.path
import os
import ogr
import math
import numpy as np
import logging
from collections import namedtuple

#logging.basicConfig(level=logging.INFO)

class Ring( object ):

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

        nint = 0
        Intersection=namedtuple('Intersection','no band nextpt dir xy used offset')
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
                if its0.dir != its1.dir:
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
                    intlist[i] = its0._replace(offset=offset)

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
                intlist[ip0] = itsp._replace(offset=offset)

            if logging.root.isEnabledFor(logging.INFO):
                logging.info("Ring points (no,band,x,y)")
                for i in range(len(pts)):
                    logging.info( "%d %d %f %f",i,bands[i],pts[i][0],pts[i][1])

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

class LineSet( list ):

    class End(namedtuple('End','no start')):

        def otherEnd( self ):
            return LineSet.End( self.no, not self.start )


    def endpt( self, end ):
        line = self[end.no]
        pt = line[0] if end.start else line[-1]
        return pt

    def nearestEnd( self, end ):
        pt = self.endpt(end)
        nearest = None
        minoffset = 0
        for i in range(len(self)):
            for terminal in (True,False):
                testend = LineSet.End(i,terminal)
                if testend == end:
                    continue
                testpt = self.endpt(testend)
                offset = np.sum(np.square(pt-testpt))
                if nearest == None or offset < minoffset:
                    minoffset = offset
                    nearest=testend
        return nearest, minoffset

    def formRings( self, tolerance ):
        rings = []
        usedlines=[]
        for i in range(len(self)):
            if i in usedlines:
                continue
            start = LineSet.End(i,True)
            ring = [start]
            usedlines.append(i)
            while True:
                next, offset = self.nearestEnd( ring[-1].otherEnd() )
                if offset > tolerance:
                    raise ValueError("Lines do not form a ring")
                if next == start:
                    rings.append(ring)
                    break
                if next.no in usedlines:
                    raise ValueError( "Topology error :-(")
                usedlines.append(next.no)
                ring.append(next)
        return rings

    def buildRing( self, ends ):
        npt = sum((self[x.no].shape[0] for x in ends))
        npt -= len(ends)-1
        ring = np.empty((npt,2))
        npt = 0
        start=0
        for r in ends:
            l = self[r.no]
            if not r.start:
                l=l[::-1]
            l=l[start:]
            start = 1
            npt1 = npt+l.shape[0]
            ring[npt:npt1] = l
            npt = npt1
        return Ring(ring)

if len(sys.argv) != 3:
    print "Require input and output shape files"
    sys.exit()

infile = sys.argv[1]
outfile = sys.argv[2]

f = ogr.Open(infile)
if f == None:
    print "Cannot open input file",infile
    sys.exit()
layer = f.GetLayer(0)

lines = LineSet()
nptt=0
while True:
    feat = layer.GetNextFeature()
    if not feat:
        break
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

rings = lines.formRings(0.0000001)
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


tilesize=100000
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
