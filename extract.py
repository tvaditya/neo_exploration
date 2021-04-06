import csv
import json
import pathlib
from models import NearEarthObject, CloseApproach

def load_neos(neo_csv_path):
    infile = pathlib.Path(neo_csv_path)
    out_neos = list()
    # process the file and create the NEO
    with open(infile, 'r') as input:
        data = csv.DictReader(input)
        for row in data:
            out_neos.append(NearEarthObject(
                designation=row['pdes'], name=row['name'],
                diameter=row['diameter'], hazardous=row['pha']))
    return out_neos


def load_approaches(cad_json_path):
    # get the data from the json file
    infile = pathlib.Path(cad_json_path)
    with open(infile, 'r') as input:
        raw_data = json.load(input)

    # create a list of fields
    fields = list()
    # create a list of approaches with complete row data
    raw_approaches = list()
    # do the processing of data
    for item in raw_data:
        # find the dict with fields and values
        if item == 'fields':
            for item in raw_data[item]:
                fields.append(item)
        # find the dict with data and add them to approaches list
        if item == 'data':
            for list_item in raw_data[item]:
                raw_approaches.append(list_item)

    # helper to get the indexes of the fields in json file
    fields_dict = build_dict_of_fields(fields)
    # get a list of approaches based on the index of fields from raw_approaches
    approaches = build_list_of_approaches(raw_approaches, fields_dict)

    list_of_ca_objects = list()
    # finally we can create a list of CAs based on keywords
    for approach in approaches:
        list_of_ca_objects.append(
            CloseApproach(designation=approach['des'],
                          time=approach['cd'],
                          distance=approach['dist'],
                          velocity=approach['v_rel']))

    return list_of_ca_objects


def build_list_of_approaches(approaches, fields):
    o_approaches = list()
    # loop through approaches and create a dictionary for each approach
    # which is added to the list o_approaches
    for approach in approaches:
        # for each approach we need an empty set
        output_item = dict()

        # add these values to the dict

        output_item.update(v_rel=approach[fields['v_rel']])
        output_item.update(dist=approach[fields['dist']])
        output_item.update(cd=approach[fields['cd']])
        output_item.update(des=approach[fields['des']])

        # append the output_item to list with the formatted approach
        o_approaches.append(output_item)

    # return the whole list
    return o_approaches


def build_dict_of_fields(fields):

    if type(fields) == list:
        des = fields.index('des')
        cd = fields.index('cd')
        dist = fields.index('dist')
        v_rel = fields.index('v_rel')
    else:
        raise TypeError
    return {"des": des, "cd": cd, "dist": dist, "v_rel": v_rel}
