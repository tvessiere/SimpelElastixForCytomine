
import SimpleITK as sitk
import scipy.misc as misc
import numpy as np
import csv
from openslide import *


def ComposeProperties(dictionnaire,mode):
    for param_name, prop_name in dictionnaire.items():
        if prop_name[1] == False:
            properties_map[prop_name[0]] = TransformX.GetTransformParameter(mode,param_name)[0]
        else:
            for i,v in enumerate(TransformX.GetTransformParameter(mode,param_name)):
                properties_map["{}_{}".format(prop_name[0],i)] = v
    print properties_map

if __name__ == "__main__":
    SimpleElastix = sitk.SimpleElastix()

    iterationNumbers = 512
    samplingAttemps = 8
    spatialSamples = 6000

    FixImage = sitk.ReadImage("/home/tvessiere/Pictures/fixtissu.png",sitk.sitkFloat32)
    MovingImage = sitk.ReadImage("/home/tvessiere/Pictures/movtissu.png",sitk.sitkFloat32)

    fix_image_grey = misc.imread("/home/tvessiere/Pictures/fixtissu.png",mode='F')
    fix_image_color = misc.imread("/home/tvessiere/Pictures/fixtissu.png",mode='RGB')

    mov_image_grey = misc.imread("/home/tvessiere/Pictures/movtissu.png",mode='F')
    mov_image_color = misc.imread("/home/tvessiere/Pictures/movtissu.png",mode='RGB')

    itk_fix_image = sitk.GetImageFromArray(fix_image_grey)
    itk_mov_image = sitk.GetImageFromArray(mov_image_grey)

    itk_mov_image_color_0 = sitk.GetImageFromArray(mov_image_color[:,:,0])
    itk_mov_image_color_1 = sitk.GetImageFromArray(mov_image_color[:,:,1])
    itk_mov_image_color_2 = sitk.GetImageFromArray(mov_image_color[:,:,2])

    SimpleElastix.SetFixedImage(itk_fix_image)
    SimpleElastix.SetMovingImage(itk_mov_image)

    parameterMapTranslation = sitk.GetDefaultParameterMap("translation")
    parameterMapAffine = sitk.GetDefaultParameterMap("affine")


    SimpleElastix.SetParameterMap(parameterMapTranslation)
    SimpleElastix.AddParameterMap(parameterMapAffine)

    SimpleElastix.SetParameter("MaximumNumberOfIterations" , str(iterationNumbers))
    SimpleElastix.SetParameter("MaximumNumberOfSamplingAttempts" , str(samplingAttemps))
    SimpleElastix.SetParameter("NumberOfSpatialSamples" , str(spatialSamples))
    SimpleElastix.SetParameter("WriteIterationInfo" , "true")

    SimpleElastix.Execute()

    transform_map = SimpleElastix.GetTransformParameterMap()
    properties_map = {}

    np_img = sitk.GetArrayFromImage(SimpleElastix.GetResultImage())
    TransformX = sitk.SimpleTransformix()
    TransformX.SetTransformParameterMap(transform_map)

    dict_translation = {
        "DefaultPixelValue": ("sitk_translation_default_pixel_value",False), # int #
        "Direction": ("sitk_translation_direction", True), # tuple with 4 ints #
        "FinalBSplineInterpolationOrder": ("sitk_translation_final_bspline_interpolation_order", False),# int #
        "FixedImageDimension": ("sitk_translation_fixed_image_dimension", False) ,# int #
        "FixedInternalImagePixelType": ("sitk_translation_fixed_internal_image_pixel_type", False), # string #
        "HowToCombineTransforms": ("sitk_translation_how_combine_transforms", False) , # string #
        "Index": ("sitk_translation_index", True), # tuple with 2 int #
        "InitialTransformParametersFileName": ("sitk_translation_initial_transform_parameters_file_name", False) ,
        "MovingImageDimension": ("sitk_translation_moving_image_dimension", False) ,
        "MovingInternalImagePixelType": ("sitk_translation_moving_internal_image_pixel_type", False) ,
        "NumberOfParameters": ("sitk_translation_number_of_parameters", False) ,
        "Origin": ("sitk_translation_origin", True) ,
        "ResampleInterpolator": ("sitk_translation_resample_interpolator", False) ,
        "Resampler": ("sitk_translation_resampler", False) ,
        "Spacing": ("sitk_translation_spacing", True) ,
        "Transform": ("sitk_translation_transform", False) ,
        "TransformParameters": ("sitk_translation_transform_parameters", True) ,
        "UseDirectionCosines": ("sitk_translation_use_directions_Cosines", False) ,
    }

    ComposeProperties(dict_translation,0)

    dict_affine = {
        "CenterOfRotationPoint": ("sitk_affine_centrer_of_rotation", True ),
        "DefaultPixelValue": ("sitk_affine_default_pixel_value", False) ,
        "Direction": ("sitk_affine_direction", True ) ,
        "FinalBSplineInterpolationOrder": ("sitk_affine_final_bspline_interpolation_order", False) ,
        "FixedImageDimension": ("sitk_affine_fixed_image_dimension", False) ,
        "FixedInternalImagePixelType": ("sitk_affine_fixed_internal_image_pixel_type", False) ,
        "HowToCombineTransforms": ("sitk_affine_how_combine_transforms", False ) ,
        "Index": ("sitk_affine_index", True) ,
        "InitialTransformParametersFileName": ("sitk_affine_initial_transform_parameters_file_name", False) ,
        "MovingImageDimension": ("sitk_affine_moving_image_dimension", False) ,
        "MovingInternalImagePixelType": ("sitk_affine_moving_internal_image_pixel_type", False) ,
        "NumberOfParameters": ("sitk_affine_number_of_parameters", False) ,
        "Origin": ("sitk_affine_origin", True) ,
        "ResampleInterpolator": ("sitk_affine_resample_interpolator", False) ,
        "Resampler": ("sitk_affine_resampler", False) ,
        "Spacing": ("sitk_affine_spacing", True) ,
        "Transform": ("sitk_affine_transform", False) ,
        "TransformParameters": ("sitk_affine_transform_parameters", True) ,
        "UseDirectionCosines": ("sitk_affine_use_directions_Cosines" , False) ,
    }

    ComposeProperties(dict_affine, 1)

    """"# translation #
    param = TransformX.GetTransformParameter(0,"DefaultPixelValue")
    properties_map["sitk_translation_default_pixel_value"] = param[0] # float #
    param = TransformX.GetTransformParameter(0,"Direction")
    properties_map["sitk_translation_direction"] = param # tuple with 4 ints #
    param = TransformX.GetTransformParameter(0,"FinalBSplineInterpolationOrder")
    properties_map["sitk_translation_final_bspline_interpolation_order"] = param[0] # int #
    param = TransformX.GetTransformParameter(0,"FixedImageDimension")
    properties_map["sitk_translation_fixed_image_dimension"] = param[0] # int #
    param = TransformX.GetTransformParameter(0,"FixedInternalImagePixelType")
    properties_map["sitk_translation_fixed_internal_image_pixel_type"] = param[0] # float #
    param = TransformX.GetTransformParameter(0,"HowToCombineTransforms")
    properties_map["sitk_translation_how_combine_transforms"] = param[0] # string #
    param = TransformX.GetTransformParameter(0,"Index")
    properties_map["sitk_translation_index"] = param # tuple with 2 int #
    param = TransformX.GetTransformParameter(0,"InitialTransformParametersFileName")
    properties_map["sitk_translation_initial_transform_parameters_file_name"] = param[0] # string #
    param = TransformX.GetTransformParameter(0,"MovingImageDimension")
    properties_map["sitk_translation_moving_image_dimension"] = param[0] # int #
    param = TransformX.GetTransformParameter(0,"MovingInternalImagePixelType")
    properties_map["sitk_translation_moving_internal_image_pixel_type"] = param[0] # string #
    param = TransformX.GetTransformParameter(0,"NumberOfParameters")
    properties_map["sitk_translation_number_of_parameters"] = param[0] # int #
    param = TransformX.GetTransformParameter(0,"Origin")
    properties_map["sitk_translation_origin"] = param # tuple with 2 ints #
    param = TransformX.GetTransformParameter(0,"ResampleInterpolator")
    properties_map["sitk_translation_resample_interpolator"] = param[0] # string #
    param = TransformX.GetTransformParameter(0,"Resampler")
    properties_map["sitk_translation_resampler"] = param[0] # string #
    param = TransformX.GetTransformParameter(0,"Spacing")
    properties_map["sitk_translation_spacing"] = param # tuple with 2 ints #
    param = TransformX.GetTransformParameter(0,"Transform")
    properties_map["sitk_translation_transform"] = param[0] # string #
    param = TransformX.GetTransformParameter(0,"TransformParameters")
    properties_map["sitk_translation_transform_parameters"] = param # tuple with number_of_parameters floats #
    param = TransformX.GetTransformParameter(0,"UseDirectionCosines")

    properties_map["sitk_translation_use_directions_Cosines"] = bool(param[0]) # boolean #

    # affine #
    param = TransformX.GetTransformParameter(1,"CenterOfRotationPoint")
    properties_map["sitk_affine_centre_of_rotation_x"] = param[0] # int #
    properties_map["sitk_affine_centre_of_rotation_y"] = param[1] # int #
    param = TransformX.GetTransformParameter(1,"DefaultPixelValue")
    properties_map["sitk_affine_default_pixel_value"] = param[0] # int #
    param = TransformX.GetTransformParameter(1,"Direction")
    properties_map["sitk_affine_direction"] = param # tuple with 4 ints #
    param = TransformX.GetTransformParameter(1,"FinalBSplineInterpolationOrder")
    properties_map["sitk_affine_final_bspline_interpolator_order"] = param[0] # int #
    param = TransformX.GetTransformParameter(1,"FixedImageDimension")
    properties_map["sitk_affine_fixed_image_dimension"] = param[0] # int #
    param = TransformX.GetTransformParameter(1,"FixedInternalImagePixelType")
    properties_map["sitk_affine_fixed_internal_image_type"] = param[0] # string #
    param = TransformX.GetTransformParameter(1,"HowToCombineTransforms")
    properties_map["sitk_affine_how_to_combine_transform"] = param[0] # string #
    param = TransformX.GetTransformParameter(1,"Index")
    properties_map["sitk_affine_index"] = param # tuple with 2 ints #
    param = TransformX.GetTransformParameter(1,"InitialTransformParametersFileName")
    properties_map["sitk_affine_initial_transform_parameter_file_name"] = param[0] # int #
    param = TransformX.GetTransformParameter(1,"MovingImageDimension")
    properties_map["sitk_affine_moving_image_dimension"] = param[0] # int #
    param = TransformX.GetTransformParameter(1,"NumberOfParameters")
    properties_map["sitk_affine_number_of_parameters"] = param[0] # int #
    param = TransformX.GetTransformParameter(1,"MovingInternalImagePixelType")
    properties_map["sitk_affine_moving_internal_image_pixel_type"] = param[0] # string #
    param = TransformX.GetTransformParameter(1,"Origin")
    properties_map["sitk_affine_origin"] = param # tuple with 2 ints #
    param = TransformX.GetTransformParameter(1,"ResampleInterpolator")
    properties_map["sitk_affine_resample_interpolator"] = param[0] # string #
    param = TransformX.GetTransformParameter(1,"Resampler")
    properties_map["sitk_affine_resample_Resampler"] = param[0] # string #
    param = TransformX.GetTransformParameter(1,"Transform")
    properties_map["sitk_affine_transform"] = param[0] # string #
    param = TransformX.GetTransformParameter(1,"TransformParameters")
    properties_map["sitk_affine_transform_parameters"] = param # tuple with number_of_parameters float #
    param = TransformX.GetTransformParameter(1,"UseDirectionCosines")
    properties_map["sitk_affine_use_direction_Cosines"] = bool(param[0]) # boolean #
    param = TransformX.GetTransformParameter(1,"Spacing")
    properties_map["sitk_affine_Spacing"] = param # tuple with 2 ints #
    print type(properties_map["sitk_affine_Spacing"])"""

    TransformX.SetMovingImage(itk_mov_image_color_0)
    img_to_save_0 = TransformX.Execute()
    TransformX.SetMovingImage(itk_mov_image_color_1)
    img_to_save_1 = TransformX.Execute()
    TransformX.SetMovingImage(itk_mov_image_color_2)
    img_to_save_2 = TransformX.Execute()

    img_color_final = img_to_save = np.zeros((np_img.shape[0],np_img.shape[1],3))

    img_color_final[:,:,0] = sitk.GetArrayFromImage(img_to_save_0)
    img_color_final[:,:,1] = sitk.GetArrayFromImage(img_to_save_1)
    img_color_final[:,:,2] = sitk.GetArrayFromImage(img_to_save_2)

    misc.imsave("result_color_overlay.png",img_color_final + (0.80 * fix_image_color))
    misc.imsave("result_color.png",img_color_final)

    #print sitk.GetArrayFromImage(img_to_save).shape,sitk.GetArrayFromImage(MovingImage).shape,sitk.GetArrayFromImage(FixImage).shape
    #misc.imsave("a_result.png",sitk.GetArrayFromImage(img_to_save))
    #misc.imsave("a_fix.png",sitk.GetArrayFromImage(FixImage))
    #misc.imsave("a_moving.png",sitk.GetArrayFromImage(MovingImage))
    #misc.imsave("a_result_elastix.png",sitk.GetArrayFromImage(SimpleElastix.GetResultImage()))

