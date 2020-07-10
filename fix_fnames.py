#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import logging
logging.basicConfig(filename='renaming.log', level=logging.DEBUG)

import datetime
from xml.dom.minidom import parse

# get the correct date my subtracting the raw date (as fractional days)
# by Jan 1 1900, the excel format
beginning_date = datetime.datetime(1900, 1, 1)
def excel_date_to_datetime(raw_excel_date):
    dt = datetime.timedelta(days=raw_excel_date)
    return beginning_date + dt

def load_date_from_xml(base):
    tree = parse(base + '.modd')
    date_elem = tree.getElementsByTagName('real')[0]
    date_raw = float(date_elem.firstChild.data)
    return excel_date_to_datetime(date_raw)

def rename_file(base, date):
    old_path = base + ".avi"

    new_base = date.strftime("%Y-%m-%d %Hh%Mm%Ss") + ".avi"
    new_path = os.path.join(os.path.split(base)[0], new_base)

    logging.info("Renaming \'{}\' to \'{}\'"
            .format(old_path, new_path))

    os.rename(old_path, new_path)

def main():
    # .avi files
    avis = glob.glob("*.avi")
    avis.extend(glob.glob("**/*.avi"))

    # base names from those files
    base_names = [avi_file.split('.')[0] for avi_file in avis]
    logging.info("Found these base names for videos: " + str(base_names))

    for base in base_names:
        date = load_date_from_xml(base)
        logging.info("Determined date for \'{}\' to be \'{}\'"
                .format(base + ".avi", date)) 

        # now append the metadata
        rename_file(base, date)

if __name__ == "__main__":
    main()

