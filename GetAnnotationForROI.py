from cytomine import Cytomine
import shapely
import openslide
import scipy.misc as misc
from shapely.affinity import affine_transform

if __name__ == "__main__":

    Pk = 'cbfe0e04-3fd7-4a7f-a13c-b86685ecb570'
    Prk = 'XXXXXX'
    Url = 'demo.cytomine.be'

    cytomine_server = Cytomine(Url,Pk,Prk)

    AnnotationFix = cytomine_server.get_annotation(19713157)
    #AnnotationMoving = cytomine_server.get_annotations(15548182, id_image=15857650,showWKT=True)
    SlideFix = openslide.OpenSlide('/home/tvessiere/Pictures/fixtissu.ndpi')
    #SlideMov = openslide.OpenSlide('/home/tvessiere/Pictures/movingitssu.ndpi')

    HeightFix = SlideFix.dimensions[1]
    #HeightMov = SlideMov.dimensions[1]

    PolyFix = shapely.wkt.loads(AnnotationFix.location)
    PolyFix = affine_transform(PolyFix, [1, 0, 0, -1, 0, HeightFix])
    FixBounds = PolyFix.bounds
    LocationOffsetFix = (int(FixBounds[0]),int(FixBounds[1]))
    print  LocationOffsetFix
    WidthAndHeightFix = (int(FixBounds[3] - FixBounds[1]), int(FixBounds[2] - FixBounds[0]))
    print WidthAndHeightFix

   # for annots in AnnotationMoving:
    #    PolyMov = shapely.wkt.loads(annots.location)
     #   MovBounds = PolyMov.bounds
      #  LocationOffsetMov = (int(MovBounds[0]),int(HeightMov - MovBounds[1]))
       # WidthAndHeightMov = (int(MovBounds[3] - MovBounds[1]), int(MovBounds[2] - MovBounds[0]))
        #if(WidthAndHeightMov[0] > 10000.0):
         #   print WidthAndHeightMov



    CropFix = SlideFix.read_region(LocationOffsetFix,0,WidthAndHeightFix)
    #misc.imsave('testcropfix.tif', CropFix)
    #SlideMov.read_region(LocationOffsetMov,1,WithAndHeightMov)
