import os
import tempfile

if __name__ == "__main__":
    import cytomine

    # Connect to cytomine, edit connection values

    cytomine_host = "demo.cytomine.be"
    Pk = 'cbfe0e04-3fd7-4a7f-a13c-b86685ecb570'
    Prk = '1e1cb3e8-ed0a-434d-b049-3a48552429c7'
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

    software = conn.add_software("SE_TranslationAffine", "ImageAlignment")
    conn.add_software_parameter(name="cytomine_id_software",id_software=software.id,type = "Number",required=True,)

    addSoftwareProject = conn.add_software_project(id_project, software.id)

