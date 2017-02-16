import SimpleITK as sitk
import numpy as np
import scipy.misc as misc

simpleElastix = sitk.SimpleElastix()
simpleElastix.SetParameter( "Metric", "CorrespondingPointsEuclideanDistanceMetric" )
simpleElastix.SetParameter("Registration","AdvancedImageToImageMetric" )
simpleElastix.LogToConsoleOn()
#simpleElastix.SetParameterMap(sitk.GetDefaultParameterMap('rigid'))
#simpleElastix.AddParameterMap(sitk.GetDefaultParameterMap('affine'))
simpleElastix.PrintParameterMap()

fixImage = sitk.ReadImage("/home/tvessiere/Pictures/fixtissu.png",sitk.sitkFloat32)
movingImage = sitk.ReadImage("/home/tvessiere/Pictures/movtissu.png",sitk.sitkFloat32)

simpleElastix.SetFixedImage(fixImage)
simpleElastix.SetMovingImage(movingImage)

simpleElastix.SetFixedPointSetFileName("/home/tvessiere/Pictures/fixpoint.txt")
simpleElastix.SetMovingPointSetFileName("/home/tvessiere/Pictures/movpoint.txt")
simpleElastix.Execute()

img = simpleElastix.GetResultImage()
np_img = sitk.GetArrayFromImage(img)
img_to_save = np.zeros((np_img.shape[0],np_img.shape[1],3))
img_to_save[:,:,1] = np_img
img_to_save[:,:,2] = sitk.GetArrayFromImage(fixImage)
misc.imsave("result.png",img_to_save)