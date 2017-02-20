from argparse import ArgumentParser
import SimpleITK as stik


def main(argv):
    parser = ArgumentParser(prog="TestParser", description="Catch argment form exec cmd")

    parser.add_argument('--cytomine_host', dest="cytomine_host", default='demo.cytomine.be')
    parser.add_argument('--cytomine_public_key', dest="cytomine_public_key")
    parser.add_argument('--cytomine_private_key', dest="cytomine_private_key")
    parser.add_argument('--cytomine_id_software', dest="cytomine_id_software", type=int)
    parser.add_argument("--cytomine_id_project", dest="cytomine_id_project", type=int)
    parser.add_argument('--id_fix_image', dest="id_fix_image", type=int)
    parser.add_argument("--id_mov_image", dest="id_mov_image", type=int)
    parser.add_argument('--nb_iterations', dest="nb_iterations", type=int)
    parser.add_argument("--nb_spatialsampels", dest="nb_spatialsampels", type=int)
    arguments, others = parser.parse_known_args(argv)


    fixImage = arguments.id_fix_image
    movImage = arguments.id_mov_image
    idProject = arguments.cytomine_id_project

    workingPath = "/home/tvessiere/data/Project/TestProcessing/Images"

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])