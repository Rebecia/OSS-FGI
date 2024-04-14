import json
import os

from google.protobuf.json_format import MessageToJson
from google.protobuf.text_format import Merge


def json_loads(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts=False):
    if isinstance(data, str):
        return data

    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items()  # changed to .items() for python 2.7/3
        }

    # python 3 compatible duck-typing
    # if this is a unicode string, return its string representation
    if str(type(data)) == "<type 'unicode'>":
        return data.encode('utf-8')

    # if it's anything else, return it in its original form
    return data


def read_json_from_file(filepath):
    try:
        import json
    except ImportError as e:
        raise Exception("'json' module not available. Please install.")
    try:
        with open(filepath, "r") as f:
            return json_loads(f.read())
    except Exception as e:
        raise Exception("Failed to load json data from file %s: %s" % (filepath, str(e)))


def get_file_type(filepath):
    if os.path.isfile(filepath):
        file_type = 'FILE'
    elif os.path.isdir(filepath):
        file_type = 'DIR'
    elif os.path.islink(filepath):
        file_type = 'LINK'
    else:
        file_type = 'UNKNOWN'
    return file_type


def read_file_lines(filename):
    try:
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                yield line
            f.close()
    except Exception as e:
        raise Exception("Failed to read file %s: %s" % (filename, str(e)))


def read_from_csv(filename, skip_header=False):
    import csv
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        if skip_header:
            next(reader)
        for row in reader:
            if len(row) and not row[0].startswith('#'):
                yield row


def write_json_to_file(filepath, data_json, indent=0):
    try:
        import json
    except ImportError as e:
        raise Exception("'json' module not available. Please install.")
    try:
        with open(filepath, "w+") as f:
            json.dump(data_json, f, indent=indent)
    except Exception as e:
        raise Exception("Failed to dump json content to file %s: %s" % (filepath, str(e)))


def write_to_file(filename, data):
    try:
        with open(filename, 'w+') as f:
            f.write("%s" % (data))
    except Exception as e:
        raise Exception("Failed to write to file %s: %s" % (filename, str(e)))


def read_proto_from_file(proto, filename, binary=True):
    if binary:
        f = open(filename, "rb")
        proto.ParseFromString(f.read())
        f.close()
    else:
        f = open(filename, "r")
        Merge(f.read(), proto)
        f.close()


def write_dict_to_file(dict_data, outfile):
    import json
    with open(outfile, 'w+') as of:
        json.dump(dict_data, of, indent=4)


def write_proto_to_file(proto, filename, binary=True):
    if binary:
        f = open(filename, "wb")
        f.write(proto.SerializeToString())
        f.close()
    else:
        f = open(filename, "w")
        f.write(MessageToJson(proto))
        f.close()
