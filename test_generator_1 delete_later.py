# test_generator.py

class Neuron(object):
    def __init__(self, name, params, fire_on_init, connections):
        self.name = name
        self.params = list(map(lambda el: el.replace(" ", "").split(":"), params)) # Strip white space and turn to a better list
        self.fire_on_init = fire_on_init
        self.connections = connections

maxt = 100

name = "test_network"

neurons = [ # Params are "name : type : value"
    Neuron("n_0", ["test_variable : float : 0.24565"], 1, [0, 1, 0, 0, 0]),
    Neuron("n_1", ["test_variable : float : 0.0"], 0, [0, 0, 1, 0, 0]),
    Neuron("n_2", ["test_variable : float : 0.0"], 0, [0, 0, 0, 1, 0]),
    Neuron("n_3", ["test_variable : float : 0.0"], 0, [0, 0, 0, 0, 1]),
    Neuron("n_4", ["test_variable : float : 0.0"], 0, [1, 0, 0, 0, 0]),
]

def makeGraph(neurons, name, maxt, globalClock = False):
    
    def makeClock(clock):
        if clock:
            return """      
            <DeviceType id="clock">
                <Properties>
                    <Scalar name="neuronCount" type="uint32_t"/>
                </Properties>
                <State>
                    <Scalar name="waitCount" type="uint32_t"/>
                    <Scalar name="t" type="uint32_t"/>
                </State>
                <OnInit><![CDATA[
                    deviceState->waitCount = deviceProperties->neuronCount;
                    ]]>
                </OnInit>
                <InputPin name="tock" messageTypeId="tick">
                    <OnReceive><![CDATA[
                        assert(deviceState->waitCount > 0);
                        deviceState->waitCount--;
                        ]]>
                    </OnReceive>
                </InputPin>
                <OutputPin name="tick" messageTypeId="tick" indexed="false">
                    <OnSend><![CDATA[
                    assert(deviceState->waitCount==0);
                    deviceState->waitCount=deviceProperties->neuronCount;
                    deviceState->t++;
                    if(deviceState->t > graphProperties->max_t){
                        *doSend=false;
                        fake_handler_exit(0);
                    }
                    ]]>
                    </OnSend>
                </OutputPin>
                <ReadyToSend><![CDATA[
                    *readyToSend = deviceState->waitCount==0 ? RTS_FLAG_tick : 0;
                    ]]>
                    </ReadyToSend>
                </DeviceType>"""
        else:
            return ""

    def makeTick(clock):
        if clock:
            #return """
            #<MessageType id="tick">
            #    <Message>
            #        <Scalar name="firings" type="uint32_t"/>
            #    </Message>
            #</MessageType>"""
            return "<MessageType id=\"tick\"/>"
        else:
            return ""

    def addClock(clock):
        if clock:
            return """
            <DevI id="clock" type="clock"><P>"neuronCount":%s</P></DevI>""" % str(len(deviceInstances))
        else:
            return ""

    deviceInstances = []
    edgeInstances = []     

    properties = '\n        '.join(list(map(lambda el : "<Scalar name=\"%s\" type=\"%s\" default=\"%s\"/>" % (el[0], el[1], el[2]), neurons[0].params)))
    states = '\n        '.join(list(map(lambda el : "<Scalar name=\"%s\" type=\"%s\"/>" % (el[0], el[1]), neurons[0].params)))
    inits = '\n        '.join(list(map(lambda el : "deviceState->%s = deviceProperties->%s; // Set initial %s value" % (el[0], el[0], el[0]), neurons[0].params)))
    assignments = '\n        '.join(list(map(lambda el : "%s &%s = deviceState->%s; // Assign %s" % (el[1], el[0], el[0], el[0]), neurons[0].params)))

    def makeDeviceType(clock):
        if clock:
            return """<DeviceType id="neuron">
                <Properties>
                    <Scalar name="seed" type="uint32_t"/>
                    <Scalar name="fire_on_init" type="int8_t" default="0"/>
                    <Scalar name="a" type="float" default="0.0"/>
                    <Scalar name="b" type="float" default="0.0"/>
                    <Scalar name="c" type="float" default="0.0"/>
                    <Scalar name="d" type="float" default="0.0"/>
                    <Scalar name="Ir" type="float"/>
                    <Scalar name="fanin" type="uint32_t"/>
                </Properties>
                <State>
                    <Scalar name="fireValue" type="int8_t"/> 
                    <Scalar name="u" type="float"/>
                    <Scalar name="v" type="float"/>
                    <Scalar name="I" type="float"/>
                    <Scalar name="Icount" type="uint32_t"/>
                    <Scalar name="fireValue" type="int8_t"/>
                    <Scalar name="waitTick" type="int8_t"/>
                    <Scalar name="sentSpike" type="int8_t"/>
                </State>
                <OnInit><![CDATA[
                    deviceState->rng = deviceProperties->seed;

                    deviceState->v=-65;
                    deviceState->u=deviceProperties->b * deviceState->v;

                    deviceState->fireValue=false; // We don't fire in the first round

                    deviceState->I=deviceProperties->Ir * grng(deviceState->rng);
                    deviceState->Icount=deviceProperties->fanin;
                    deviceState->waitTick=false;
                    deviceState->sentSpike=true;

                    ]]>
                </OnInit>
                <InputPin name="tick" messageTypeId="tick">
                    <OnReceive><![CDATA[
                        assert(deviceState->waitTick);
                        assert(!deviceState->sentSpike);
                        deviceState->waitTick=false;
                        ]]>
                    </OnReceive>
                </InputPin>
                <InputPin name="input" messageTypeId="spike">
                    <Properties>
                        <Scalar name="weight" type="float"/>
                    </Properties>
                    <OnReceive><![CDATA[
                        assert(deviceState->Icount < deviceProperties->fanin);

                        deviceState->Icount++;
                        if(message->fired){
                            deviceState->I += edgeProperties->weight;
                        }
                        ]]>
                    </OnReceive>
                </InputPin>
                <OutputPin name="tock" messageTypeId="tick" indexed="false">
                    <OnSend><![CDATA[
                        assert(deviceState->Icount==deviceProperties->fanin);
                        assert(!deviceState->waitTick && deviceState->sentSpike);

                        float &v=deviceState->v;
                        float &u=deviceState->u;
                        float &I=deviceState->I;

                        v=v+0.5*(0.04*v*v+5*v+140-u+I); // step 0.5 ms                THE DIFFERENTIAL EQUATION
                        v=v+0.5*(0.04*v*v+5*v+140-u+I); // for numerical
                        u=u+deviceProperties->a*(deviceProperties->b*v-u);                 // stability

                        deviceState->fireValue = v >= 30;
                        if(deviceState->fireValue){
                            handler_log(3, "FIRE!");

                            v=deviceProperties->c;
                            u += deviceProperties->d;
                        }

                        deviceState->I=deviceProperties->Ir * grng(deviceState->rng);
                        deviceState->Icount=0;
                        deviceState->sentSpike=false;
                        deviceState->waitTick=true;

                    ]]>
                    </OnSend>
                </OutputPin>
                <OutputPin name="fire" messageTypeId="spike" indexed="false">
                    <OnSend><![CDATA[
                        assert(!deviceState->waitTick);
                        assert(!deviceState->sentSpike);
                        message->fired=deviceState->fireValue;
                        deviceState->sentSpike=true;
                        ]]>
                    </OnSend>
                </OutputPin>
                    <ReadyToSend><![CDATA[
                        *readyToSend=0;
                        if(deviceState->Icount==deviceProperties->fanin && !deviceState->waitTick && deviceState->sentSpike ){
                            *readyToSend |= RTS_FLAG_tock;
                        }else if(!deviceState->waitTick && !deviceState->sentSpike){
                            *readyToSend |= RTS_FLAG_fire;
                        }
                    ]]>
                </ReadyToSend>
            </DeviceType>""" % (properties, states, inits, assignments)
        else:
            return """<DeviceType id="neuron"> 
                <Properties> 
                    <Scalar name="seed" type="uint32_t"/> 
                    <Scalar name="fire_on_init" type="int8_t" default="0"/> 
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
                    
                    // whether to fire first cycle == 1
                    if (deviceProperties->fire_on_init == 1) { 
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
    
    devices = makeDeviceType(globalClock)

    for neuron in neurons:
        neuronParams = ','.join(list(map(lambda el : "\"%s\":%s" % (el[0], el[2]), neuron.params)))
        device = "            <DevI id=\"%s\" type=\"neuron\"><P>\"fire_on_init\":%s,%s</P></DevI>\n" % (neuron.name, str(neuron.fire_on_init), neuronParams)
        deviceInstances.append(device)
        connections = []
        for connection in range(len(neuron.connections)): 
            if neuron.connections[connection] == 1: 
                weight = 1.0 # change to random value
                edge = "            <EdgeI path=\"%s:input-%s:fire\"><P>\"weight\":%s</P></EdgeI>\n" % (neurons[connection].name, neuron.name, weight)
                connections.append(edge)
        edgeInstances.append("".join(connections))
        if globalClock:
            edgeInstances.append("            <EdgeI path=\"%s:tick-clock:tick\" />\n" % (neuron.name))
            edgeInstances.append("            <EdgeI path=\"clock:tock-%s:tock\" />\n" % (neuron.name))
    
    clock = makeClock(globalClock)
    tick = makeTick(globalClock)
    clockNeuron = addClock(globalClock)


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
    """ % (name, tick, clock, devices, name, name, maxt, len(deviceInstances), clockNeuron, "".join(deviceInstances), "".join(edgeInstances))

    return graph

def saveGraph(graph, filename):

    file = open(filename, "w") 
    file.writelines(graph) 
    file.close()

    print(graph)
    print("Graph saved as:", filename)


graph = makeGraph(neurons, name, maxt, True)

saveGraph(graph, "test_network.xml")