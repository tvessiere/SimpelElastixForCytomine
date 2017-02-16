from cytomine import Cytomine
from cytomine.models import *

if __name__ == "__main__":

    Pk = 'cbfe0e04-3fd7-4a7f-a13c-b86685ecb570'
    Prk = 'XXXXXXX'
    Url = 'demo.cytomine.be'
    output_dir = "/home/tvessiere/data/Project/getannotationstissu"

    cytomine_server = Cytomine(Url,Pk,Prk)

    AnnotationFix = cytomine_server.get_annotations(15548182,id_image=15857817)

    annotation_get_func = Annotation.get_annotation_crop_url
    print annotation_get_func

    dump_annotations = cytomine_server.dump_annotations(annotations=AnnotationFix,
                                             get_image_url_func=annotation_get_func,
                                             dest_path=output_dir,
                                             desired_zoom=4)

    AnnotationMov = cytomine_server.get_annotations(15548182, id_image=15857650)

    annotation_get_func = Annotation.get_annotation_crop_url
    print annotation_get_func

    dump_annotations = cytomine_server.dump_annotations(annotations=AnnotationMov,
                                                        get_image_url_func=annotation_get_func,
                                                        dest_path=output_dir,
                                                        desired_zoom=4)


