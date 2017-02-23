
__author__ = "Vessiere Thomas <vessiere.thomas@hotmail.com>"
__Copyright__ = "Copyright 2010-2017 University of Liège, Belgium, http://www.cytomine.be/"

from argparse import ArgumentParser
from sldc import Loggable, Logger, StandardOutputLogger
from cytomine import Cytomine
from cytomine_utilities import CytomineJob
import SimpleITK as sitk
import scipy.misc as misc
import numpy as np
import shutil
import os

class SimpleElastixJob(CytomineJob, Loggable):

    # set parameters for your algo, 4 first params must be like this #
    def __init__(self, cytomine, software_id, project_id, job_parameters,
                 fix_image_id, moving_image_id, nb_spatial_sample, nb_iterations, storage_id,
                 id_annotation_fix, id_annotation_moving, working_path, cytomine_host, cytomine_upload, pk, prk):

        # call init from parent classes #
        CytomineJob.__init__(self, cytomine, software_id, project_id, """parameters=job_parameters""" )
        Loggable.__init__(self, logger=StandardOutputLogger(Logger.INFO))

        # keep var from parameters #
        self._fix_image_id = fix_image_id
        self._moving_image_id = moving_image_id
        self._nb_spatial_sampel = nb_spatial_sample
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
            self._cytomine.dump_project_images(id_project=self._project_id, dest_path=os.path.join(self._working_path, "images" , str(self.job.id)), override=True, max_size=True)

            # format paths #
            path_to_fix_image = os.path.join(self._working_path,"images",str(self.job.id),str(self._fix_image_id))
            path_to_moving_image = os.path.join(self._working_path, "images", str(self.job.id), str(self._moving_image_id))

            # debug #
            print "path_to_fix_image : " + str(path_to_fix_image)
            print "path_to_moving_image" + str(path_to_moving_image)

        else:
            # dump annotations#
            annotation_fix = self._cytomine.get_annotation(self._fix_image_id)
            collection_fix = self._cytomine.AnnotationCollection()
            collection_fix.data().append(annotation_fix)

            self._cytomine.dump_annotations\
                                    (
                                        annotations=collection_fix,
                                        get_image_url_func=self._cytomine.Annotation.get_annotation_crop_url,
                                        dest_path= os.path.join(self._working_path,"images",str(self.job.id),"annotation_fix"),
                                        desired_zoom=0
                                    )

            annotation_moving = self._cytomine.get_annotation(self._id_annotation_moving)
            collection_moving = self._cytomine.AnnotationCollection()
            collection_moving.data().append(annotation_moving)

            self._cytomine.dump_annotations\
                                    (
                                        annotations=collection_moving,
                                        get_image_url_func=self._cytomine.Annotation.get_annotation_crop_url,
                                        dest_path = os.path.join(self._working_path,"images",str(self.job.id),"annotation_moving"),
                                        desired_zoom=0
                                    )

            # get id_term for path #
            id_term = annotation_fix.term[0]

            # because the name of the file is vague, just list the file and get the elem at 0 #
            list_fix = os.listdir(os.path.join(self._working_path,"images",str(self.job.id),"annotation_fix"),str(id_term))
            list_moving = os.listdir(os.path.join(self._working_path,"images",str(self.job.id),"annotation_moving"),str(id_term))

            # format paths #
            path_to_fix_image = os.path.join(self._working_path,"images",str(self.job.id),"annotation_fix",str(id_term),str(list_fix[0]))
            path_to_moving_image = os.path.join(self._working_path,"images",str(self.job.id),"annotation_moving",str(id_term),str(list_moving[0]))

            # debug #
            print "path_to_fix_image : " + str(path_to_fix_image)
            print "path_to_moving_image" + str(path_to_moving_image)



        # load images #
        fix_image = sitk.ReadImage(path_to_fix_image, sitk.sitkFloat32)
        moving_image = sitk.ReadImage(path_to_moving_image, sitk.sitkFloat32)

        # start processing algorithm #
        simple_elastix = sitk.SimpleElastix()
        simple_elastix.SetFixedImage(fix_image)
        simple_elastix.SetMovingImage(moving_image)
        parameterMapTranslation = sitk.GetDefaultParameterMap("translation")
        parameterMapAffine = sitk.GetDefaultParameterMap("affine")

        # translation & affine #
        simple_elastix.SetParameterMap(parameterMapTranslation)
        simple_elastix.AddParameterMap(parameterMapAffine)

        # params set by user #
        simple_elastix.SetParameter("MaximumNumberOfIterations", str(self._nb_iterations))
        simple_elastix.SetParameter("NumberOfSpatialSamples", str(self._nb_spatial_sampel))

        # start computing #
        simple_elastix.Execute()

        # format image result #
        img = simple_elastix.GetResultImage()
        np_img = sitk.GetArrayFromImage(img)
        img_to_save = np.zeros((np_img.shape[0], np_img.shape[1], 3))
        img_to_save[:, :, 1] = np_img
        img_to_save[:, :, 2] = sitk.GetArrayFromImage(fix_image)
        img_to_save_path = os.path.join(self._working_path,"images",str(self._storage_id),"result_translationaffine.png")
        misc.imsave(img_to_save_path, img_to_save)

        # connection to demo-upload #
        demo_upload = Cytomine(self._cytomine_upload, self._pk, self._prk, verbose=True)

        demo_upload.upload_image(img_to_save_path,self._project_id, self._storage_id, "http://demo.cytomine.be")

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
    parser.add_argument("--cytomine_id_annotation_fix", dest="id_annotation_fix",type=long)
    parser.add_argument("--cytomine_id_annotation_moving", dest="id_annotation_moving", type=long)
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
                    arguments.storage_id, arguments.id_annotation_fix, arguments.id_annotation_moving, arguments.working_path,
                    arguments.cytomine_upload,arguments.cytomine_public_key, arguments.cytomine_private_key
                 ) as context:

        context.run()
