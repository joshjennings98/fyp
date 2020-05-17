# loadConfig.py
from networkGenerator import Network
from neuronGenerator import genNeurons
from mathParser import NumericStringParser
import random
import re

random.seed(123)
rand = random.random
nsp = NumericStringParser()

def parseParam(param : str) -> str:
    """
    Takes an unparsed string <param> containing a parameter definition and converts it to a string in the form:

    "name : value type : value : deviceType"
    """
    param = param.replace(" ", "") #.replace("R", f"{rand()}")
    param = list(filter(lambda x: x != '', re.split(r'[=\s:]\s*', param)))
    p, propOrState = (1, "p") if param[0] == "property" else (0, "s")
    
    name = param[p].replace(' ', '')
    vtype = "float" if "." in param[p + 1] else "uint32_t"
    value = param[p + 1].replace('r', '')
    deviceType = propOrState

    return f"{name} : {vtype} : {value} : {deviceType}"

def makeFromConfig(filename : str, printNetwork : bool = False) -> None:
    """
    Loads config file located at <filename> and parses the human readable information into the representations used by the network generator.

    A network is then generated according to the contents of the config file.

    Also optionally prints the final network (not recomended for large networks).
    """
    allParams = []
    parameters = {}

    with open(filename, 'r') as f:
        # Split up parameters into lists
        x = f.read().split(';')
        x = list(map(lambda x: x.replace('\n', "").split(':'), x))
        x = list(map(lambda y: list(map(lambda z: z.split(','), y)), x))
        x = list(filter(lambda x: x != [['']], x))
        # Load parameters into a dictionary
        for param in x:
            parameters[param[0][0]] = param[1]
        for x in parameters:
            # Since you can have multiple parameters, account for that
            if "parameter" in x:
                params = list(map(lambda el: parseParam(el), parameters[x]))
                p = params[:-4]

                """
                newP = []
                r = rand()
                for l in list(map(lambda x: x.replace(' ', "").split(':'), p)):
                    l[2] = str(eval(l[2].replace("R", f"{r}")))
                    newP.append(" : ".join(l))
                """

                meta = list(map(lambda x: x.replace(' ', "").split(':')[2], params[-4:]))
                allParams.append((p, float(meta[0]), int(meta[1]), float(meta[2]), meta[3]))
            # Turn strings into form "param : what to do to param : property"
            if x =="reset":
                parameters[x] = list(map(lambda x: x.replace(" ", " : "), parameters[x]))
            if x =="init":
                parameters[x] = list(map(lambda x: x.replace(" ", "").replace("=", " : = : "), parameters[x]))
            # Name had a space in front of it sometimes so remove that
            if x == "name":
                parameters[x] = list(map(lambda x: x.replace(" ", ""), parameters[x]))

    # Check parameter fractions add up to 1
    frac = sum(map(lambda p: p[1], allParams))
    if frac < 1.0:
        raise Exception("All neurons need to have parameters, check the fractions of all the parameters add up to 1.0")    
    elif frac > 1.0:
        raise Exception("You cannot have the total fraction of parameters greater than 1.0")

    # Generate network
    neurons = genNeurons(int(parameters["number"][0]), allParams) 
    network = Network(parameters["name"][0], parameters["equations"], parameters["threshold"][0], neurons, parameters["reset"], parameters["init"], int(parameters["maxt"][0]), parameters["type"][0])
    
    if printNetwork:
        network.printGraph()