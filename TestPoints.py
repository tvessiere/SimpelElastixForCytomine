import SimpleITK as sitk
# Compute the transformation from moving image to the fixed image


SimpleElastix = sitk.SimpleElastix()
FixImage = sitk.ReadImage("/home/tvessiere/Pictures/fixtissu.png",sitk.sitkFloat32)
MovingImage = sitk.ReadImage("/home/tvessiere/Pictures/movtissu.png",sitk.sitkFloat32)
SimpleElastix.SetFixedImage(FixImage)
SimpleElastix.SetMovingImage(MovingImage)
SimpleElastix.Execute()
# Warp point set. The transformed points will be written to a file named
# outputpoints.txt in the output directory determined by SetOutputDirectory()
# (defaults to working directory)
SimpleTransformix = sitk.SimpleTransformix()
SimpleTransformix.SetFixedPointSetFileName("/home/tvessiere/Pictures/movpoint.txt")
SimpleTransformix.AddTransformParameterMap(sitk.GetDefaultParameterMap("bspline"))
SimpleTransformix.PrintParameterMap()
SimpleTransformix.Execute()