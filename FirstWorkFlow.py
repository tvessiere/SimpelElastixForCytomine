from argparse import ArgumentParser
import SimpleITK as sitk
from cytomine import Cytomine
import scipy.misc as misc
import numpy as np
import os

Pk = 'cbfe0e04-3fd7-4a7f-a13c-b86685ecb570'
Prk = 'XXXXXX'
Url = 'demo.cytomine.be'


workingPath = "/home/tvessiere/data/Project/TestProcessing"



def main(argv):

    #parsing arguemnts
    parser = ArgumentParser(prog="TestParser", description="Catch argment form exec cmd")

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

    #set var
    fixImageId = arguments.id_fix_image
    movImageId = arguments.id_mov_image
    idProject = arguments.cytomine_id_project


    #connection
    conn = Cytomine(Url,Pk,Prk,working_path=workingPath)

    #dump images in folder working path + images, for reach iamges : working path + images + id project -> u are in the right folder
    conn.dump_project_images(id_project=idProject,dest_path="/images/",override=True,max_size=True)

    """fixImage = sitk.ReadImage(workingPath + "/images/" + str(idProject) + "/" + str(fixImageId)+ ".jpg",sitk.sitkFloat32)
    movImage = sitk.ReadImage(workingPath + "/images/" + str(idProject) + "/" + str(movImageId) +".jpg",sitk.sitkFloat32)

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
    misc.imsave("/home/tvessiere/data/Project/TestProcessing/images/movimage.png",np_img)"""

    storageObj = conn.get_storage(19676833)
    ims_conn = Cytomine("demo-ims.cytomine.be", Pk, Prk, verbose=False)
    response = ims_conn.upload_image(filename="/home/tvessiere/data/Project/TestProcessing/images/result_translationaffine.png",project=idProject,storage=storageObj,cytomine_host="demo.cytomine.be",sync=False,properties=None)
    #conn.upload_image("/home/tvessiere/data/Project/TestProcessing/images/result_translationaffine.png",project=idProject,storage=storage,cytomine_host="demo-ims.cytomine.be")
    #conn.upload_image("/home/tvessiere/data/Project/TestProcessing/images/movimage.png", idProject, 19676833, conn,"demo-ims.cytomine.be")

    #os.remove("/home/tvessiere/data/Project/TestProcessing/images/")

    #/home/tvessiere/data/miniconda2/envs/cytomine/bin/python FirstWorkFlow.py --cytomine_host demo.cytomine.be --cytomine_public_key --cytomine_id_project 19941904  --id_fix_image 19942095 --id_mov_image 19942069 --nb_iterations 6000 --nb_spatialsampels 6000
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

