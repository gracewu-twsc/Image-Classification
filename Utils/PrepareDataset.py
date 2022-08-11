import os
import shutil
import io
import base64
from sklearn.model_selection import train_test_split


def GetDataSetList(DataSetPath,Dataset):
    for Path, Folders, Files in os.walk(DataSetPath):
        if (len(Files) > 0):
            FolderName = Path.split("/")[-1]
            Dataset[FolderName]={}
            Dataset[FolderName]['FileList'] = Files
            

def SplitDataSet(Dataset,RandomSeed=721):
    for FolderName in Dataset.keys():
        Dataset[FolderName]['train'], Dataset[FolderName]['valid'] = \
            train_test_split(Dataset[FolderName]['FileList'], train_size=0.7, random_state = RandomSeed)


def MakeTrainingDataSet(Source,Dataset):
    if os.path.exists(f"/{os.environ['DATA_MOUNT_PATH']}/dataset"):
        shutil.rmtree(f"/{os.environ['DATA_MOUNT_PATH']}/dataset")

    os.mkdir(f"/{os.environ['DATA_MOUNT_PATH']}/dataset")
    os.mkdir(f"/{os.environ['DATA_MOUNT_PATH']}/dataset/train")
    os.mkdir(f"/{os.environ['DATA_MOUNT_PATH']}/dataset/valid")
    for FolderName in Dataset.keys():
        for Type in ['train','valid']:
            os.mkdir(f"/{os.environ['DATA_MOUNT_PATH']}/dataset/{Type}/{FolderName}")
            for File in Dataset[FolderName][Type]:
                shutil.copy(f"{Source}/{FolderName}/{File}",f"/{os.environ['DATA_MOUNT_PATH']}/dataset/{Type}/{FolderName}/{File}")


def CountDataSet(Dataset):
    str="類別\t訓練資料量\t測試資料量\n"
    for FolderName in Dataset.keys():
        str+=f"{FolderName}\t"
        for Type in ['train','valid']:
            str+=f"{len(Dataset[FolderName][Type])}\t\t"
        str+="\n"
    return str


def FormateImage(OrgImage):
    Buffered = io.BytesIO()
    OrgImage.thumbnail((64, 64))
    OrgImage.save(Buffered, format="png")
    Buffered.seek(0)
    EncodeString = base64.b64encode(Buffered.read()).decode()
    return f'<img src="data:image/png;base64,{EncodeString}">'
