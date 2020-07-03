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
    "experimentA": {"AC16_Rep1": [], "AC16_Rep2": [],},
    "experimentB": {
        "AC16_Rep1": [],
        "AC16_Rep2": [],
        "AC16_Rep3": [],
        "AC16_Rep4": [],
        "U2OS_Rep1": [],
        "U2OS_Rep2": [],
        "U2OS_Rep3": [],
        "U2OSNr1d1KO_Rep1": [],
        "U2OSNr1d1KO_Rep2": [],
        "U2OSNr1d1KO_Rep3": [],
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
        for rep in ["AC16_Rep1", "AC16_Rep2"]:
            if name.startswith(rep):
                dataset = rep
    elif name.endswith(".dv"):
        project = "experimentB"
        if "Nr1d1KO" in name:
            for r in ["_Rep1", "_Rep2", "_Rep3"]:
                if r in name:
                    dataset = "U2OSNr1d1KO" + r
        elif "U2OS" in name:
            for r in ["_Rep1", "_Rep2", "_Rep3"]:
                if r in name:
                    dataset = "U2OS" + r
        elif "AC16_" in name:
            for r in range(1, 5):
                if f"_Rep{r}" in name:
                    dataset = f"AC16_Rep{r}"
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
