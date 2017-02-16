from cytomine_utilities import CytomineJob
import SimpleITK as sitk
import scipy.misc as misc
import numpy as np
import os
import tempfile
import sys

from argparse import ArgumentParser

def main(argv):

    parser = ArgumentParser(prog="SE_TranslationAffine",
                            description="test SimpelElastix on Cytomine")

    parser.add_argument('--cytomine_host', dest="cytomine_host", default='demo.cytomine.be')
    parser.add_argument('--cytomine_public_key', dest="cytomine_public_key")
    parser.add_argument('--cytomine_private_key', dest="cytomine_private_key")
    parser.add_argument('--cytomine_id_software',dest="cytomine_id_software")
    parser.add_argument('--cytomine_base_path', dest="cytomine_base_path", default='/api/')
    parser.add_argument('--cytomine_id_software', dest="cytomine_id_software", type=int)
    parser.add_argument('--cytomine_id_project', dest="cytomine_id_project", type=int)
    parser.add_argument('--cytomine_id_fiximage',dest="cytomine_id_fiximage", type=int)
    parser.add_argument('--cytomine_id_movimage', dest="cytomine_id_movimage", type=int)
    parser.add_argument('--cytomine_nbiterations', dest="cytomine_nbiterations", type=int)
    parser.add_argument('--cytomine_nbspatialsampels', dest="cytomine_nbspatialsampels", type=int)
    default_saveimg_path = os.path.join(tempfile.gettempdir(), "Pictures")
    parser.add_argument("--working_path", dest="working_path", default=default_saveimg_path)
    default_working_path = os.path.join(tempfile.gettempdir(), "cytomine")
    parser.add_argument('--cytomine_working_path', dest="cytomine_working_path", default=default_working_path)


if __name__ == "__main__":
    main(sys.argv[1:])