import re
import sys
import csv

InstrumentIDs = {"HWI-M[0-9]{4}$" : ["MiSeq"],
        "HS2000" : ["HiSeq 2000"],
        "HWUSI" : ["Genome Analyzer IIx"],
        "M[0-9]{5}$" : ["MiSeq"],
        "HWI-C[0-9]{5}$" : ["HiSeq 1500"],
        "C[0-9]{5}$" : ["HiSeq 1500"],
        "HWI-D[0-9]{5}$" : ["HiSeq 2500"],
        "D[0-9]{5}$" : ["HiSeq 2500"],
        "J[0-9]{5}$" : ["HiSeq 3000"],
        "K[0-9]{5}$" : ["HiSeq 3000","HiSeq 4000"],
        "E[0-9]{5}$" : ["HiSeq X"],
        "NB[0-9]{6}$": ["NextSeq"],
        "NS[0-9]{6}$" : ["NextSeq"],
        "MN[0-9]{5}$" : ["MiniSeq"],
        "HWI-ST[0-9]{3}" : ["HiSeq HWI-ST?"],
        "A[0-9]{5}" : ["NovaSeq?"],
        "A[0-9]{5}" : ["NovaSeq?"],
        }

#FCIDs = {"C[A-Z,0-9]{4}ANXX$" : (["HiSeq 1500", "HiSeq 2000", "HiSeq 2500"], "High Output (8-lane) v4 flow cell"),
#         "C[A-Z,0-9]{4}ACXX$" : (["HiSeq 1000", "HiSeq 1500", "HiSeq 2000", "HiSeq 2500"], "High Output (8-lane) v3 flow cell"),
#         "C[A-Z,0-9]{4}ACXX_[0-9]{1}$" : (["HiSeq 1000", "HiSeq 1500", "HiSeq 2000", "HiSeq 2500"], "High Output (8-lane) v3 flow cell"),
#         "H[A-Z,0-9]{4}ADXX$" : (["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v1 flow cell"),
#         "H[A-Z,0-9]{4}BCXX$" : (["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v2 flow cell"),
#         "H[A-Z,0-9]{4}BCXY$" : (["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v2 flow cell"),

FCIDs = {"C[A-Z,0-9]{4}ANXX$" : (["HiSeq 1000;1500;2000;2500"], "High Output (8-lane) v4 flow cell"),
         "C[A-Z,0-9]{4}ACXX$" : (["HiSeq 1000;1500;2000;2500"], "High Output (8-lane) v3 flow cell"),
         "C[A-Z,0-9]{4}ACXX_[0-9]{1}$" : (["HiSeq 1000;1500;2000;2500?"], "High Output (8-lane) v3 flow cell"), # Many UK samples have this pattern
         "C[A-Z,0-9]{5}ACXX_[0-9]{1}$" : (["HiSeq 1000;1500;2000;2500?"], "High Output (8-lane) v3 flow cell"), # Many Canadian samples have this pattern
         "H[A-Z,0-9]{4}ADXX$" : (["HiSeq 1000;1500;2000;2500"], "Rapid Run (2-lane) v1 flow cell"),
         "H[A-Z,0-9]{4}BCXX$" : (["HiSeq 1000;1500;2000;2500"], "Rapid Run (2-lane) v2 flow cell"),
         "H[A-Z,0-9]{4}BCXY$" : (["HiSeq 1000;1500;2000;2500"], "Rapid Run (2-lane) v2 flow cell"),
         "H[A-Z,0-9]{4}BBXX$" : (["HiSeq 4000"], "(8-lane) v1 flow cell"),
         "H[A-Z,0-9]{4}BBXY$" : (["HiSeq 4000"], "(8-lane) v1 flow cell"),
         "H[A-Z,0-9]{4}CCXX$" : (["HiSeq X"], "(8-lane) flow cell"),
         "H[A-Z,0-9]{4}CCXY$" : (["HiSeq X"], "(8-lane) flow cell"),
         "H[A-Z,0-9]{4}ALXX$" : (["HiSeq X"], "(8-lane) flow cell"),
         "H[A-Z,0-9]{4}BGXX$" : (["NextSeq"], "High output flow cell"),
         "H[A-Z,0-9]{4}BGXY$" : (["NextSeq"], "High output flow cell"),
         "H[A-Z,0-9]{4}BGX2$" : (["NextSeq"], "High output flow cell"),
         "H[A-Z,0-9]{4}AFXX$" : (["NextSeq"], "Mid output flow cell"),
         "A[A-Z,0-9]{4}$" : (["MiSeq"], "MiSeq flow cell"),
         "B[A-Z,0-9]{4}$" : (["MiSeq"], "MiSeq flow cell"),
         "D[A-Z,0-9]{4}$" : (["MiSeq"], "MiSeq nano flow cell"),
         "G[A-Z,0-9]{4}$" : (["MiSeq"], "MiSeq micro flow cell"),
         "H[A-Z,0-9]{4}DMXX$" : (["NovaSeq S2"], "S2 flow cell"),
         "H[A-Z,0-9]{4}DSXX$" : (["NovaSeq S4"], "S4 flow cell")}

def get_instrument(instrument_id):
    result = []
    for key in InstrumentIDs:
        if re.search(key, instrument_id): 
            result.extend(InstrumentIDs[key])
    return result

def get_flow_cell(flow_cell_id):
    result = []
    for key in FCIDs:
        if re.search(key, flow_cell_id): 
            result.extend(FCIDs[key][0])
    return result

reader = csv.DictReader(sys.stdin)

print("sample,group,read_id,instrument,flow_cell")

for row in reader:
     sample = row['sample']
     read_id = row['read_id']
     group = row['group']
     fields = read_id.split(":")
     if group in ["UK", "CAN"] and len(fields) == 5:
         instrument_id = ""
         flow_cell_id = fields[0]
         if flow_cell_id.startswith("HS2000"):
             instrument_id = flow_cell_id
     elif len(fields) >= 3:
         instrument_id = fields[0]
         flow_cell_id = fields[2]
     instrument_matches = set(get_instrument(instrument_id))
     flow_cell_matches = set(get_flow_cell(flow_cell_id))
     if len(flow_cell_matches) > 1 and "MiSeq" in flow_cell_matches:
         flow_cell_matches.remove("MiSeq")
     instrument_str = "-".join(instrument_matches)
     flow_cell_str = "-".join(flow_cell_matches)
     if instrument_str == "":
         instrument_str = "UNKNOWN"
     if flow_cell_str == "":
         flow_cell_str = "UNKNOWN"
     if instrument_str == "UNKNOWN":
         instrument_str = flow_cell_str
     print(f'{sample},{group},{read_id},{instrument_str},{flow_cell_str}')
