import SimpleITK as sitk

fixImage = sitk.ReadImage("/home/tvessiere/Pictures/fixtissu.png",sitk.sitkFloat32)
movingImage = sitk.ReadImage("/home/tvessiere/Pictures/movtissu.png",sitk.sitkFloat32)


