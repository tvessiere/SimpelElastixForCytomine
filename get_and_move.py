
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
                 id_annotation_fix, id_annotation_moving, working_path, cytomine_host, cytomine_upload, pk, prk,exort_overlay_images):

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
        self._overlayed_images = exort_overlay_images

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
        fix_image_grey = misc.imread(path_to_fix_image, mode='F')
        fix_image_color = misc.imread(path_to_fix_image, mode='RGB')

        moving_image_grey = misc.imread(path_to_moving_image, mode='F')
        moving_image_color = misc.imread(path_to_moving_image, mode='RGB')

        # get images with ITK format #
        itk_fix_image = sitk.GetImageFromArray(fix_image_grey)
        itk_moving_image = sitk.GetImageFromArray(moving_image_grey)

        # start processing algorithm #
        # got all the channel for keep orignal color #
        itk_mov_image_color_0 = sitk.GetImageFromArray(moving_image_color[:, :, 0])
        itk_mov_image_color_1 = sitk.GetImageFromArray(moving_image_color[:, :, 1])
        itk_mov_image_color_2 = sitk.GetImageFromArray(moving_image_color[:, :, 2])

        # set ParamtersMap to sitk for compute transformation #
        simple_elastix = sitk.SimpleElastix()
        simple_elastix.SetFixedImage(itk_fix_image)
        simple_elastix.SetMovingImage(itk_moving_image)
        parameter_map_translation = sitk.GetDefaultParameterMap("translation")
        parameter_map_affine = sitk.GetDefaultParameterMap("affine")

        # translation & affine #
        simple_elastix.SetParameterMap(parameter_map_translation)
        simple_elastix.AddParameterMap(parameter_map_affine)

        # params set by user #
        simple_elastix.SetParameter("MaximumNumberOfIterations", str(self._nb_iterations))
        simple_elastix.SetParameter("NumberOfSpatialSamples", str(self._nb_spatial_sampel))

        # start computing #
        simple_elastix.Execute()

        # get parameters of the transform for apply it on 3 channels #
        transform_map = simple_elastix.GetTransformParameterMap()
        # for set shape of images #
        np_img = sitk.GetArrayFromImage(simple_elastix.GetResultImage())

        # set parameterMap & complete properties_map #
        properties_map = {}
        transform_x = sitk.SimpleTransformix()
        transform_x.SetTransformParameterMap(transform_map)

        # translation map #
        param = transform_x.GetTransformParameter(0, "DefaultPixelValue")
        properties_map["sitk_translation_default_pixel_value"] = param[0]  # float #
        param = transform_x.GetTransformParameter(0, "Direction")
        properties_map[ "sitk_translation_direction"] = param  # tuple with 4 ints #
        param = transform_x.GetTransformParameter(0, "FinalBSplineInterpolationOrder")
        properties_map["sitk_translation_final_bspline_interpolation_order"] = param[0]  # int #
        param = transform_x.GetTransformParameter(0, "FixedImageDimension")
        properties_map["sitk_translation_fixed_image_dimension"] = param[0]  # int #
        param = transform_x.GetTransformParameter(0, "FixedInternalImagePixelType")
        properties_map["sitk_translation_fixed_internal_image_pixel_type"] = param[0]  # string #
        param = transform_x.GetTransformParameter(0, "HowToCombineTransforms")
        properties_map["sitk_translation_how_combine_transforms"] = param[0]  # string #
        param = transform_x.GetTransformParameter(0, "Index")
        properties_map["sitk_translation_index"] = param  # tuple with 2 int #
        param = transform_x.GetTransformParameter(0, "InitialTransformParametersFileName")
        properties_map["sitk_translation_initial_transform_parameters_file_name"] = param[0]  # string #
        param = transform_x.GetTransformParameter(0, "MovingImageDimension")
        properties_map["sitk_translation_moving_image_dimension"] = param[0]  # int #
        param = transform_x.GetTransformParameter(0, "MovingInternalImagePixelType")
        properties_map["sitk_translation_moving_internal_image_pixel_type"] = param[0]  # string #
        param = transform_x.GetTransformParameter(0, "NumberOfParameters")
        properties_map["sitk_translation_number_of_parameters"] = param[0]  # int #
        param = transform_x.GetTransformParameter(0, "Origin")
        properties_map["sitk_translation_origin"] = param  # tuple with 2 ints #
        param = transform_x.GetTransformParameter(0, "ResampleInterpolator")
        properties_map["sitk_translation_resample_interpolator"] = param[0]  # string #
        param = transform_x.GetTransformParameter(0, "Resampler")
        properties_map["sitk_translation_resampler"] = param[0]  # string #
        param = transform_x.GetTransformParameter(0, "Spacing")
        properties_map["sitk_translation_spacing"] = param  # tuple with 2 ints #
        param = transform_x.GetTransformParameter(0, "Transform")
        properties_map["sitk_translation_transform"] = param[0]  # string #
        param = transform_x.GetTransformParameter(0, "TransformParameters")
        properties_map["sitk_translation_transform_parameters"] = param  # tuple with number_of_parameters floats #
        param = transform_x.GetTransformParameter(0, "UseDirectionCosines")
        properties_map["sitk_translation_use_directions_Cosines"] = bool(param[0])  # boolean #

        # affine map #
        param = transform_x.GetTransformParameter(1, "CenterOfRotationPoint")
        properties_map["sitk_affine_centre_of_rotation_x"] = param[0]  # int #
        properties_map["sitk_affine_centre_of_rotation_y"] = param[1]  # int #
        param = transform_x.GetTransformParameter(1, "DefaultPixelValue")
        properties_map["sitk_affine_default_pixel_value"] = param[0]  # int #
        param = transform_x.GetTransformParameter(1, "Direction")
        properties_map["sitk_affine_direction"] = param  # tuple with 4 ints #
        param = transform_x.GetTransformParameter(1, "FinalBSplineInterpolationOrder")
        properties_map["sitk_affine_final_bspline_interpolator_order"] = param[0]  # int #
        param = transform_x.GetTransformParameter(1, "FixedImageDimension")
        properties_map["sitk_affine_fixed_image_dimension"] = param[0]  # int #
        param = transform_x.GetTransformParameter(1, "FixedInternalImagePixelType")
        properties_map["sitk_affine_fixed_internal_image_type"] = param[0]  # string #
        param = transform_x.GetTransformParameter(1, "HowToCombineTransforms")
        properties_map["sitk_affine_how_to_combine_transform"] = param[0]  # string #
        param = transform_x.GetTransformParameter(1, "Index")
        properties_map["sitk_affine_index"] = param  # tuple with 2 ints #
        param = transform_x.GetTransformParameter(1, "InitialTransformParametersFileName")
        properties_map["sitk_affine_initial_transform_parameter_file_name"] = param[0]  # int #
        param = transform_x.GetTransformParameter(1, "MovingImageDimension")
        properties_map["sitk_affine_moving_image_dimension"] = param[0]  # int #
        param = transform_x.GetTransformParameter(1, "NumberOfParameters")
        properties_map["sitk_affine_number_of_parameters"] = param[0]  # int #
        param = transform_x.GetTransformParameter(1, "MovingInternalImagePixelType")
        properties_map["sitk_affine_moving_internal_image_pixel_type"] = param[0]  # string #
        param = transform_x.GetTransformParameter(1, "Origin")
        properties_map["sitk_affine_origin"] = param  # tuple with 2 ints #
        param = transform_x.GetTransformParameter(1, "ResampleInterpolator")
        properties_map["sitk_affine_resample_interpolator"] = param[0]  # string #
        param = transform_x.GetTransformParameter(1, "Resampler")
        properties_map["sitk_affine_resample_Resampler"] = param[0]  # string #
        param = transform_x.GetTransformParameter(1, "Transform")
        properties_map["sitk_affine_transform"] = param[0]  # string #
        param = transform_x.GetTransformParameter(1, "TransformParameters")
        properties_map["sitk_affine_transform_parameters"] = param  # tuple with sitk_affine_number_of_parameters float #
        param = transform_x.GetTransformParameter(1, "UseDirectionCosines")
        properties_map["sitk_affine_use_direction_Cosines"] = bool(param[0])  # boolean #
        param = transform_x.GetTransformParameter(1, "Spacing")
        properties_map["sitk_affine_Spacing"] = param  # tuple with 2 ints #

        # apply transforms on all channels #
        transform_x.SetMovingImage(itk_mov_image_color_0)
        img_to_save_0 = transform_x.Execute()
        transform_x.SetMovingImage(itk_mov_image_color_1)
        img_to_save_1 = transform_x.Execute()
        transform_x.SetMovingImage(itk_mov_image_color_2)
        img_to_save_2 = transform_x.Execute()

        # format image color #
        img_color_final = np.zeros((np_img.shape[0], np_img.shape[1], 3))

        img_color_final[:, :, 0] = sitk.GetArrayFromImage(img_to_save_0)
        img_color_final[:, :, 1] = sitk.GetArrayFromImage(img_to_save_1)
        img_color_final[:, :, 2] = sitk.GetArrayFromImage(img_to_save_2)

        # save images #
        # DONT FORGET TO FORMAT THE MAP FOR IMAGE'S PROPERTIES #
        img_transform_to_save_path = os.path.join(self._working_path, "images", str(self.job.id),"result_translationaffine.png")

        if(self._overlayed_images == True):
            img_overlay_to_save_path = os.path.join(self._working_path, "images", str(self.job.id),"overlayed_images.png")
            misc.imsave(img_transform_to_save_path,img_color_final)
            misc.imsave(img_overlay_to_save_path, img_color_final + (0.75 * fix_image_color))

            # connection to demo-upload #
            demo_upload = Cytomine(self._cytomine_upload, self._pk, self._prk, verbose=True)
            demo_upload.upload_image(img_transform_to_save_path, self._project_id, self._storage_id, "http://demo.cytomine.be",properties=properties_map)
            # DONT FORGET TO COMPLETE PROPERTIES #
            demo_upload.upload_image(img_overlay_to_save_path,self._project_id, self._storage_id, "http://demo.cytomine.be",properties=None)

        else:
            misc.imsave(img_transform_to_save_path, img_color_final)
            misc.imsave(img_transform_to_save_path,img_color_final)

            # connection to demo-upload #
            demo_upload = Cytomine(self._cytomine_upload, self._pk, self._prk, verbose=True)
            # DONT FORGET TO COMPLETE PROPERTIES #
            demo_upload.upload_image(img_transform_to_save_path, self._project_id, self._storage_id,  "http://demo.cytomine.be", properties=properties_map)

        # remove the directory of the current job #
        shutil.rmtree(os.path.join(self._working_path, "images", str(self.job.id)), ignore_errors=True)

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
    parser.add_argument("--export_overlay_images",dest="export_overlay_images")

    arguments, others = parser.parse_known_args(argv)

    # connection to demo #
    cytomine = Cytomine\
        (
            arguments.cytomine_host,
            arguments.cytomine_public_key,
            arguments.cytomine_private_key,
            working_path=arguments.working_path # = software_routeur/algo/simple_elastix #
        )

    # instance SimpleElastixJob object and run the logic of the algorithm #
    with SimpleElastixJob\
                 (
                    cytomine, arguments.cytomine_id_software, arguments.cytomine_id_project, arguments.__dict__,
                    arguments.id_fix_image, arguments.id_mov_image, arguments.nb_iterations, arguments.nb_spatialsampels,
                    arguments.storage_id, arguments.id_annotation_fix, arguments.id_annotation_moving, arguments.working_path,
                    arguments.cytomine_upload,arguments.cytomine_public_key, arguments.cytomine_private_key,arguments.export_overlay_images
                 ) as context:

        context.run()