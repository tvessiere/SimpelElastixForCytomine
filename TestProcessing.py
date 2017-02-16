import SimpleITK as sitk
import scipy.misc as misc
import numpy as np
import csv

SimpleElastix = sitk.SimpleElastix()

iterationNumbers = 2048
samplingAttemps = 8
spatialSamples = 4096


FixImage = sitk.ReadImage("/home/tvessiere/Pictures/fixtissu2.png",sitk.sitkFloat32)
MovingImage = sitk.ReadImage("/home/tvessiere/Pictures/movtissu2.png",sitk.sitkFloat32)
print sitk.GetArrayFromImage(FixImage).shape

SimpleElastix.SetFixedImage(FixImage)
SimpleElastix.SetMovingImage(MovingImage)

parameterMapTranslation = sitk.GetDefaultParameterMap("translation")
parameterMapAffine = sitk.GetDefaultParameterMap("affine")
parameterMapSpline = sitk.GetDefaultParameterMap("bspline")

SimpleElastix.SetParameterMap(parameterMapTranslation)
SimpleElastix.AddParameterMap(parameterMapAffine)
SimpleElastix.AddParameterMap(parameterMapSpline)

SimpleElastix.SetParameter("MaximumNumberOfIterations" , str(iterationNumbers))
SimpleElastix.SetParameter("MaximumNumberOfSamplingAttempts" , str(samplingAttemps))
SimpleElastix.SetParameter("NumberOfSpatialSamples" , str(spatialSamples))
SimpleElastix.SetParameter("WriteIterationInfo" , "true")

SimpleElastix.PrintParameterMap()

SimpleElastix.Execute()

img = SimpleElastix.GetResultImage()
np_img = sitk.GetArrayFromImage(img)
img_to_save = np.zeros((np_img.shape[0],np_img.shape[1],3))
img_to_save[:,:,1] = np_img
img_to_save[:,:,2] = sitk.GetArrayFromImage(FixImage)
misc.imsave("result2048_8_4096_translationaffinespline.png",img_to_save)
misc.imsave("fiximage2048_8_4096_trnaslationaffinespline.png",sitk.GetArrayFromImage(FixImage))
misc.imsave("movimage2048_8_4096_trnaslationaffinespline.png",np_img)

c = csv.writer(open("result2048_8_4096_translationaffinespline.csv", "wb"))
c.writerow(["MaximumNumberOfIterations","MaximumNumberOfSamplingAttempts","NumberOfSpatialSamples"])
c.writerow([str(iterationNumbers),str(samplingAttemps),str(spatialSamples)])