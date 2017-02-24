
import SimpleITK as sitk
import scipy.misc as misc
import numpy as np
import csv
from openslide import *
"""
ndpi_path : path to .ndpi image
r : rescale factor
returns: ndpi image resized by factor r in PIL (Image) format
"""
def open_and_resize(ndpi_path):
    image = OpenSlide(ndpi_path)
    (h,w) = image.dimensions
    grey_img = np.asarray(image.get_thumbnail(h, w).convert(mode='L')).astype('double')
    color_img = np.asarray(image.get_thumbnail(h, w)).astype('double')
    image.close()
    return grey_img,color_img

SimpleElastix = sitk.SimpleElastix()

iterationNumbers = 6000
samplingAttemps = 8
spatialSamples = 6000

"""
FixImage = sitk.ReadImage("/home/tvessiere/Pictures/fixtissu.png",sitk.sitkFloat32)
MovingImage = sitk.ReadImage("/home/tvessiere/Pictures/movtissu.png",sitk.sitkFloat32)
"""

fix_image_grey = misc.imread("/home/tvessiere/Pictures/fixtissu2.png",mode='F')
fix_image_color = misc.imread("/home/tvessiere/Pictures/fixtissu2.png",mode='RGB')

mov_image_grey =  misc.imread("/home/tvessiere/Pictures/movtissu2.png",mode='F')
mov_image_color = misc.imread("/home/tvessiere/Pictures/movtissu2.png",mode='RGB')

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

print "Before Exe"
SimpleElastix.Execute()
print "After Exe"

map = SimpleElastix.GetTransformParameterMap()


np_img = sitk.GetArrayFromImage(SimpleElastix.GetResultImage())
TransformX = sitk.SimpleTransformix()
TransformX.SetTransformParameterMap(map)
print type(TransformX.PrintParameterMap())
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

misc.imsave("result_color_overlay.png",img_color_final + (0.65 * fix_image_color))
misc.imsave("result_color.png",img_color_final)

#print sitk.GetArrayFromImage(img_to_save).shape,sitk.GetArrayFromImage(MovingImage).shape,sitk.GetArrayFromImage(FixImage).shape
#misc.imsave("a_result.png",sitk.GetArrayFromImage(img_to_save))
#misc.imsave("a_fix.png",sitk.GetArrayFromImage(FixImage))
#misc.imsave("a_moving.png",sitk.GetArrayFromImage(MovingImage))
#misc.imsave("a_result_elastix.png",sitk.GetArrayFromImage(SimpleElastix.GetResultImage()))