# horible_string_stuff.py
from typing import List

def devicesGen(properties : str, states : str, inits : str, assignments : str, equations : str, threshold : str, onReset : str) -> str:
    """
    Generate the XML for the devices
    """
    return f"""<DeviceType id="neuron"> 
\t\t\t\t<Properties> 
\t\t\t\t\t<Scalar name="seed" type="uint32_t"/>
\t\t\t\t\t<Scalar name="Ir" type="float"/>
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
\t\t\t\t\t<![CDATA[
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
\t\t{onReset}
\t\t\t\t\t\t}}\n
\t\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\t\tdeviceState->Icount=0;
\t\t\t\t\t\tdeviceState->pendingFires--;
\t\t\t\t\t\tdeviceState->t++;\n
\t\t\t\t\t\tif(deviceState->t > graphProperties->max_t && graphProperties->max_t != 0){{
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

def graphGen(name : str, devices : str, maxt: int, deviceInstances : List[str], edgeInstances : List[str]) -> str:
    """
    Generate the XML for the entire graph, takes the devices and edges and attaches everyting together
    """
    return f"""<?xml version='1.0'?>
<Graphs xmlns="https://poets-project.org/schemas/virtual-graph-schema-v3">
\t<GraphType xmlns="https://poets-project.org/schemas/virtual-graph-schema-v3" id="{name}"> 
\t\t<Properties> 
\t\t\t<Scalar name="max_t" type="uint32_t"/> 
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
\t\t\t"max_t":{maxt}
\t\t</Properties> 
\t\t<DeviceInstances>\t\t
{"".join(deviceInstances)}\t\t</DeviceInstances> 
\t\t<EdgeInstances> 
{"".join(edgeInstances)}\t\t</EdgeInstances> 
\t</GraphInstance> 
</Graphs>"""