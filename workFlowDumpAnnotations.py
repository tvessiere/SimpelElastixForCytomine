__author__ = "Vessiere Thomas <vessiere.thomas@hotmail.com>"
__Copyright__ = "Copyright 2010-2017 University of Liège, Belgium, http://www.cytomine.be/"


from argparse import ArgumentParser
import SimpleITK as sitk
from cytomine import Cytomine
from cytomine.models import *
import scipy.misc as misc
import numpy as np
import os

Pk = 'cbfe0e04-3fd7-4a7f-a13c-b86685ecb570'
Prk = 'XXX'
urlCore = 'demo.cytomine.be'
urlUploadDemo = "demo-upload.cytomine.be"
workingPath = "/home/tvessiere/data/Project/TestProcessing/DumpAnnots/Images/"


def main(argv):

    # parsing arguments
    parser = ArgumentParser(prog="TestParser", description="Catch arguments form exec cmd")

    parser.add_argument('--cytomine_host', dest="cytomine_host", default='demo.cytomine.be')
    parser.add_argument('--cytomine_public_key', dest="cytomine_public_key")
    parser.add_argument('--cytomine_private_key', dest="cytomine_private_key")
    parser.add_argument('--cytomine_id_software', dest="cytomine_id_software", type=int)
    parser.add_argument("--cytomine_id_project", dest="cytomine_id_project", type=int)
    parser.add_argument('--id_fix_image', dest="id_fix_image", type=int)
    parser.add_argument("--id_mov_image", dest="id_mov_image", type=int)
    parser.add_argument('--nb_iterations', dest="nb_iterations", type=int)
    parser.add_argument("--nb_spatialsampels", dest="nb_spatialsampels", type=int)
    arguments, others = parser.parse_known_args(argv)

    # set var
    fixImageId = arguments.id_fix_image
    movImageId = arguments.id_mov_image
    projectId = arguments.cytomine_id_project

    # connection
    conn = Cytomine(urlCore, Pk, Prk, working_path=workingPath)


    # dump images in folder working path + images, for reach iamges : working path + images + id project -> u are in the right folder
    annotationFix = conn.get_annotations(projectId, id_image=fixImageId)
    fixData = annotationFix.data()
    excludedTerms = []
    IdTerm = 0
    for a in fixData:
        i = 0
        term = conn.get_term(int(a.term[i]))
        if term.name != 'ROI':
            excludedTerms[i] = a.term[i]
        else:
            IdTerm = a.term[i]
        i += 1
        conn.dump_annotations(annotations=annotationFix,
                                    get_image_url_func=Annotation.get_annotation_crop_url,
                                    dest_path=workingPath + "/imagefix/",
                                    excluded_terms=excludedTerms,
                                    desired_zoom=0
                                    )

    annotationMov = conn.get_annotations(projectId, id_image=movImageId)
    movData = annotationMov.data()
    excludedTerms = []

    for b in movData:
        i = 0
        term = conn.get_term(int(a.term[i]))
        if term.name != 'ROI':
            excludedTerms[i] = a.term[i]
        else:
            IdTerm = a.term[i]
        i += 1

    dump_annotations = conn.dump_annotations(annotations=annotationMov,
                                                       get_image_url_func=Annotation.get_annotation_crop_url,
                                                       dest_path=workingPath + "/imagemov/",
                                                       desired_zoom=excludedTerms,
                                                       excluded_terms=excludedTerms
                                                       )

    listFix= os.listdir(workingPath + "imagefix" + "/" + str(IdTerm) + "/")
    listMov = os.listdir(workingPath + "imagemov" + "/" + str(IdTerm) + "/")

    fixImage = sitk.ReadImage(workingPath + "imagefix" + "/" + str(IdTerm) + "/" + listFix[0],sitk.sitkFloat32)
    movImage = sitk.ReadImage(workingPath + "imagemov" + "/" + str(IdTerm) + "/" + listMov[0],sitk.sitkFloat32)

    simpleElastix = sitk.SimpleElastix()
    simpleElastix.SetFixedImage(fixImage)
    simpleElastix.SetMovingImage(movImage)
    parameterMapTranslation = sitk.GetDefaultParameterMap("translation")
    parameterMapAffine = sitk.GetDefaultParameterMap("affine")

    simpleElastix.SetParameterMap(parameterMapTranslation)
    simpleElastix.AddParameterMap(parameterMapAffine)

    simpleElastix.SetParameter("MaximumNumberOfIterations", str(arguments.nb_iterations))
    simpleElastix.SetParameter("NumberOfSpatialSamples",str(arguments.nb_spatialsampels))

    simpleElastix.Execute()

    img = simpleElastix.GetResultImage()
    np_img = sitk.GetArrayFromImage(img)
    img_to_save = np.zeros((np_img.shape[0], np_img.shape[1], 3))
    img_to_save[:, :, 1] = np_img
    img_to_save[:, :, 2] = sitk.GetArrayFromImage(fixImage)
    misc.imsave("/home/tvessiere/data/Project/TestProcessing/images/result_translationaffine.png", img_to_save)
    misc.imsave("/home/tvessiere/data/Project/TestProcessing/images/movimage.png",np_img)

    storageId = 19676833
    demoUpload = Cytomine(urlUploadDemo, Pk, Prk, verbose=True)
    sync = False

    storage = conn.get_storage(storageId)
    assert storage.id == storageId

    demoUpload.upload_image("/home/tvessiere/data/Project/TestProcessing/images/result_translationaffine.png",projectId, storageId, "http://demo.cytomine.be")

    os.system("rm -rf " + workingPath + "imagefix" + "/" + str(IdTerm) + "/")
    os.system("rm -rf " + workingPath + "imagemov" + "/" + str(IdTerm) + "/")

    # /home/tvessiere/data/miniconda2/envs/cytomine/bin/python FirstWorkFlow.py --cytomine_host demo.cytomine.be --cytomine_id_project 19941904  --id_fix_image 19942095 --id_mov_image 19942069 --nb_iterations 6000 --nb_spatialsampels 6000


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])

