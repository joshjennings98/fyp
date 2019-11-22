# test_generator.py

class Neuron(object):
    def __init__(self, name, fire_init, connections):
        self.name = name
        self.fire_init = fire_init
        self.connections = connections

def makeGraph(neurons, name, maxt):
    deviceInstances = []
    edgeInstances = []        

    for neuron in neurons:
        device = "  <DevI id=\"%s\" type=\"neuron\"><P>\"fire_init\":%i</P></DevI>\n" % (neuron.name, neuron.fire_init)
        deviceInstances.append(device)
        connections = []
        for connection in range(len(neuron.connections)): # change so only does connections set to 1
            if neuron.connections[connection] == 1: 
                weight = 1.0 # change to random value
                edge = "   <EdgeI path=\"%s:input-%s:fire\"><P>\"weight\":%s</P></EdgeI>\n" % (neurons[connection].name, neuron.name, weight)
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
    ]]></SharedCode> 
<MessageTypes> 
    <MessageType id="synapse"> 
    <Message> 
        <Scalar name="fired" type="int8_t"/> 
    </Message> 
    </MessageType> 
</MessageTypes> 
<DeviceTypes> 
    <DeviceType id="neuron"> 
    <Properties> 
        <Scalar name="seed" type="uint32_t"/> 
        <Scalar name="fire_init" type="int8_t" default="0"/> 
    </Properties> 
    <State> 
        <Scalar name="fireValue" type="int8_t"/> 
        <Scalar name="rts" type="uint32_t"/> 
        <Scalar name="t" type="uint32_t"/> 
    </State> 
    <OnInit><![CDATA[    
        if (deviceProperties->fire_init == 1) { 
        handler_log(1, "Fired Spike"); 
        deviceState->fireValue = true; 
        } else { 
        deviceState->fireValue = false; 
        }		   
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
    <OutputPin name="fire" messageTypeId="synapse" indexed="false"> 
        <OnSend><![CDATA[ 
            message->fired=deviceState->fireValue; // Add conditional in future for v_threshold 
        handler_log(1, "Fired Spike"); 
        deviceState->fireValue = false; 
        deviceState->t++; 
            if(deviceState->t > graphProperties->max_t / graphProperties->neuron_count){ 
                *doSend=0; 
                fake_handler_exit(0); 
            } 
        ]]></OnSend> 
    </OutputPin> 
    <ReadyToSend><![CDATA[ 
            *readyToSend = (deviceState->fireValue == true) ? RTS_FLAG_fire : 0; 
        ]]></ReadyToSend> 
    </DeviceType> 
</DeviceTypes> 
</GraphType> 
<GraphInstance id="%s_output" graphTypeId="%s"> 
<Properties> 
    "max_t":%i,
    "neuron_count":%i
</Properties> 
<DeviceInstances> 
%s    </DeviceInstances> 
<EdgeInstances> 
%s    </EdgeInstances> 
</GraphInstance> 
</Graphs> 
    """ % (name, name, name, maxt, len(deviceInstances), "".join(deviceInstances), "".join(edgeInstances))

    return graph

def saveGraph(graph, filename):

    file = open(filename, "w") 
    file.writelines(graph) 
    file.close()

    print(graph)
    print("Graph saved as:", filename)
