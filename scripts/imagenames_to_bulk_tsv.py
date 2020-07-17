import csv


"""
Proposed layout for testing.

2 Experiments (A and B). ExpA = 3D-SIM (tif), ExpB = RNA-FISH (dv).

2 Datasets for ExpA. Dataset Names = AC16_Rep1, AC16_Rep2.

Example file names for ExpA = AC16_Rep1_18d24h37d2h_HNRNPC488_NUP594_01_SIR_THR_ALN.tif,
        AC16_Rep2_18d24h_HNRNPC488_NUP594_01_SIR_THR_ALN.tif.

10 Datsets for ExpB. Dataset Names = AC16_Rep1, AC16_Rep2, AC16_Rep3, AC16_Rep4,
    U2OS_Rep1, U2OS_Rep2, U2OS_Rep3, U2OSNr1d1KO_Rep1, U2OSNr1d1KO_Rep2, U2OSNr1d1KO_Rep3.

Example file names for ExpB = AC16_T18d24h_Rep1_PoorProbeChan1_Cry2Chan2_DAPIChan3_1.dv, AC16_T18d24h_Rep2_PoorProbeChan1_Cry2Chan2_DAPIChan3_1.dv.

"""

project_name = "Project:name:idr0070-kerwin-hdbr/experimentA/"
path_to_data = "/uod/idr/filesets/idr0070-kerwin-hdbr"

pdi = {
    "experimentA": {
        "Rep1_HNRNPC_NUP": [],
        "Rep2_HNRNPC_NUP": [],
        "Rep2_H3K4M_H3K27M": [],
        "Rep2_POLS2P_H3K9M": [],
    },
    # NB REV-ERBα is NR1D1
    "experimentB": {
        "REV-ERBα_AC16": [],
        "CRY2_AC16": [],
        "TP53_AC16": [],
        "AC16_Rep4": [],
        "REV-ERBα_U2OS": [],
        "Nr1d1KO_U2OS": [],
    },
}

project_names = "idr0089-experimentA-filePaths.tsv"

image_names = []
with open("image_names.txt", mode="r") as img_names:
    for line in img_names:
        names = [name.strip() for name in line.split(" ")]
        names = [n for n in names if len(n) > 0]
        image_names.extend(names)

print(f"Found {len(image_names)} image names")

for name in image_names:
    project = None
    dataset = None
    if name.endswith(".tif"):
        project = "experimentA"
        if "HNRNPC" in name and "Rep1" in name:
            dataset = "Rep1_HNRNPC_NUP"
        elif "HNRNPC" in name and "Rep2" in name:
            dataset = "Rep2_HNRNPC_NUP"
        elif "H3K4M" in name:
            dataset = "Rep2_H3K4M_H3K27M"
        elif "POLS2P" in name:
            dataset = "Rep2_POLS2P_H3K9M"
    elif name.endswith(".dv"):
        project = "experimentB"
        if "Nr1d1KO" in name:
            dataset = "Nr1d1KO_U2OS"
        elif "U2OS" in name and "Nr1d1" in name:
            # Nr1d1 == REV-ERBα
            dataset = "REV-ERBα_U2OS"
        elif "AC16_" in name:
            if "Nr1d1" in name:
                dataset = "REV-ERBα_AC16"
            elif "Tp53" in name:
                dataset = "TP53_AC16"
            elif "Cry2" in name:
                dataset = "CRY2_AC16"
    if project is not None and dataset is not None:
        pdi[project][dataset].append(name)
    else:
        print("Not assigned", name)

for project, datasets in pdi.items():
    with open(f"idr0089-{project}-filePaths.tsv", mode="w") as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter="\t")
        for dataset, images in datasets.items():
            for name in images:
                # Project:name:idr0070-kerwin-hdbr/experimentA/Dataset:name:EFR3A-CS23	/uod/idr/filesets/idr0070-kerwin-hdbr/20200214-ftp/HDBR_EFR3A_ISH/968,2,body,CS23,28_2015-11-18 15_35_09.scn	HDBR_EFR3A_ISH/968,2,body,CS23,28_2015-11-18 15_35_09.scn
                idr = "idr0089-fischl-coldtemp"
                target = f"Project:name:{idr}/{project}/Dataset:name:{dataset}"
                image_path = f"/uod/idr/filesets/{idr}/20200625-ftp/{name}"
                tsv_writer.writerow([target, image_path, name])
