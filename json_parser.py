

def load_json(path):
    with open(path, 'r') as file:
        content = file.readlines()
    jsonData = [(obj.rstrip()).lstrip() for obj in content[1:-1]]
    return jsonData


def from_str(val):
    val = val.strip()
    if val.isdigit():
        try:
            val = int(val)
        except ValueError:
            val = float(val)
    else:
        val = bool(val)
    return val


def rlstrip(data, chars='", '):
    return (data.rstrip(chars)).lstrip(chars).strip()


def get_key(data):
    return data.split(':')[0]


def parse(jsonData):
    jsonDict = {}
    length = len(jsonData)
    inner_ind = 0
    while inner_ind < length:

        if jsonData[inner_ind][-1] == '{':
            key = rlstrip(get_key(jsonData[inner_ind]))
            jsonDict[key], ind = parse(jsonData[inner_ind+1:])
            inner_ind = inner_ind + ind + 1
            continue

        elif jsonData[inner_ind][-1:].strip() == '}' or jsonData[inner_ind][-2:] == '},':
            return jsonDict, inner_ind + 1

        elif jsonData[inner_ind][-1] == '[':
            key = rlstrip(get_key(jsonData[inner_ind]))
            val = []
            inner_ind += 1

            while jsonData[inner_ind][-2:] != '],':
                v = jsonData[inner_ind].rstrip(',')
                if v == rlstrip(v, chars='"'):
                    v = from_str(v)
                else:
                    v = rlstrip(jsonData[inner_ind])
                val.append(v)
                inner_ind += 1

            jsonDict[key] = val
            inner_ind += 1
            continue

        elif jsonData[inner_ind][-2:] == '",' or jsonData[inner_ind][-1:] == '"':
            key, val = jsonData[inner_ind].split(':')
            key = rlstrip(key)
            val = rlstrip(val)
            jsonDict[key] = val
            inner_ind += 1
            continue

        else:
            key, val = jsonData[inner_ind].split(':')
            key = rlstrip(key)
            val = rlstrip(val)
            val = from_str(val)
            jsonDict[key] = val
            inner_ind += 1

        # raise Exception('I forgot to parse smth')

    return jsonDict, inner_ind

'''
if __name__ == '__main__':
    jsonData = load_json('data.json')
    json_dict, _ = parse(jsonData)
    print(json_dict)
'''
