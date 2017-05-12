__author__ = "Vessiere Thomas <vessiere.thomas@hotmail.com>"
__Copyright__ = "Copyright 2010-2017 University of Liege, Belgium, http://www.cytomine.be/"


import os
import tempfile

if __name__ == "__main__":
    import cytomine

    # Connect to cytomine, edit connection values

    cytomine_host = "http://localhost-core:8080"
    Pk = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    Prk = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    id_project = 19941904

    # Connection to Cytomine Core
    conn = cytomine.Cytomine(
        cytomine_host,
        Pk,
        Prk,
        base_path='/api/',
        working_path=os.path.join(tempfile.gettempdir(), "cytomine"),
        verbose=True
    )

    #add software with execute command
    software = conn.add_software("Simple_Elastix","createRabbitJobWithArgsService","download","/root/miniconda2/envs/cytomine/bin/python software_routeur/algo/simple_elastix/get_and_move.py "+
                                                                                                     "--cytomine_host $cytomine_host " +
                                                                                                     "--cytomine_public_key $cytomine_public_key " +
                                                                                                     "--cytomine_private_key $cytomine_private_key " +
                                                                                                     "--cytomine_id_software $cytomine_id_software " +
                                                                                                     "--cytomine_working_path software_router/algo/simple_elastix " +
                                                                                                     "--cytomine_id_project $cytomine_id_project " +
                                                                                                     "--fix_image_id fix_image " +
                                                                                                     "--mov_image_id $id_mov_image " +
                                                                                                     "--nb_iterations $nb_iterations " +
                                                                                                     "--nb_spatialsampels $nb_spatial_sample " +
                                                                                                     "--cytomine_storage_id $storage " +
                                                                                                     "--cytomine_annotation_fix_id $annotation_fix_id " +
                                                                                                     "--cytomine_annotation_moving_id $annotation_moving_id " +
                                                                                                     "--cytomine_upload demo-upload.cytomine.be " +
                                                                                                     "--export_overlay_images $export_overlay_images " +
                                                                                                     "--number_of_resolutions $number_of_resolutions " +
                                                                                                     "--result_file_name $result_file_name "
                                 )


    conn.add_software_parameter(name="fix_image",id_software=software.id,type= "Number",default_value=None,required=True,index=10,set_by_server=False)
    conn.add_software_parameter(name="moving_image",id_software=software.id,type= "Number",default_value=None,required=True,index=20,set_by_server=False)
    conn.add_software_parameter(name="nb_iterations",id_software=software.id,type= "Number",default_value=None,required=True,index=30,set_by_server=False)
    conn.add_software_parameter(name="nb_spatial_sample",id_software=software.id,type= "Number",default_value=None,required=True,index=40,set_by_server=False)
    conn.add_software_parameter(name="storage",id_software=software.id,type= "Number",default_value=None,required=True,index=50,set_by_server=False)
    conn.add_software_parameter(name="annotation_fix_id",id_software=software.id,type= "Number",default_value=None,required=False,index=60,set_by_server=False)
    conn.add_software_parameter(name="annotation_moving_id",id_software=software.id,type= "Number",default_value=None,required=False,index=70,set_by_server=False)
    conn.add_software_parameter(name="upload_server",id_software=software.id,type= "Number",default_value=None,required=True,index=80,set_by_server=True)
    conn.add_software_parameter(name="annotation_moving_id",id_software=software.id,type= "Number",default_value=None,required=False,index=90,set_by_server=True)
    conn.add_software_parameter(name="cytomine_id_software",id_software=software.id,type= "Number",default_value= 0,required= True, index=100, set_by_server=True)
    conn.add_software_parameter(name="cytomine_id_project",id_software=software.id,type= "Number",default_value= 0,required= True, index=110, set_by_server=True)
    conn.add_software_parameter(name="export_overlay_images" , id_software= software.id, type="Boolean", default_value=False,required=True, index= 120, set_by_server=False)
    conn.add_software_parameter(name="number_of_resolutions", id_software=software.id, type="Number",
                                default_value=4, required=True, index=130, set_by_server=False)
    conn.add_software_parameter(name="result_file_name", id_software=software.id, type="String",
                                default_value="result_image", required=True, index=140, set_by_server=False)
