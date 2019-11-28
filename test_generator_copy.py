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
        for connection in range(len(neuron.connections)): 
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

    
    graph = """<?xml version='1.0' encoding='ASCII'?>
<Graphs xmlns="https://poets-project.org/schemas/virtual-graph-schema-v3">
  <GraphType id="%s">
    <Properties>
      <Scalar name="max_t" type="uint32_t" />
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
    </MessageTypes>
    <DeviceTypes>
      <DeviceType id="neuron">
        <Properties>
          <Scalar name="seed" type="uint32_t"/>
          <Scalar name="fanin" type="uint32_t"/>
        </Properties>
        <State>
          <Scalar name="rng" type="uint32_t"/>
          <Scalar name="Icount" type="uint32_t"/>
          <Scalar name="pendingFires" type="uint32_t"/>
          <Scalar name="rts" type="uint32_t"/>
          <Scalar name="t" type="uint32_t"/>
        </State>
        <OnInit><![CDATA[

		  
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
		  

		  if(deviceState->Icount == deviceProperties->fanin){
			deviceState->pendingFires++;
			deviceState->Icount=0;
		  }
		  ]]></OnReceive>
        </InputPin>
        <OutputPin name="fire" messageTypeId="synapse">
          <OnSend><![CDATA[
		  assert(deviceState->pendingFires > 0);

		  

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
</Graphs> """ % (name, name, name, maxt, len(deviceInstances), "".join(deviceInstances), "".join(edgeInstances))

    
    return graph

def saveGraph(graph, filename):

    file = open(filename, "w") 
    file.writelines(graph) 
    file.close()

    print(graph)
    print("Graph saved as:", filename)
