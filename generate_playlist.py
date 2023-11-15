#!/usr/bin/env python3

from datetime import date, datetime
import os
import re
import shutil

CUR_DIR = os.path.dirname(__file__)
SRC_DIR = CUR_DIR + "/FROgehtaus Originalfiles"  # path to source directory
TGT_DIR = CUR_DIR + "/FROgehtaus for PL"         # path to target directory
TGT_NAME = "FROgehtaus"                          # basename of copied file
MAX_FILES = 10                                   # max files to copy
FALLBACK = SRC_DIR + "/Radio FRO beeps.mp3"      # file to copy to match MAX_FILES


def generate_playlist(src_dir: str, start_date: date = date.today(), max_files: int = MAX_FILES) -> list[str]:
    resre = []
    respr = []
    items = map(lambda f: os.path.join(src_dir, f), os.listdir(src_dir))
    files = sorted(filter(lambda f: os.path.isfile(f), items))
    for file in files:
        match = re.search(r'\d{4}_\d{2}_\d{2}', os.path.basename(file))
        if match is not None:
            fdate = datetime.strptime(match.group(), '%Y_%m_%d').date()
            if fdate >= start_date:
                if re.search(r'^P_\d{4}_\d{2}_\d{2}', os.path.basename(file)):
                    respr.append(file)
                else:
                    resre.append(file)
    res = respr + resre
    return res[0:max_files]


def copy_files(src_names: [str], tgt_dir: str, tgt_name: str):
    for idx, fname in enumerate(src_names):
        sfx = os.path.splitext(fname)[-1].lower()
        tgt = os.sep.join([tgt_dir, "{}{}{}".format(tgt_name, idx+1, sfx)])
        shutil.copyfile(fname, tgt)
        print(f"Copied {fname} to {tgt}")


playlist = generate_playlist(SRC_DIR)

# add fallback file if list is too short
delta = MAX_FILES - len(playlist)
if delta > 0:
    for i in range(delta):
        playlist.append(FALLBACK)

copy_files(playlist, TGT_DIR, TGT_NAME)
