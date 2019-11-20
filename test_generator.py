
class Neuron(object):
    def __init__(self, name, fire_init, connections):
        self.name = name
        self.fire_init = fire_init
        self.connections = connections

name = "test_network"
maxt = 100

neurons = [
    Neuron("n_0", 1, [0, 1, 0, 0, 0]),
    Neuron("n_1", 0, [0, 0, 1, 0, 0]),
    Neuron("n_2", 0, [0, 0, 0, 1, 0]),
    Neuron("n_3", 0, [0, 0, 0, 0, 1]),
    Neuron("n_4", 0, [1, 0, 0, 0, 0]),
]

deviceInstances = []

for neuron in neurons:
    device = "   <DevI id=\"" + neuron.name + "\" type=\"neuron\"><P>\"fire_init\":" + str(neuron.fire_init) + "</P></DevI>\n"
    deviceInstances.append(device)

num_neurons = len(deviceInstances)

edgeInstances = []

for neuron in neurons:
    connections = []
    for connection in range(len(neuron.connections)): # change so only does connections set to 1
        if neuron.connections[connection] == 1: 
            weight = 1.0 # change to random value
            x = "<EdgeI path=\"" + neurons[connection].name + ":input-" + neuron.name + ":fire\"><P>\"weight\":" + str(weight) + "</P></EdgeI>\n" 
            connections.append(x)
    y = "".join(connections)
    edgeInstances.append(y)

# To Do: Make this thing nicer using multiline strings or something
graph = [
    "<?xml version='1.0'?>\n",
    "<Graphs xmlns=\"https://poets-project.org/schemas/virtual-graph-schema-v3\">\n",
    "<GraphType xmlns=\"https://poets-project.org/schemas/virtual-graph-schema-v3\" id=\"", name, "\"> \n",
    "  <Properties> \n",
    "    <Scalar name=\"max_t\" type=\"uint32_t\"/> \n",
    "	<Scalar name=\"neuron_count\" type=\"uint32_t\"/> \n",
    "  </Properties> \n",
    "  <SharedCode><![CDATA[ \n",
    "    #ifdef POETS_LEGACY_HAS_HANDLER_EXIT \n",
    "    #define _do_handler_exit(code) handler_exit(code) \n",
    "    #else \n",
    "    #define _do_handler_exit(code) ((void)0) \n",
    "    #endif \n",
    " \n",
    "    #define fake_handler_exit(code) \\\n",
    "    { \\\n",
    "        if((code)==0){ \\\n",
    "            handler_log(0, \"_HANDLER_EXIT_SUCCESS_9be65737_\"); \\\n",
    "        }else{ \\\n",
    "            handler_log(0, \"_HANDLER_EXIT_FAIL_9be65737_\"); \\\n",
    "        } \\\n",
    "        _do_handler_exit(code); \\\n",
    "    } \n",
    "    ]]></SharedCode> \n",
    "  <MessageTypes> \n",
    "    <MessageType id=\"synapse\"> \n",
    "      <Message> \n",
    "        <Scalar name=\"fired\" type=\"int8_t\"/> \n",
    "      </Message> \n",
    "    </MessageType> \n",
    "  </MessageTypes> \n",
    "  <DeviceTypes> \n",
    "    <DeviceType id=\"neuron\"> \n",
    "      <Properties> \n",
    "        <Scalar name=\"seed\" type=\"uint32_t\"/> \n",
    "        <Scalar name=\"fire_init\" type=\"int8_t\" default=\"0\"/> \n",
    "      </Properties> \n",
    "      <State> \n",
    "        <Scalar name=\"fireValue\" type=\"int8_t\"/> \n",
    "        <Scalar name=\"rts\" type=\"uint32_t\"/> \n",
    "        <Scalar name=\"t\" type=\"uint32_t\"/> \n",
    "      </State> \n",
    "      <OnInit><![CDATA[    \n",
    "        if (deviceProperties->fire_init == 1) { \n",
    "          handler_log(1, \"Fired Spike\"); \n",
    "          deviceState->fireValue = true; \n",
    "        } else { \n",
    "          deviceState->fireValue = false; \n",
    "        }		   \n",
    "		  ]]></OnInit> \n",
    "      <InputPin name=\"input\" messageTypeId=\"synapse\"> \n",
    "        <Properties> \n",
    "          <Scalar name=\"weight\" type=\"float\"/> \n",
    "        </Properties> \n",
    "        <OnReceive><![CDATA[ \n",
    "		      if(message->fired){ \n",
    "            handler_log(1, \"Recieved Spike\"); \n",
    "            deviceState->fireValue = true; \n",
    "		      } \n",
    "          deviceState->rts = RTS_FLAG_fire; \n",
    "		  ]]></OnReceive> \n",
    "      </InputPin> \n",
    "      <OutputPin name=\"fire\" messageTypeId=\"synapse\" indexed=\"false\"> \n",
    "        <OnSend><![CDATA[ \n",
    "		      message->fired=deviceState->fireValue; // Add conditional in future for v_threshold \n",
    "          handler_log(1, \"Fired Spike\"); \n",
    "          deviceState->fireValue = false; \n",
    "          deviceState->t++; \n",
    "	        if(deviceState->t > graphProperties->max_t / graphProperties->neuron_count){ \n",
    "		        *doSend=0; \n",
    "			      fake_handler_exit(0); \n",
    "	      	} \n",
    "		  ]]></OnSend> \n",
    "      </OutputPin> \n",
    "      <ReadyToSend><![CDATA[ \n",
    "		    *readyToSend = (deviceState->fireValue == true) ? RTS_FLAG_fire : 0; \n",
    "		]]></ReadyToSend> \n",
    "    </DeviceType> \n",
    "  </DeviceTypes> \n",
    "</GraphType> \n",
    " <GraphInstance id=\"", name, "_output", "\" graphTypeId=\"", name, "\"> \n",
    "   <Properties> \n",
    "    \"max_t\":", str(maxt), ",\n",
    "    \"neuron_count\":", str(num_neurons), "\n",
    "   </Properties> \n",
    "  <DeviceInstances> \n",
    "".join(deviceInstances), " \n",
    "  </DeviceInstances> \n",
    "  <EdgeInstances> \n",
    "".join(edgeInstances), " \n",
    "  </EdgeInstances> \n",
    " </GraphInstance> \n",
    "</Graphs> \n",
]

file1 = open("test_network.xml","w") 
file1.writelines(graph) 
file1.close()

print("".join(graph))
