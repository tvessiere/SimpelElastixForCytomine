__author__ = "Vessiere Thomas <vessiere.thomas@hotmail.com>"
__Copyright__ = "Copyright 2010-2017 University of Liege, Belgium, http://www.cytomine.be/"


import os
import tempfile

if __name__ == "__main__":
    import cytomine

    # Connect to cytomine, edit connection values

    cytomine_host = "localhost-core:8080"
    Pk = '574a02a6-6f62-40f3-9408-82b77807d5b2'
    Prk = '37ee0493-f881-431c-bfea-e1123fda9b3e'
    #id_project = 19941904

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
    software = conn.add_software("SimpleElastixV25","createRabbitJobWithArgsService","download","/root/miniconda2/envs/cytomine/bin/python /software_router/algo/simple_elastix/get_and_move.py " +
                                                                                                     "--cytomine_host $host " +
                                                                                                     "--cytomine_public_key $publicKey " +
                                                                                                     "--cytomine_private_key $privateKey " +
                                                                                                     "--cytomine_id_software $cytomine_id_software " +
                                                                                                     "--cytomine_working_path /software_router/algo/simple_elastix/ " +
                                                                                                     "--cytomine_id_project $cytomine_id_project " +
                                                                                                     "--fix_image_id $fix_image_id " +
                                                                                                     "--mov_image_id $mov_image_id " +
                                                                                                     "--nb_iterations $nb_iterations " +
                                                                                                     "--nb_spatialsampels $nb_spatial_sample " +
                                                                                                     "--cytomine_storage_id $storage " +
                                                                                                     "--annotation_fix_id $annotation_fix_id " +
                                                                                                     "--annotation_moving_id $annotation_moving_id " +
                                                                                                     "--cytomine_upload $cytomine_upload " +
                                                                                                     "--export_overlay_images $export_overlay_images " +
                                                                                                     "--result_file_name $result_file_name " +
                                                                                                     "--number_of_resolution $number_of_resolution "
                                 )


    conn.add_software_parameter(name="cytomine_id_software",id_software=software.id,type= "Number",default_value= 0,required= True, index=100, set_by_server=True)
    conn.add_software_parameter(name="cytomine_id_project",id_software=software.id,type= "Number",default_value= 0,required= True, index=110, set_by_server=True)

    conn.add_software_parameter(name="fix_image_id", type="Domain", id_software=software.id, default_value=None,required=False,index=10,set_by_server=False,uri="/api/project/$currentProject$/imageinstance.json",uriPrintAttribut="instanceFilename",uriSortAttribut="instanceFilename")
    conn.add_software_parameter(name="mov_image_id",type="Domain", id_software=software.id, default_value=None,required=False,index=20,set_by_server=False,uri="/api/project/$currentProject$/imageinstance.json",uriPrintAttribut="instanceFilename",uriSortAttribut="instanceFilename")
    conn.add_software_parameter(name="nb_iterations",id_software=software.id,type= "Number",default_value=512,required=True,index=30,set_by_server=False)
    conn.add_software_parameter(name="nb_spatial_sample",id_software=software.id,type= "Number",default_value=2048,required=True,index=40,set_by_server=False)
    conn.add_software_parameter(name="storage",type="Domain", id_software=software.id, default_value=None,required=False,index=50,set_by_server=False,uri="/api/storage.json",uriPrintAttribut="name",uriSortAttribut="name")
    conn.add_software_parameter(name="annotation_fix_id",id_software=software.id,type= "Number",default_value=49526,required=False,index=60,set_by_server=False)
    conn.add_software_parameter(name="annotation_moving_id",id_software=software.id,type= "Number",default_value=49888,required=False,index=70,set_by_server=False)
    conn.add_software_parameter(name="export_overlay_images" , id_software= software.id, type="Boolean", default_value=False,required=True, index= 120, set_by_server=False)
    conn.add_software_parameter(name="result_file_name", id_software=software.id, type="String",default_value="result_Simple_Elastix.png",required=True, index=130, set_by_server=False)
    conn.add_software_parameter(name="number_of_resolution", id_software=software.id, type="Number", default_value=4, required=True, index=140, set_by_server=False)