import os
import tempfile

if __name__ == "__main__":
    import cytomine

    # Connect to cytomine, edit connection values

    cytomine_host = "demo.cytomine.be"
    Pk = 'cbfe0e04-3fd7-4a7f-a13c-b86685ecb570'
    Prk = 'XXXXX'
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

    software = conn.get_software(19953189)
    conn.add_software_parameter(name="cytomine_id_software",id_software=software.id,type = "Number",default_value=None,required=True,index=1,set_by_server=True)
    conn.add_software_parameter(name="cytomine_id_project",id_software=software.id,type= "Number",default_value=None,required=True,index=10,set_by_server=True)
    conn.add_software_parameter(name="cytomine_id_fix_image",id_software=software.id,type= "Number",default_value=None,required=True,index=20,set_by_server=False)
    conn.add_software_parameter(name="cytomine_id_mov_image",id_software=software.id,type= "Number",default_value=None,required=True,index=30,set_by_server=False)
    conn.add_software_parameter(name="cytomine_nbiterations",id_software=software.id,type= "Number",default_value=None,required=True,index=40,set_by_server=False)
    conn.add_software_parameter(name="cytomine_nbspatialsampels",id_software=software.id,type= "Number",default_value=None,required=True,index=50,set_by_server=False)

    addSoftwareProject = conn.add_software_project(id_project, software.id)


