import json  # import the json library.

def versioning():
    with open("variables.json", "r") as f:  # read the json file
        variables = json.load(f)

    minor = variables["minor"]  # To get the value currently stored
    incremental = variables["incremental"]  # To get the value currently stored
    major = variables["major"]  # To get the value currently stored
    if incremental == 0:
        temp = incremental + 1
    else:
        temp = incremental + 1
    for i in range(temp):
        if i == incremental:
            if variables["incremental"] == 9:
                variables["minor"] +=1
                variables["incremental"] = 0
            if variables["minor"] == 10:
                variables["major"] += 1
                variables["minor"] = 0
                variables["incremental"] = 0
            variables["incremental"] +=1
            break
    version = str(variables["major"])+"."+str( variables["minor"])+"."+str(variables["incremental"])
    variables["version"] = version
    with open("variables.json", "w") as f:  # write back to the json file
        json.dump(variables, f)
    version = str(str(variables["major"])+"."+str(variables["minor"])+"."+str(variables["incremental"]))
    print(version)

versioning()
