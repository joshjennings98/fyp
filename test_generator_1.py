# test_generator.py
import random
urand=random.random

class Neuron(object):
    def __init__(self, name, params, connections, equations, threshold):
        self.name = name
        self.props = list(map(lambda el: el.replace(" ", "").split(":"), params)) # Strip white space and turn to a better list
        self.states = list(filter(lambda x: x[3] == "s", list(map(lambda el: el.replace(" ", "").split(":"), params))))
        self.connections = connections
        self.equations = equations
        self.threshold = threshold

maxt = 30

name = "test_network"

equations = [
    "v = 0.04 * v * v + 5 * v + 140 - u + I",
    "u = a * (b * v - u)"
]

th = "v >= 30"

neurons = [ # Props are "name : type : value"
    Neuron("n_0", [
            f"u : float : {-65+15*urand()*urand()} : s", 
            f"v : float : {8-6*urand()*urand()} : s", 
            "a : float : 0.02 : s", 
            "b : float : 0.2 : s",             
            "fanin : uint32_t : 2 : p",             
            "Ir : float : 1 : p",
        ], [1, 0, 1, 0, 0], equations, th),
    Neuron("n_1", [
            f"u : float : {-65+15*urand()*urand()} : s", 
            f"v : float : {8-6*urand()*urand()} : s",       
            "a : float : 0.02 : s", 
            "b : float : 0.2 : s",             
            "fanin : uint32_t : 2 : p",             
            "Ir : float : 1 : p",
        ], [0, 0, 0, 1, 1], equations, th),
    Neuron("n_2", [
            "u : float : 2 : s", 
            "v : float : -65 : s",        
            f"a : float : {0.02+0.08*urand()} : s", 
            f"b : float : {0.25-0.05*urand()} : s",             
            "fanin : uint32_t : 2 : p",             
            "Ir : float : 1 : p",
        ], [0, 1, 0, 1, 0], equations, th),
    Neuron("n_3", [
            "u : float : 2 : s", 
            "v : float : -65 : s",        
            f"a : float : {0.02+0.08*urand()} : s", 
            f"b : float : {0.25-0.05*urand()} : s",             
            "fanin : uint32_t : 2 : p",             
            "Ir : float : 1 : p",
        ], [1, 0, 0, 0, 1], equations, th),
    Neuron("n_4", [
            "u : float : 2 : s", 
            "v : float : -65 : s",        
            f"a : float : {0.02+0.08*urand()} : s", 
            f"b : float : {0.25-0.05*urand()} : s",             
            "fanin : uint32_t : 2 : p",             
            "Ir : float : 1 : p",
        ], [0, 0, 1, 1, 0], equations, th),
]

def makeGraph(neurons, name, maxt, globalClock = False):

    deviceInstances = []
    edgeInstances = []     

    def makeDeviceType():
        return """<DeviceType id="neuron"> 
            <Properties> 
                <Scalar name="seed" type="uint32_t"/> 
                %s 
            </Properties> 
            <State> 
                <Scalar name="fireValue" type="int8_t"/> 
                <Scalar name="rts" type="uint32_t"/> 
                <Scalar name="t" type="uint32_t"/> 
                %s
            </State> 
            <OnInit><![CDATA[    
                // Initialise state values
                %s	   
                ]]></OnInit> 
            <InputPin name="input" messageTypeId="synapse"> 
                <Properties> 
                <Scalar name="weight" type="float"/> 
                </Properties> 
                <OnReceive><![CDATA[ 
                    if(message->fired){ 
                        handler_log(1, "Recieved Spike"); 
                        deviceState->fireValue = true; 
                    } 
                    deviceState->rts = RTS_FLAG_fire; 
                ]]></OnReceive> 
            </InputPin> 
            <OutputPin name="fire" messageTypeId="synapse"> 
                <OnSend><![CDATA[ 
                    // Assignments
                    %s

                    message->fired=deviceState->fireValue; // Add conditional in future for v_threshold 
                    handler_log(1, "Fired Spike"); 
                    deviceState->fireValue = false; 
                    deviceState->t++; 
                    // /*
                    if(deviceState->t > graphProperties->max_t / graphProperties->neuron_count){ 
                        *doSend=0; 
                        fake_handler_exit(0); 
                    }
                    // */ 
                ]]></OnSend> 
            </OutputPin> 
            <ReadyToSend><![CDATA[ 
                    *readyToSend = (deviceState->fireValue == true) ? RTS_FLAG_fire : 0; 
                ]]></ReadyToSend> 
        </DeviceType>""" % (properties, states, inits, assignments)
    
    def makeNeuronType(neuron : Neuron) -> str:
        properties = '\n        '.join(list(map(lambda el : "\t\t\t<Scalar name=\"%s\" type=\"%s\" default=\"%s\"/>" % (el[0], el[1], el[2]), neuron.props)))
        states = '\n        '.join(list(map(lambda el : "\t\t\t<Scalar name=\"%s\" type=\"%s\"/>" % (el[0], el[1]), neuron.states)))
        inits = '\n        '.join(list(map(lambda el : "\t\t\tdeviceState->%s = deviceProperties->%s; // Set initial %s value" % (el[0], el[0], el[0]), neuron.states)))
        assignments = '\n        '.join(list(map(lambda el : "\t\t\t\t%s &%s = deviceState->%s; // Assign %s" % (el[1], el[0], el[0], el[0]), neuron.states)))
        equations = '\n        '.join(list(map(lambda el : "\t\t\t\t%s;" % el, neuron.equations)))
        threshold = '%s' % (neuron.threshold)
        
        return"""<DeviceType id="neuron"> 
                <Properties> 
                    <Scalar name="seed" type="uint32_t"/>
        %s 
                </Properties> 
                <State> 
                    <Scalar name="rng" type="uint32_t"/> 
                    <Scalar name="Icount" type="uint32_t"/>
                    <Scalar name="pendingFires" type="uint32_t"/>
                    <Scalar name="rts" type="uint32_t"/> 
                    <Scalar name="t" type="uint32_t"/>
                    <Scalar name="I" type="float"/> 
        %s
                </State> 
                <OnInit><![CDATA[    
                    // Initialise state values
        %s
                    
                    deviceState->rng = deviceProperties->seed;
                    deviceState->I=deviceProperties->Ir * grng(deviceState->rng);
                    deviceState->Icount=0;
                    deviceState->pendingFires=1;
                    deviceState->rts = RTS_FLAG_fire;		   
                    ]]></OnInit> 
                <InputPin name="input" messageTypeId="synapse"> 
                    <Properties> 
                    <Scalar name="weight" type="float"/> 
                    </Properties> 
                    <OnReceive><![CDATA[ 
                        deviceState->Icount++;
                        if(message->fired){
                            deviceState->I += edgeProperties->weight; // fire at 1, (1 * weight) = weight so just add weight
                        }

                        if(deviceState->Icount == deviceProperties->fanin){
                            deviceState->pendingFires++;
                            deviceState->Icount=0;
                        }
                    ]]></OnReceive> 
                </InputPin> 
                <OutputPin name="fire" messageTypeId="synapse"> 
                    <OnSend><![CDATA[ 
                        // Assignments
        %s
                        float &I = deviceState->I; // Assign I

        %s

                        message->fired = %s;
                        
                        if(message->fired){
        %s
                        }

                        deviceState->I=deviceProperties->Ir * grng(deviceState->rng);
                        deviceState->Icount=0;
                        deviceState->pendingFires--;
                        deviceState->t++;
                        if(deviceState->t > graphProperties->max_t){
                            *doSend=0;
                            fake_handler_exit(0);
                        }
                    ]]></OnSend> 
                </OutputPin> 
                <ReadyToSend><![CDATA[ 
                        *readyToSend = (deviceState->pendingFires > 0) ? RTS_FLAG_fire : 0;
                    ]]></ReadyToSend> 
            </DeviceType>""" % (properties, states, inits, assignments, equations ,threshold, inits)

    devices = makeNeuronType(neurons[0])

    for neuron in neurons:
        neuronProps = ','.join(list(map(lambda el : "\"%s\":%s" % (el[0], el[2]), neuron.props)))
        device = "            <DevI id=\"%s\" type=\"neuron\"><P>%s</P></DevI>\n" % (neuron.name, neuronProps)
        deviceInstances.append(device)
        connections = []
        for connection in range(len(neuron.connections)): 
            if neuron.connections[connection] == 1: 
                weight = -urand() if urand() > 0.8 else 0.5 * urand() # change to random value
                edge = "            <EdgeI path=\"%s:input-%s:fire\"><P>\"weight\":%s</P></EdgeI>\n" % (neurons[connection].name, neuron.name, weight)
                connections.append(edge)
        edgeInstances.append("".join(connections))

    graph = """<?xml version='1.0'?>
<Graphs xmlns="https://poets-project.org/schemas/virtual-graph-schema-v3">
    <GraphType xmlns="https://poets-project.org/schemas/virtual-graph-schema-v3" id="%s"> 
        <Properties> 
            <Scalar name="max_t" type="uint32_t"/> 
            <Scalar name="neuron_count" type="uint32_t"/> 
        </Properties> 
        <SharedCode><![CDATA[ 
            #ifdef POETS_LEGACY_HAS_HANDLER_EXIT 
            #define _do_handler_exit(code) handler_exit(code) 
            #else 
            #define _do_handler_exit(code) ((void)0) 
            #endif 

            #define fake_handler_exit(code) \\
            { \\
                if((code)==0){ \\
                    handler_log(0, "_HANDLER_EXIT_SUCCESS_9be65737_"); \\
                }else{ \\
                    handler_log(0, "_HANDLER_EXIT_FAIL_9be65737_"); \\
                } \\
                _do_handler_exit(code); \\
            }
            uint32_t urng(uint32_t &state)
            {
                state = state*1664525+1013904223;
                return state;
            }

            // Worlds crappiest gaussian
            float grng(uint32_t &state)
            {
                uint32_t u=urng(state);
                int32_t acc=0;
                for(unsigned i=0;i<8;i++){
                acc += u&0xf;
                u=u>>4;
                }
                // a four-bit uniform has mean 7.5 and variance ((15-0+1)^2-1)/12 = 85/4
                // sum of four uniforms has mean 8*7.5=60 and variance of 8*85/4=170
                const float scale=0.07669649888473704; // == 1/sqrt(170)
                return (acc-60.0f) * scale;
            } 
            ]]></SharedCode> 
        <MessageTypes> 
            <MessageType id="synapse"> 
                <Message> 
                    <Scalar name="fired" type="int8_t"/> 
                </Message>
            </MessageType>
            <MessageType id="synapse1"> 
                <Message> 
                    <Scalar name="fired1" type="int8_t"/> 
                </Message>
            </MessageType>                %s
        </MessageTypes> 
        <DeviceTypes>%s
            %s
        </DeviceTypes> 
    </GraphType> 
    <GraphInstance id="%s_output" graphTypeId="%s"> 
        <Properties> 
            "max_t":%i,
            "neuron_count":%i
        </Properties> 
        <DeviceInstances>        %s
%s        </DeviceInstances> 
        <EdgeInstances> 
%s        </EdgeInstances> 
    </GraphInstance> 
</Graphs> 
    """ % (name, "", "", devices, name, name, maxt, len(deviceInstances), "", "".join(deviceInstances), "".join(edgeInstances))
    return graph

def saveGraph(graph, filename):

    file = open(filename, "w") 
    file.writelines(graph) 
    file.close()

    print(graph)
    print("Graph saved as:", filename)

graph = makeGraph(neurons, name, maxt)

saveGraph(graph, "test_network.xml")