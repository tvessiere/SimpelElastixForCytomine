import os
import tempfile

if __name__ == "__main__":
    import cytomine

    # Connect to cytomine, edit connection values

    cytomine_host = "demo.cytomine.be"
    Pk = 'cbfe0e04-3fd7-4a7f-a13c-b86685ecb570'
    Prk = 'XXXXXXX'
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
    software = conn.add_software("SE_TranslationAffine2","createRabbitJobWithArgsService","download","python algo/Simple_Elastix/WorkFlowSE.py"+
                                                                                                     "--cytomine_host $host" +
                                                                                                     "--cytomine_public_key $publicKey" +
                                                                                                     "--cytomine_private_key $privateKey" +
                                                                                                     "--cytomine_base_path /api/" +
                                                                                                     "--cytomine_id_software $cytomine_id_software" +
                                                                                                     "--cytomine_working_path algo/Simple_Elastix/images" +
                                                                                                     "--cytomine_id_project $cytomine_id_project" +
                                                                                                     "--id_fix_image $id_fix_image" +
                                                                                                     "--id_mov_image $id_mov_image" +
                                                                                                     "--nb_iterations $nb_iterations" +
                                                                                                     "--nb_spatialsampels $nb_spatialsampels")

    #conn.add_software_parameter(name="cytomine_id_software",id_software=software.id,type = "Number",default_value=None,required=True,index=1,set_by_server=True)
    #conn.add_software_parameter(name="cytomine_id_project",id_software=software.id,type= "Number",default_value=None,required=True,index=10,set_by_server=True)

    conn.add_software_parameter(name="id_fix_image",id_software=software.id,type= "Number",default_value=None,required=True,index=20,set_by_server=False)
    conn.add_software_parameter(name="id_mov_image",id_software=software.id,type= "Number",default_value=None,required=True,index=30,set_by_server=False)
    conn.add_software_parameter(name="nb_iterations",id_software=software.id,type= "Number",default_value=None,required=True,index=40,set_by_server=False)
    conn.add_software_parameter(name="nb_spatialsampels",id_software=software.id,type= "Number",default_value=None,required=True,index=50,set_by_server=False)

    """conn.delete_software_parameter(19957884)
    conn.delete_software_parameter(19957890)
    conn.delete_software_parameter(19957896)
    conn.delete_software_parameter(19957902)"""



