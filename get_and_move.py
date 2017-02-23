import os
from argparse import ArgumentParser

from cytomine.models import annotation
from sldc import Loggable, Logger, StandardOutputLogger
from cytomine import Cytomine
from cytomine_utilities import CytomineJob
import SimpleITK as sitk
import scipy.misc as misc
import numpy as np
import os

class SimpleElastixJob(CytomineJob, Loggable):

    # set parameters for your algo, 4 first params must be like this #
    def __init__(self, cytomine, software_id, project_id, job_parameters,
                 fix_image_id, moving_image_id, nb_spatial_sampel, nb_iterations, storage_id,
                 id_annotation_fix, id_annotation_moving, working_path, cytomine_host, cytomine_upload, pk, prk):

        # call init from parent classes #
        CytomineJob.__init__(self, cytomine, software_id, project_id, parameters=job_parameters)
        Loggable.__init__(self, logger=StandardOutputLogger(Logger.INFO))

        # keep var from parameters #
        self._fix_image_id = fix_image_id
        self._moving_image_id = moving_image_id
        self._nb_spatial_sampel = nb_spatial_sampel
        self._nb_iterations = nb_iterations
        self._storage_id = storage_id
        self._id_annotation_fix = id_annotation_fix
        self._id_annotation_moving = id_annotation_moving
        self._working_path = working_path
        self._cytomine_upload = cytomine_upload
        self._cytomine_host = cytomine_host
        self._cytomine = cytomine
        self._project_id = project_id
        self._pk = pk
        self._prk = prk

    # run methode, the logic of your algorithm is here #
    # DONT FORGET TO COMPLETE PATH WITH ID_JOB #
    def run(self):

        if not self._id_annotation_fix and not self._id_annotation_fix:
            # dump images #
            self._cytomine.dump_project_images(id_project=self._project_id, dest_path="/images/" , override=True, max_size=True)

            # read images #
            fix_image = sitk.ReadImage(self._working_path + "/images/" + str(self._project_id) + "/" + str(self._fix_image_id) + ".jpg",sitk.sitkFloat32)
            mov_image = sitk.ReadImage(self._working_path + "/images/" + str(self._project_id) + "/" + str(self._fix_image_id) + ".jpg",sitk.sitkFloat32)

            # instanciate and processing with SimpleElastix #
            simple_elastix = sitk.SimpleElastix()
            simple_elastix.SetFixedImage(fix_image)
            simple_elastix.SetMovingImage(mov_image)
            parameterMapTranslation = sitk.GetDefaultParameterMap("translation")
            parameterMapAffine = sitk.GetDefaultParameterMap("affine")

            # 2 params, Translation and affine #
            simple_elastix.SetParameterMap(parameterMapTranslation)
            simple_elastix.AddParameterMap(parameterMapAffine)

            # params set by user #
            simple_elastix.SetParameter("MaximumNumberOfIterations", str(self._nb_iterations))
            simple_elastix.SetParameter("NumberOfSpatialSamples", str(self._nb_spatialsampels))

            # run processing #
            simple_elastix.Execute()

            # get result image and fix image for upload #
            img = simple_elastix.GetResultImage()
            np_img = sitk.GetArrayFromImage(img)
            img_to_save = np.zeros((np_img.shape[0], np_img.shape[1], 3))
            img_to_save[:, :, 1] = np_img
            img_to_save[:, :, 2] = sitk.GetArrayFromImage(fix_image)
            misc.imsave(self._working_path + "/images/" + "result_translationaffine.png" , img_to_save)

            # upload config #
            uploadConn = Cytomine(self._cytomine_upload, self._pk, self._prk, verbose=False)
            sync = False

            # uploading image #
            uploadConn.upload_image(self._working_path + "/images/" +"result_translationaffine.png",
                                    self._project_id, self._storage_id, "http://" + self._cytomine_host)

        else:
            # dump annotations#
            annotation_fix = self._cytomine.get_annotation(self._fix_image_id)
            collection_fix = self._cytomine.AnnotationCollection()
            collection_fix.data().append(annotation_fix)

            self._cytomine.dump_annotations\
                                    (
                                        annotations=collection_fix,
                                        get_image_url_func=self._cytomine.Annotation.get_annotation_crop_url,
                                        dest_path=self._working_path + "/image_fix/",
                                        desired_zoom=0
                                    )

            annotation_moving = self._cytomine.get_annotation(self._id_annotation_moving)
            collection_moving = self._cytomine.AnnotationCollection()
            collection_moving.data().append(annotation_moving)

            self._cytomine.dump_annotations\
                                    (
                                        annotations=collection_moving,
                                        get_image_url_func=self._cytomine.Annotation.get_annotation_crop_url,
                                        dest_path=self._working_path + "/image_mov/",
                                        desired_zoom=0
                                    )

            # get id_term for path #
            id_term = annotation_fix.term[0]

            # because the name of the file is vague, just list the file and get the elem at 0 #
            list_fix = os.listdir(self._working_path + "/image_fix/" + str(id_term) + "/")
            list_moving = os.listdir(self._working_path + "/imag_mov/" + str(id_term) + "/")

            # read images #
            fix_image = sitk.ReadImage(self._working_path + "image_fix" + "/" + str(id_term) + "/" + list_fix[0],   sitk.sitkFloat32)
            mov_image = sitk.ReadImage(self._working_path + "image_mov" + "/" + str(id_term) + "/" + list_moving[0], sitk.sitkFloat32)

            # instanciate and processing with SimpleElastix #
            simple_elastix = sitk.SimpleElastix()
            simple_elastix.SetFixedImage(fix_image)
            simple_elastix.SetMovingImage(mov_image)
            parameterMapTranslation = sitk.GetDefaultParameterMap("translation")
            parameterMapAffine = sitk.GetDefaultParameterMap("affine")

            # 2 params, Translation and affine #
            simple_elastix.SetParameterMap(parameterMapTranslation)
            simple_elastix.AddParameterMap(parameterMapAffine)

            # params set by user #
            simple_elastix.SetParameter("MaximumNumberOfIterations", str(self._nb_iterations))
            simple_elastix.SetParameter("NumberOfSpatialSamples", str(self._nb_spatialsampels))

            # run processing #
            simple_elastix.Execute()

            # get result image and fix image for upload #
            img = simple_elastix.GetResultImage()
            np_img = sitk.GetArrayFromImage(img)
            img_to_save = np.zeros((np_img.shape[0], np_img.shape[1], 3))
            img_to_save[:, :, 1] = np_img
            img_to_save[:, :, 2] = sitk.GetArrayFromImage(fix_image)
            misc.imsave(self._working_path + "/images/" + "result_translationaffine.png", img_to_save)

            # upload config #
            uploadConn = Cytomine(self._cytomine_upload, self._pk, self._prk, verbose=False)
            sync = False

            # uploading image #
            uploadConn.upload_image(self._working_path + "/images/" + "result_translationaffine.png",
                                    self._project_id, self._storage_id, "http://" + self._cytomine_host)

def main(argv):

    # parsing arguments
    parser = ArgumentParser(prog="get_and_move.py", description="workflow with simple elastix")

    parser.add_argument('--cytomine_host', dest="cytomine_host", default='demo.cytomine.be')
    parser.add_argument('--cytomine_public_key', dest="cytomine_public_key")
    parser.add_argument('--cytomine_private_key', dest="cytomine_private_key")
    parser.add_argument('--cytomine_id_software', dest="cytomine_id_software", type=long)
    parser.add_argument("--cytomine_id_project", dest="cytomine_id_project", type=long)
    parser.add_argument('--id_fix_image', dest="id_fix_image", type=long)
    parser.add_argument("--id_mov_image", dest="id_mov_image", type=long)
    parser.add_argument('--nb_iterations', dest="nb_iterations", type=long)
    parser.add_argument("--nb_spatialsampels", dest="nb_spatialsampels", type=long)
    parser.add_argument("--cytomine_storage_id",dest="storage_id",type=long)
    parser.add_argument("--cytomine_id_annotation", dest="id_annotation",type=long)
    parser.add_argument("--cytomine_working_path",dest="working_path")
    parser.add_argument("--cytomine_upload",dest ="cytomine_upload")

    arguments, others = parser.parse_known_args(argv)

    # connection to demo #
    cytomine = Cytomine\
        (
            arguments.cytomine_host,
            arguments.cytomine_public_key,
            arguments.cytomine_private_key,
            working_path=arguments.working_path # = software_routeur/algo/simple_elastix #
        )

    # instance SimpleElastixJob Object and run the logic of the algorithm #
    with SimpleElastixJob\
                 (
                    cytomine, arguments.cytomine_id_software, arguments.cytomine_id_project, arguments.__dict__,
                    arguments.id_fix_image, arguments.id_mov_image, arguments.nb_iterations, arguments.nb_spatialsampels,
                    arguments.storage_id, arguments.id_annotation, arguments.working_path, arguments.cytomine_upload,
                    arguments.cytomine_public_key, arguments.cytomine_private_key
                 ) as context:

        context.run()