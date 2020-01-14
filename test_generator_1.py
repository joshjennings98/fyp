# test_generator.py
import random
from typing import List
rand=random.random

class Neuron(object):
    def __init__(self, name : str, params : List[str], connections : List[int]):
        self.name = name
        self.props = list(map(lambda el: el.replace(" ", "").split(":"), params)) # Strip white space and turn to a better list
        self.states = list(filter(lambda x: x[3] == "s", list(map(lambda el: el.replace(" ", "").split(":"), params))))
        self.connections = connections

class Network(object):
    def __init__(self, name : str, equations : List[str], threshold : str, neurons : List[Neuron], maxt : int = 100):
        self.name = name
        self.equations = equations
        self.threshold = threshold
        self.neurons = neurons
        self.maxt = maxt
        self.graph = self.makeGraph(self.neurons, self.name, self.maxt, self.equations, self.threshold)
    def makeGraph(self, neurons : List[str], name : str, maxt : int, equations : List[str], threshold : str) -> str:              
        deviceInstances = []
        edgeInstances = []
        
        properties = '\n        '.join(list(map(lambda el : "\t\t\t<Scalar name=\"%s\" type=\"%s\" default=\"%s\"/>" % (el[0], el[1], el[2]), neurons[0].props)))
        states = '\n        '.join(list(map(lambda el : "\t\t\t<Scalar name=\"%s\" type=\"%s\"/>" % (el[0], el[1]), neurons[0].states)))
        inits = '\n        '.join(list(map(lambda el : "\t\t\tdeviceState->%s = deviceProperties->%s; // Set initial %s value" % (el[0], el[0], el[0]), neurons[0].states)))
        assignments = '\n        '.join(list(map(lambda el : "\t\t\t\t%s &%s = deviceState->%s; // Assign %s" % (el[1], el[0], el[0], el[0]), neurons[0].states)))
        equations = '\n        '.join(list(map(lambda el : "\t\t\t\t%s;" % el, equations))) 

        for neuron in neurons:
            neuronProps = ','.join(list(map(lambda el : "\"%s\":%s" % (el[0], el[2]), neuron.props)))
            device = "\t\t\t<DevI id=\"%s\" type=\"neuron\"><P>%s</P></DevI>\n" % (neuron.name, neuronProps)
            deviceInstances.append(device)
            connections = []
            for connection in range(len(neuron.connections)): 
                if neuron.connections[connection] == 1: 
                    weight = -rand() if rand() > 0.8 else 0.5 * rand() # change to random value
                    edge = "\t\t\t<EdgeI path=\"%s:input-%s:fire\"><P>\"weight\":%s</P></EdgeI>\n" % (neurons[connection].name, neuron.name, weight)
                    connections.append(edge)
            edgeInstances.append("".join(connections))
        
        devices =  f"""<DeviceType id="neuron"> 
\t\t\t\t<Properties> 
\t\t\t\t\t<Scalar name="seed" type="uint32_t"/>
\t\t{properties} 
\t\t\t\t</Properties> 
\t\t\t\t<State> 
\t\t\t\t\t<Scalar name="rng" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="Icount" type="uint32_t"/>
\t\t\t\t\t<Scalar name="pendingFires" type="uint32_t"/>
\t\t\t\t\t<Scalar name="rts" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="t" type="uint32_t"/>
\t\t\t\t\t<Scalar name="I" type="float"/> 
\t\t{states}
\t\t\t\t</State> 
\t\t\t\t<OnInit>
\t\t\t\t\t<![CDATA[\t
\t\t\t\t\t// Initialise state values
\t\t{inits}\n
\t\t\t\t\tdeviceState->rng = deviceProperties->seed;
\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\tdeviceState->Icount=0;
\t\t\t\t\tdeviceState->pendingFires=1;
\t\t\t\t\tdeviceState->rts = RTS_FLAG_fire;		   
\t\t\t\t\t]]>
\t\t\t\t</OnInit> 
\t\t\t\t<InputPin name="input" messageTypeId="synapse"> 
\t\t\t\t\t<Properties> 
\t\t\t\t\t<Scalar name="weight" type="float"/> 
\t\t\t\t\t</Properties> 
\t\t\t\t\t<OnReceive>
\t\t\t\t\t\t<![CDATA[ 
\t\t\t\t\t\tdeviceState->Icount++;
\t\t\t\t\t\tif(message->fired){{
\t\t\t\t\t\t\tdeviceState->I += edgeProperties->weight; // fire at 1, (1 * weight) = weight so just add weight
\t\t\t\t\t\t}}\n
\t\t\t\t\t\tif(deviceState->Icount == deviceProperties->fanin){{
\t\t\t\t\t\t\tdeviceState->pendingFires++;
\t\t\t\t\t\t\tdeviceState->Icount=0;
\t\t\t\t\t\t}}
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnReceive> 
\t\t\t\t</InputPin> 
\t\t\t\t<OutputPin name="fire" messageTypeId="synapse"> 
\t\t\t\t\t<OnSend>
\t\t\t\t\t\t<![CDATA[ 
\t\t\t\t\t\t// Assignments
\t\t{assignments}
\t\t\t\t\t\tfloat &I = deviceState->I; // Assign I\n
\t\t{equations}\n
\t\t\t\t\t\tmessage->fired = {threshold};
\t\t\t\t\t\t
\t\t\t\t\t\tif(message->fired){{
\t\t\t{inits}
\t\t\t\t\t\t}}\n
\t\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\t\tdeviceState->Icount=0;
\t\t\t\t\t\tdeviceState->pendingFires--;
\t\t\t\t\t\tdeviceState->t++;
\t\t\t\t\t\tif(deviceState->t > graphProperties->max_t){{
\t\t\t\t\t\t\t*doSend=0;
\t\t\t\t\t\t\tfake_handler_exit(0);
\t\t\t\t\t\t}}
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnSend> 
\t\t\t\t</OutputPin> 
\t\t\t\t<ReadyToSend>
\t\t\t\t\t<![CDATA[ 
\t\t\t\t\t*readyToSend = (deviceState->pendingFires > 0) ? RTS_FLAG_fire : 0;
\t\t\t\t\t]]>
\t\t\t\t</ReadyToSend> 
\t\t\t</DeviceType>"""
        
        graph = f"""<?xml version='1.0'?>
<Graphs xmlns="https://poets-project.org/schemas/virtual-graph-schema-v3">
\t<GraphType xmlns="https://poets-project.org/schemas/virtual-graph-schema-v3" id="{name}"> 
\t\t<Properties> 
\t\t\t<Scalar name="max_t" type="uint32_t"/> 
\t\t\t<Scalar name="neuron_count" type="uint32_t"/> 
\t\t</Properties> 
\t\t<SharedCode>
\t\t\t<![CDATA[ 
\t\t\t#ifdef POETS_LEGACY_HAS_HANDLER_EXIT 
\t\t\t#define _do_handler_exit(code) handler_exit(code) 
\t\t\t#else 
\t\t\t#define _do_handler_exit(code) ((void)0) 
\t\t\t#endif\n
\t\t\t#define fake_handler_exit(code) \\
\t\t\t{{ \\
\t\t\t\tif((code)==0){{ \\
\t\t\t\t\thandler_log(0, "_HANDLER_EXIT_SUCCESS_9be65737_"); \\
\t\t\t\t}}else{{ \\
\t\t\t\t\thandler_log(0, "_HANDLER_EXIT_FAIL_9be65737_"); \\
\t\t\t\t}} \\
\t\t\t\t_do_handler_exit(code); \\
\t\t\t}}
\t\t\tuint32_t urng(uint32_t &state)
\t\t\t{{
\t\t\t\tstate = state*1664525+1013904223;
\t\t\t\treturn state;
\t\t\t}}\n
\t\t\t// Worlds crappiest gaussian
\t\t\tfloat grng(uint32_t &state)
\t\t\t{{
\t\t\t\tuint32_t u=urng(state);
\t\t\t\tint32_t acc=0;
\t\t\t\tfor(unsigned i=0;i<8;i++){{
\t\t\t\tacc += u&0xf;
\t\t\t\tu=u>>4;
\t\t\t\t}}
\t\t\t\t// a four-bit uniform has mean 7.5 and variance ((15-0+1)^2-1)/12 = 85/4
\t\t\t\t// sum of four uniforms has mean 8*7.5=60 and variance of 8*85/4=170
\t\t\t\tconst float scale=0.07669649888473704; // == 1/sqrt(170)
\t\t\t\treturn (acc-60.0f) * scale;
\t\t\t}} 
\t\t\t]]>
\t\t</SharedCode> 
\t\t<MessageTypes> 
\t\t\t<MessageType id="synapse"> 
\t\t\t\t<Message> 
\t\t\t\t\t<Scalar name="fired" type="int8_t"/> 
\t\t\t\t</Message>
\t\t\t</MessageType> 
\t\t</MessageTypes> 
\t\t<DeviceTypes>
\t\t\t{devices}
\t\t</DeviceTypes> 
\t</GraphType> 
\t<GraphInstance id="{name}_output" graphTypeId="{name}"> 
\t\t<Properties> 
\t\t\t"max_t":{maxt},
\t\t\t"neuron_count":{len(deviceInstances)}
\t\t</Properties> 
\t\t<DeviceInstances>\t\t
{"".join(deviceInstances)}\t\t</DeviceInstances> 
\t\t<EdgeInstances> 
{"".join(edgeInstances)}\t\t</EdgeInstances> 
\t</GraphInstance> 
</Graphs>"""
        return graph
    def saveGraph(self):
        filename = "%s.xml" % self.name
        file = open(filename, "w") 
        file.writelines(self.graph) 
        file.close()
        print(self.graph)
        print("Graph saved as:", filename)

if __name__ == "__main__":
    
    equations = [
        "v = 0.04 * v * v + 5 * v + 140 - u + I",
        "u = a * (b * v - u)"
    ]

    neurons1 = [ # Props are "name : type : value : <property p or state s>"
        Neuron("n_0", [
                f"u : float : {-65+15*rand()*rand()} : s", 
                f"v : float : {8-6*rand()*rand()} : s", 
                "a : float : 0.02 : s", 
                "b : float : 0.2 : s",             
                "fanin : uint32_t : 2 : p",             
                #"Ir : float : 1 : p",
            ], [1, 0, 1, 0, 0]),
        Neuron("n_1", [
                f"u : float : {-65+15*rand()*rand()} : s", 
                f"v : float : {8-6*rand()*rand()} : s",       
                "a : float : 0.02 : s", 
                "b : float : 0.2 : s",             
                "fanin : uint32_t : 2 : p",             
                #"Ir : float : 1 : p",
            ], [0, 0, 0, 1, 1]),
        Neuron("n_2", [
                "u : float : 2 : s", 
                "v : float : -65 : s",        
                f"a : float : {0.02+0.08*rand()} : s", 
                f"b : float : {0.25-0.05*rand()} : s",             
                "fanin : uint32_t : 2 : p",             
                #"Ir : float : 1 : p",
            ], [0, 1, 0, 1, 0]),
        Neuron("n_3", [
                "u : float : 2 : s", 
                "v : float : -65 : s",        
                f"a : float : {0.02+0.08*rand()} : s", 
                f"b : float : {0.25-0.05*rand()} : s",             
                "fanin : uint32_t : 2 : p",             
                #"Ir : float : 1 : p",
            ], [1, 0, 0, 0, 1]),
        Neuron("n_4", [
                "u : float : 2 : s", 
                "v : float : -65 : s",        
                f"a : float : {0.02+0.08*rand()} : s", 
                f"b : float : {0.25-0.05*rand()} : s",             
                "fanin : uint32_t : 2 : p",             
                #"Ir : float : 1 : p",
            ], [0, 0, 1, 1, 0]),
    ]

    Network("test_network", equations, "v >= 30", neurons1, 30).saveGraph()