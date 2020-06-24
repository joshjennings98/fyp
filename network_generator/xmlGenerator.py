# xmlGenerator.py

from typing import List

def devicesGenGALS(properties : str, states : str, inits : str, assignments : str, equations : str, threshold : str, onReset : str, relaxed : int = 0) -> str:
    """
    Generate the XML for the devices.
    
    xml.dom.minidom with prettyfying makes everything ugly so it is hard coded.

    GALS version.
    """
    return f"""<DeviceType id="neuron"> 
\t\t\t\t<Properties> 
\t\t\t\t\t<Scalar name="seed" type="uint32_t"/>
\t\t\t\t\t<Scalar name="refractory" type="uint32_t" default="0"/> 
\t\t{properties} 
\t\t\t\t</Properties> 
\t\t\t\t<State> 
\t\t\t\t\t<Scalar name="rng" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="Icount" type="uint32_t"/>
\t\t\t\t\t<Scalar name="pendingFires" type="uint32_t"/>
\t\t\t\t\t<Scalar name="rts" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="t" type="uint32_t"/>
\t\t\t\t\t<Scalar name="finishRefractory" type="uint32_t"/>
\t\t\t\t\t<Scalar name="I" type="float"/> 
\t\t\t\t\t<Scalar name="message_count" type="uint32_t"/> 
\t\t{states}
\t\t\t\t</State> 
\t\t\t\t<OnInit>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t// Initialise state values
\t\t{inits}\n
\t\t\t\t\tdeviceState->rng = deviceProperties->seed;
\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\tdeviceState->Icount=0;
\t\t\t\t\tdeviceState->message_count=0;
\t\t\t\t\tdeviceState->pendingFires=1;
\t\t\t\t\tdeviceState->finishRefractory=0;
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
\t\t\t\t\t\tif(deviceState->Icount >= deviceProperties->fanin-{relaxed}){{
\t\t\t\t\t\t\tdeviceState->pendingFires++;
\t\t\t\t\t\t\tdeviceState->Icount=0;
\t\t\t\t\t\t}}
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnReceive> 
\t\t\t\t</InputPin> 
\t\t\t\t<OutputPin name="fire" messageTypeId="synapse"> 
\t\t\t\t\t<OnSend>
\t\t\t\t\t\t<![CDATA[  
\t\t\t\t\t\tdeviceState->message_count++;
\t\t\t\t\t\t//handler_log(1, "%d", deviceState->message_count);
\t\t\t\t\t\t// Assignments
\t\t{assignments}
\t\t\t\t\t\tfloat &I = deviceState->I; // Assign I\n
\t\t\t\t\t\tif (deviceState->t >= deviceState->finishRefractory) {{
\t\t\t{equations}
\t\t\t\t\t\t}}\n
\t\t\t\t\t\tmessage->fired = {threshold};
\t\t\t\t\t\tif(message->fired){{
\t\t\t\t\t\t\t//handler_log(1, "FIRE! %i", deviceState->t);
\t\t\t\t\t\t\tdeviceState->finishRefractory = deviceState->t + deviceProperties->refractory;
\t\t{onReset}
\t\t\t\t\t\t}}\n
\t\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\t\tdeviceState->Icount=0;
\t\t\t\t\t\tdeviceState->pendingFires--;
\t\t\t\t\t\tdeviceState->t++;\n
\t\t\t\t\t\tif(deviceState->t > graphProperties->max_t && graphProperties->max_t != 0){{
\t\t\t\t\t\t\thandler_log(1, "Total messages %d", deviceState->message_count);
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

def graphGenGALS(name : str, devices : str, maxt: int) -> str:
    """
    Generate the XML for the entire graph, takes the devices and edges and attaches everyting together.

    GALS version.
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
\t\t\tfloat grngOG(uint32_t &state)
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

// NEW SHIT

float const pi = 3.14159265358979323846;
float const two_pi = 2.0 * pi;
float const half_pi = 0.5 * pi;

float cosineCalc1(float x)
{{
    const float c1 = 0.9999932946;
    const float c2 = -0.4999124376;
    const float c3 = 0.0414877472;
    const float c4 = -0.0012712095;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * (c3 + c4 * x2)));
}}

float cosineCalc(float x)
{{
    const float c1 = 0.99940307;
    const float c2 = -0.49558072;
    const float c3 = 0.03679168;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * c3));
}}

// Driver for cosine function, simplifies maths
float cosine(float x)
{{
    //return cos(x);
    int quad; // quadrant

    
    // float modulo to get rid of x > 2pi
    while (x > two_pi)
        x -= two_pi;

    // cos -x = cos x
    if (x < 0)
        x = -x;
    

    quad = int(x/half_pi);
    switch (quad) {{
        case 0:
            return cosineCalc(x);
        case 1:
            return -cosineCalc(pi-x);
        case 2:
            return -cosineCalc(x-pi);
        case 3:
            return cosineCalc(two_pi-x);
    }}
}}

// sine is just cosine shifted by half pi
float sine(float x)
{{
    return cosine(half_pi - x);
}}

float logarithm(float x)
{{
    union {{ float f; uint32_t i; }} vx = {{ x }};
    union {{ uint32_t i; float f; }} mx = {{ (vx.i & 0x007FFFFF) | 0x3f000000 }};
  
    float y = vx.i;
    y *= 1.1920928955078125e-7f;

    return y - 124.22551499f
           - 1.498030302f * mx.f 
           - 1.72587999f / (0.3520887068f + mx.f);
}}

float squareroot(float x)
{{
   unsigned int i = *(unsigned int*) &x; 
   // adjust bias
   i  += 127 << 23;
   // approximation of square root
   i >>= 1; 
   return *(float*) &i;
}}

float grng(uint32_t &state)
{{
	float mu = 0, sigma = 1;
	static const float epsilon = 1.7e-37;
	// static const double two_pi = 2.0*3.14159265358979323846;

	thread_local float z1;
	thread_local bool generate;
	generate = !generate;

	if (!generate)
	   return z1 * sigma + mu;

	float u1, u2;

    do
    {{
        u1 = (float)urng(state) / 4294967295.0f;
        u2 = (float)urng(state) / 4294967295.0f;
    }}
    while (u1 <= epsilon);

	float z0;
	z0 = squareroot(-2.0 * logarithm(u1)) * cosine(two_pi * u2);
	z1 = squareroot(-2.0 * logarithm(u1)) * sine(two_pi * u2);

	return z0 * sigma + mu;
}}

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
\t\t</Properties>"""

def devicesGenClocked(properties : str, states : str, inits : str, assignments : str, equations : str, threshold : str, onReset : str) -> str:
    """
    Generate the XML for the devices.
    
    xml.dom.minidom with prettyfying makes everything ugly so it is hard coded.

    Clocked version.
    """
    return f"""<DeviceType id="neuron">
\t\t\t\t<Properties>
\t\t\t\t\t<Scalar name="seed" type="uint32_t"/>
\t\t\t\t\t<Scalar name="refractory" type="uint32_t" default="0"/> 
\t\t{properties}
\t\t\t\t</Properties>
\t\t\t\t<State>
\t\t\t\t\t<Scalar name="rng" type="uint32_t"/>
\t\t\t\t\t<Scalar name="mcount" type="uint32_t"/>
\t\t\t\t\t<Scalar name="I" type="float"/>
\t\t\t\t\t<Scalar name="Icount" type="uint32_t"/>
\t\t\t\t\t<Scalar name="fireValue" type="int8_t"/>
\t\t\t\t\t<Scalar name="waitTick" type="int8_t"/>
\t\t\t\t\t<Scalar name="sentSpike" type="int8_t"/>
\t\t\t\t\t<Scalar name="finishRefractory" type="uint32_t"/>
\t\t{states}
\t\t\t\t</State>
\t\t\t\t<OnInit>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t\tdeviceState->rng = deviceProperties->seed;\n
\t\t\t{inits}\n
\t\t\t\t\t\tdeviceState->fireValue=false; // We don't fire in the first round\n
\t\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\t\tdeviceState->Icount=deviceProperties->fanin;
\t\t\t\t\t\tdeviceState->waitTick=false;
\t\t\t\t\t\tdeviceState->sentSpike=true;
\t\t\t\t\t\tdeviceState->mcount = 0;
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnInit>
\t\t\t\t<InputPin name="tick" messageTypeId="tick">
\t\t\t\t\t<OnReceive>
\t\t\t\t\t\t<![CDATA[
\t\t\t\t\t\t\tdeviceState->waitTick=false;
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnReceive>
\t\t\t\t</InputPin>
\t\t\t\t<InputPin name="input" messageTypeId="spike">
\t\t\t\t\t<Properties>
\t\t\t\t\t\t<Scalar name="weight" type="float"/>
\t\t\t\t</Properties>
\t\t\t\t\t<OnReceive>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t\tdeviceState->Icount++;
\t\t\t\t\t\tif(message->fired){{
\t\t\t\t\t\t\tdeviceState->I += edgeProperties->weight;
\t\t\t\t\t\t}}
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnReceive>
\t\t\t\t</InputPin>
\t\t\t\t<OutputPin name="tock" messageTypeId="tick" indexed="false">
\t\t\t\t\t<OnSend>
\t\t\t\t\t\t<![CDATA[
\t\t\t{assignments}
\t\t\t\t\t\tfloat &I=deviceState->I;\n
\t\t\t\t\t\tif (deviceState->finishRefractory <= 0) {{
\t\t\t{equations}
\t\t\t\t\t\t}} else {{
\t\t\t\t\t\t\t//// handler_log(1, "refractory=%d", deviceState->finishRefractory);
\t\t\t\t\t\t}}\n
\t\t\t\t\t\tif (deviceState->finishRefractory > 0) {{
\t\t\t\t\t\t\tdeviceState->finishRefractory -= 1;
\t\t\t\t\t\t}} 
\t\t\t\t\t\t\tmessage->count=0;
\t\t\t\t\t\tdeviceState->fireValue = {threshold};
\t\t\t\t\t\tif(deviceState->fireValue){{
\t\t\t\t\t\t\t//deviceState->mcount += 1;
\t\t\t\t\t\t\tmessage->count=1;
\t\t\t\t\t\t\t// handler_log(1, "FIRE!");
\t\t\t\t\t\t\tdeviceState->finishRefractory = deviceProperties->refractory;
\t\t{onReset}
\t\t\t\t\t\t}}\n
\t\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\t\t//// handler_log(1, "rand=%f", deviceState->I/deviceProperties->Ir);
\t\t\t\t\t\tdeviceState->Icount=0;
\t\t\t\t\t\tdeviceState->sentSpike=false;
\t\t\t\t\t\tdeviceState->waitTick=true;
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnSend>
\t\t\t\t</OutputPin>
\t\t\t\t<OutputPin name="fire" messageTypeId="spike" indexed="false">
\t\t\t\t\t<OnSend>
\t\t\t\t\t\t<![CDATA[
\t\t\t\t\t\t\tmessage->fired=deviceState->fireValue;
\t\t\t\t\t\t\tdeviceState->sentSpike=true;
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnSend>
\t\t\t\t</OutputPin>
\t\t\t\t<ReadyToSend>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t\t*readyToSend=0;
\t\t\t\t\t\tif(deviceState->Icount==deviceProperties->fanin && !deviceState->waitTick && deviceState->sentSpike ){{
\t\t\t\t\t\t\t*readyToSend |= RTS_FLAG_tock;
\t\t\t\t\t\t}}else if(!deviceState->waitTick && !deviceState->sentSpike){{
\t\t\t\t\t\t\t*readyToSend |= RTS_FLAG_fire;
\t\t\t\t\t\t}}
\t\t\t\t\t]]>
\t\t\t\t</ReadyToSend>
\t\t\t</DeviceType>
\t\t\t<DeviceType id="clock">
\t\t\t\t<Properties>
\t\t\t\t\t<Scalar name="neuronCount" type="uint32_t"/>
\t\t\t\t</Properties>
\t\t\t\t<State>
\t\t\t\t\t<Scalar name="waitCount" type="uint32_t"/>
\t\t\t\t\t<Scalar name="mcount" type="uint32_t"/>
\t\t\t\t\t<Scalar name="t" type="uint32_t"/>
\t\t\t\t</State>
\t\t\t\t<OnInit>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t\tdeviceState->waitCount = deviceProperties->neuronCount;
\t\t\t\t\t]]>
\t\t\t\t</OnInit>
\t\t\t\t<InputPin name="tock" messageTypeId="tick">
\t\t\t\t\t<OnReceive>
\t\t\t\t\t\t<![CDATA[
\t\t\t\t\t\t\tdeviceState->mcount += message->count;   
\t\t\t\t\t\t\tdeviceState->waitCount--;
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnReceive>
\t\t\t\t</InputPin>
\t\t\t\t<OutputPin name="tick" messageTypeId="tick" indexed="false">
\t\t\t\t\t<OnSend>
\t\t\t\t\t\t<![CDATA[
\t\t\t\t\t\t\tdeviceState->waitCount=deviceProperties->neuronCount;
\t\t\t\t\t\t\tdeviceState->t++;
\t\t\t\t\t\t\t// handler_log(1, "time = %d", deviceState->t);
\t\t\t\t\t\t\tif(deviceState->t > graphProperties->max_t){{
\t\t\t\t\t\t\t\thandler_log(1, "final count = %d", deviceState->mcount);
\t\t\t\t\t\t\t\t*doSend=false;
\t\t\t\t\t\t\t\tfake_handler_exit(0);
\t\t\t\t\t\t\t}}
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnSend>
\t\t\t\t</OutputPin>
\t\t\t\t<ReadyToSend>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t\t*readyToSend = deviceState->waitCount==0 ? RTS_FLAG_tick : 0;
\t\t\t\t\t]]>
\t\t\t\t</ReadyToSend>
\t\t\t</DeviceType>
"""

def graphGenClocked(name : str, devices : str, maxt: int) -> str:
    """
    Generate the XML for the entire graph, takes the devices and edges and attaches everyting together.

    Clocked version.
    """
    return f"""<?xml version='1.0'?>
<Graphs xmlns="https://poets-project.org/schemas/virtual-graph-schema-v3">
\t<GraphType xmlns="https://poets-project.org/schemas/virtual-graph-schema-v3" id="{name}">
\t\t<Properties>
\t\t\t<Scalar name="max_t" type="uint32_t"/>
\t\t</Properties>
\t\t<SharedCode>
\t\t\t<![CDATA[
\t\t\t\t#ifdef POETS_LEGACY_HAS_HANDLER_EXIT
\t\t\t\t#define _do_handler_exit(code) handler_exit(code)
\t\t\t\t#else
\t\t\t\t#define _do_handler_exit(code) ((void)0)
\t\t\t\t#endif\n
\t\t\t\t#define fake_handler_exit(code) \\
\t\t\t\t{{ \\
\t\t\t\t\tif((code)==0){{ \\
\t\t\t\t\t\thandler_log(0, "_HANDLER_EXIT_SUCCESS_9be65737_"); \\
\t\t\t\t\t}}else{{ \\
\t\t\t\t\t\thandler_log(0, "_HANDLER_EXIT_FAIL_9be65737_"); \\
\t\t\t\t\t}} \\
\t\t\t\t\t_do_handler_exit(code); \\
\t\t\t\t}}\n
\t\t\t\tuint32_t urng(uint32_t &state)
\t\t\t\t{{
\t\t\t\t\tstate = state*1664525+1013904223;
\t\t\t\t\treturn state;
\t\t\t\t}}\n
\t\t\t\t// Worlds crappiest gaussian
\t\t\t\tfloat grngOG(uint32_t &state)
\t\t\t\t{{
\t\t\t\t\tuint32_t u=urng(state);
\t\t\t\t\tint32_t acc=0;
\t\t\t\t\tfor(unsigned i=0;i<8;i++){{
\t\t\t\t\t\tacc += u&0xf;
\t\t\t\t\t\tu=u>>4;
\t\t\t\t\t}}
\t\t\t\t\t// a four-bit uniform has mean 7.5 and variance ((15-0+1)^2-1)/12 = 85/4
\t\t\t\t\t// sum of four uniforms has mean 8*7.5=60 and variance of 8*85/4=170
\t\t\t\t\tconst float scale=0.07669649888473704; // == 1/sqrt(170)
\t\t\t\t\tfloat f = (acc-60.0f) * scale;
\t\t\t\t\treturn f; // >= 0 ? f : -1.0 * f;
\t\t\t\t}}\n


// NEW SHIT

float const pi = 3.14159265358979323846;
float const two_pi = 2.0 * pi;
float const half_pi = 0.5 * pi;

float cosineCalc1(float x)
{{
    const float c1 = 0.9999932946;
    const float c2 = -0.4999124376;
    const float c3 = 0.0414877472;
    const float c4 = -0.0012712095;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * (c3 + c4 * x2)));
}}

float cosineCalc(float x)
{{
    const float c1 = 0.99940307;
    const float c2 = -0.49558072;
    const float c3 = 0.03679168;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * c3));
}}

// Driver for cosine function, simplifies maths
float cosine(float x)
{{
    //return cos(x);
    int quad; // quadrant

    
    // float modulo to get rid of x > 2pi
    while (x > two_pi)
        x -= two_pi;

    // cos -x = cos x
    if (x < 0)
        x = -x;
    

    quad = int(x/half_pi);
    switch (quad) {{
        case 0:
            return cosineCalc(x);
        case 1:
            return -cosineCalc(pi-x);
        case 2:
            return -cosineCalc(x-pi);
        case 3:
            return cosineCalc(two_pi-x);
    }}
}}

// sine is just cosine shifted by half pi
float sine(float x)
{{
    return cosine(half_pi - x);
}}

float logarithm(float x)
{{
    union {{ float f; uint32_t i; }} vx = {{ x }};
    union {{ uint32_t i; float f; }} mx = {{ (vx.i & 0x007FFFFF) | 0x3f000000 }};
  
    float y = vx.i;
    y *= 1.1920928955078125e-7f;

    return y - 124.22551499f
           - 1.498030302f * mx.f 
           - 1.72587999f / (0.3520887068f + mx.f);
}}

float squareroot(float x)
{{
   unsigned int i = *(unsigned int*) &x; 
   // adjust bias
   i  += 127 << 23;
   // approximation of square root
   i >>= 1; 
   return *(float*) &i;
}}

float grng(uint32_t &state)
{{
	float mu = 0, sigma = 1;
	static const float epsilon = 1.7e-37;
	// static const double two_pi = 2.0*3.14159265358979323846;

	thread_local float z1;
	thread_local bool generate;
	generate = !generate;

	if (!generate)
	   return z1 * sigma + mu;

	float u1, u2;

    do
    {{
        u1 = (float)urng(state) / 4294967295.0f;
        u2 = (float)urng(state) / 4294967295.0f;
    }}
    while (u1 <= epsilon);

	float z0;
	z0 = squareroot(-2.0 * logarithm(u1)) * cosine(two_pi * u2);
	z1 = squareroot(-2.0 * logarithm(u1)) * sine(two_pi * u2);

	return z0 * sigma + mu;
}}


\t\t\t]]>
\t\t</SharedCode>
\t\t<MessageTypes>
\t\t\t<MessageType id="spike">
\t\t\t\t<Message>
\t\t\t\t\t<Scalar name="fired" type="int8_t"/>
\t\t\t\t</Message>
\t\t\t</MessageType>
\t\t\t<MessageType id="tick">
\t\t\t\t<Message>
\t\t\t\t\t<Scalar name="count" type="uint32_t"/>
\t\t\t\t</Message>
\t\t\t</MessageType>
\t\t</MessageTypes>
\t\t<DeviceTypes>
\t\t\t{devices}\t</DeviceTypes>
\t</GraphType>
\t<GraphInstance id="{name}_output" graphTypeId="{name}">
\t\t<Properties>
\t\t\t"max_t":{maxt}
\t\t</Properties>"""

def devicesGenNone(properties : str, states : str, inits : str, assignments : str, equations : str, threshold : str, onReset : str) -> str:
    """
    Generate the XML for the devices.
    
    xml.dom.minidom with prettyfying makes everything ugly so it is hard coded.

    Non synchronised version.
    """
    return f"""<DeviceType id="neuron"> 
\t\t\t\t<Properties> 
\t\t\t\t\t<Scalar name="seed" type="uint32_t"/>

\t\t\t\t\t<Scalar name="refractory" type="uint32_t" default="0"/> 
\t\t{properties} 
\t\t\t\t</Properties> 
\t\t\t\t<State> 
\t\t\t\t\t<Scalar name="rng" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="pendingFires" type="uint32_t"/>
\t\t\t\t\t<Scalar name="rts" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="t" type="uint32_t"/>
\t\t\t\t\t<Scalar name="finishRefractory" type="uint32_t"/>
\t\t\t\t\t<Scalar name="I" type="float"/> 
\t\t{states}
\t\t\t\t</State> 
\t\t\t\t<OnInit>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t// Initialise state values
\t\t{inits}\n
\t\t\t\t\tdeviceState->rng = deviceProperties->seed;
\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\tdeviceState->pendingFires=1;
\t\t\t\t\tdeviceState->finishRefractory=0;
\t\t\t\t\tdeviceState->rts = RTS_FLAG_fire;		   
\t\t\t\t\t]]>
\t\t\t\t</OnInit> 
\t\t\t\t<InputPin name="input" messageTypeId="synapse"> 
\t\t\t\t\t<Properties> 
\t\t\t\t\t<Scalar name="weight" type="float"/> 
\t\t\t\t\t</Properties> 
\t\t\t\t\t<OnReceive>
\t\t\t\t\t\t<![CDATA[ 
\t\t\t\t\t\t\tdeviceState->I += edgeProperties->weight; // fire at 1, (1 * weight) = weight so just add weight
\t\t\t\t\t\t\tdeviceState->pendingFires++;
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnReceive> 
\t\t\t\t</InputPin> 
\t\t\t\t<OutputPin name="fire" messageTypeId="synapse"> 
\t\t\t\t\t<OnSend>
\t\t\t\t\t\t<![CDATA[ 
\t\t\t\t\t\t// Assignments
\t\t{assignments}
\t\t\t\t\t\tfloat &I = deviceState->I; // Assign I\n
\t\t\t\t\t\tif (deviceState->t >= deviceState->finishRefractory) {{
\t\t\t{equations}
\t\t\t\t\t\t}}\n
\t\t\t\t\t\t//// handler_log(1, "v=%f, u=%f, I=%f", deviceState->v, deviceState->u, deviceState->I);
\t\t\t\t\t\tmessage->fired = {threshold};
\t\t\t\t\t\tif(message->fired){{
\t\t\t\t\t\t\t// handler_log(1, "FIRE! %i", deviceState->t);
\t\t\t\t\t\t\tdeviceState->finishRefractory = deviceState->t + deviceProperties->refractory;
\t\t{onReset}
\t\t\t\t\t\t}}\n
\t\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
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

def graphGenNone(name : str, devices : str, maxt: int) -> str:
    """
    Generate the XML for the entire graph, takes the devices and edges and attaches everyting together.

    None synchronised version.
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
\t\t\tfloat grngOG(uint32_t &state)
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

// NEW SHIT

float const pi = 3.14159265358979323846;
float const two_pi = 2.0 * pi;
float const half_pi = 0.5 * pi;

float cosineCalc1(float x)
{{
    const float c1 = 0.9999932946;
    const float c2 = -0.4999124376;
    const float c3 = 0.0414877472;
    const float c4 = -0.0012712095;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * (c3 + c4 * x2)));
}}

float cosineCalc(float x)
{{
    const float c1 = 0.99940307;
    const float c2 = -0.49558072;
    const float c3 = 0.03679168;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * c3));
}}

// Driver for cosine function, simplifies maths
float cosine(float x)
{{
    //return cos(x);
    int quad; // quadrant

    
    // float modulo to get rid of x > 2pi
    while (x > two_pi)
        x -= two_pi;

    // cos -x = cos x
    if (x < 0)
        x = -x;
    

    quad = int(x/half_pi);
    switch (quad) {{
        case 0:
            return cosineCalc(x);
        case 1:
            return -cosineCalc(pi-x);
        case 2:
            return -cosineCalc(x-pi);
        case 3:
            return cosineCalc(two_pi-x);
    }}
}}

// sine is just cosine shifted by half pi
float sine(float x)
{{
    return cosine(half_pi - x);
}}

float logarithm(float x)
{{
    union {{ float f; uint32_t i; }} vx = {{ x }};
    union {{ uint32_t i; float f; }} mx = {{ (vx.i & 0x007FFFFF) | 0x3f000000 }};
  
    float y = vx.i;
    y *= 1.1920928955078125e-7f;

    return y - 124.22551499f
           - 1.498030302f * mx.f 
           - 1.72587999f / (0.3520887068f + mx.f);
}}

float squareroot(float x)
{{
   unsigned int i = *(unsigned int*) &x; 
   // adjust bias
   i  += 127 << 23;
   // approximation of square root
   i >>= 1; 
   return *(float*) &i;
}}

float grng(uint32_t &state)
{{
	float mu = 0, sigma = 1;
	static const float epsilon = 1.7e-37;
	// static const double two_pi = 2.0*3.14159265358979323846;

	thread_local float z1;
	thread_local bool generate;
	generate = !generate;

	if (!generate)
	   return z1 * sigma + mu;

	float u1, u2;

    do
    {{
        u1 = (float)urng(state) / 4294967295.0f;
        u2 = (float)urng(state) / 4294967295.0f;
    }}
    while (u1 <= epsilon);

	float z0;
	z0 = squareroot(-2.0 * logarithm(u1)) * cosine(two_pi * u2);
	z1 = squareroot(-2.0 * logarithm(u1)) * sine(two_pi * u2);

	return z0 * sigma + mu;
}}

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
\t\t</Properties>"""

def devicesGenExtreme(properties : str, states : str, inits : str, assignments : str, equations : str, threshold : str, onReset : str) -> str:
    """
    Generate the XML for the devices.
    
    xml.dom.minidom with prettyfying makes everything ugly so it is hard coded.

    Non synchronised version.
    """
    return f"""<DeviceType id="neuron"> 
\t\t\t\t<Properties> 
\t\t\t\t\t<Scalar name="seed" type="uint32_t"/>

\t\t\t\t\t<Scalar name="refractory" type="uint32_t" default="0"/> 
\t\t{properties} 
\t\t\t\t</Properties> 
\t\t\t\t<State> 
\t\t\t\t\t<Scalar name="rng" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="pendingFires" type="uint32_t"/>
\t\t\t\t\t<Scalar name="rts" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="t" type="uint32_t"/>
\t\t\t\t\t<Scalar name="finishRefractory" type="uint32_t"/>
\t\t\t\t\t<Scalar name="I" type="float"/> 
\t\t\t\t\t<Scalar name="t_most_recent" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="t_current_max" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="fireSpike" type="uint32_t"/> 
\t\t{states}
\t\t\t\t</State> 
\t\t\t\t<OnInit>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t// Initialise state values
\t\t{inits}\n
\t\t\t\t\tdeviceState->rng = deviceProperties->seed;
\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\tdeviceState->pendingFires=1;
\t\t\t\t\tdeviceState->finishRefractory=0;
\t\t\t\t\tdeviceState->t_most_recent=0;
\t\t\t\t\tdeviceState->t_current_max=0;
\t\t\t\t\tdeviceState->rts = RTS_FLAG_fire;	
\t\t\t\t\tdeviceState->fireSpike = true;		   
\t\t\t\t\t]]>
\t\t\t\t</OnInit> 
\t\t\t\t<InputPin name="input" messageTypeId="synapse"> 
\t\t\t\t\t<Properties> 
\t\t\t\t\t<Scalar name="weight" type="float"/> 
\t\t\t\t\t</Properties> 
\t\t\t\t\t<OnReceive>
\t\t\t\t\t\t<![CDATA[ 
\t\t\t\t\t\t\tdeviceState->I += edgeProperties->weight; // fire at 1, (1 * weight) = weight so just add weight
\t\t\t\t\t\t\tif(deviceState->t_current_max < message->fired){{
\t\t\t\t\t\t\t\tdeviceState->t_most_recent=message->fired;
\t\t\t\t\t\t\t}}
\t\t\t\t\t\t\tdeviceState->pendingFires++;
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnReceive> 
\t\t\t\t</InputPin> 
\t\t\t\t<OutputPin name="fire" messageTypeId="synapse"> 
\t\t\t\t\t<OnSend>
\t\t\t\t\t\t<![CDATA[ 
\t\t\t\t\t\t// Assignments
\t\t{assignments}
\t\t\t\t\t\tfloat &I = deviceState->I; // Assign I\n
\t\t\t\t\t\tdeviceState->fireSpike = false;
\t\t\t\t\t\t//// handler_log(1, "time diff=%d", deviceState->t_most_recent - deviceState->t_current_max);
\t\t\t\t\t\tif((deviceState->t_most_recent > deviceState->t_current_max)){{ 
\t\t\t\t\t\t\t\tint diff = deviceState->t_most_recent - deviceState->t_current_max;
\t\t\t\t\t\t\t\t// handler_log(1, "diff=%d", diff);
\t\t\t\t\t\t\t\tfor (int i = 0; i < diff; i++) {{
\t\t\t\t\t\t\t\t\tif (deviceState->finishRefractory <= 0) {{
\t\t\t\t\t\t\t\t\t\t//// handler_log(1, "v = %f, I = %f", deviceState->v, deviceState->I);
\t\t\t\t\t{equations}
\t\t\t\t\t\t\t\tif({threshold}){{ i = diff; }}
\t\t\t\t\t\t\t\t\t}} else {{
\t\t\t\t\t\t\t\t\tdeviceState->finishRefractory -= 1;
\t\t\t\t\t\t\t\t\t}}
\t\t\t\t\t\t\t\t}}
\t\t\t\t\t\t\t\tdeviceState->t_current_max = deviceState->t_most_recent;
\t\t\t\t\t\t}}
\t\t\t\t\t\tif({threshold}){{
\t\t\t\t\t\t\t// handler_log(1, "FIRE! %i", deviceState->t);
\t\t\t\t\t\t\tdeviceState->fireSpike = true;
\t\t\t\t\t\t\tdeviceState->finishRefractory = deviceState->t + deviceProperties->refractory;
\t\t{onReset}
\t\t\t\t\t\t}}
\t\t\t\t\t\t// handler_log(1, "firespike = %i", deviceState->fireSpike);
\t\t\t\t\t\tmessage->fired = deviceState->t_current_max + 1;
\t\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
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
\t\t\t\t\t*readyToSend = (deviceState->pendingFires > 0) ? deviceState->fireSpike : 0;
\t\t\t\t\t]]>
\t\t\t\t</ReadyToSend> 
\t\t\t</DeviceType>"""

def graphGenExtreme(name : str, devices : str, maxt: int) -> str:
    """
    Generate the XML for the entire graph, takes the devices and edges and attaches everyting together.

    None synchronised version.
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
\t\t\tfloat grngOG(uint32_t &state)
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
// NEW SHIT

float const pi = 3.14159265358979323846;
float const two_pi = 2.0 * pi;
float const half_pi = 0.5 * pi;

float cosineCalc1(float x)
{{
    const float c1 = 0.9999932946;
    const float c2 = -0.4999124376;
    const float c3 = 0.0414877472;
    const float c4 = -0.0012712095;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * (c3 + c4 * x2)));
}}

float cosineCalc(float x)
{{
    const float c1 = 0.99940307;
    const float c2 = -0.49558072;
    const float c3 = 0.03679168;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * c3));
}}

// Driver for cosine function, simplifies maths
float cosine(float x)
{{
    //return cos(x);
    int quad; // quadrant

    
    // float modulo to get rid of x > 2pi
    while (x > two_pi)
        x -= two_pi;

    // cos -x = cos x
    if (x < 0)
        x = -x;
    

    quad = int(x/half_pi);
    switch (quad) {{
        case 0:
            return cosineCalc(x);
        case 1:
            return -cosineCalc(pi-x);
        case 2:
            return -cosineCalc(x-pi);
        case 3:
            return cosineCalc(two_pi-x);
    }}
}}

// sine is just cosine shifted by half pi
float sine(float x)
{{
    return cosine(half_pi - x);
}}

float logarithm(float x)
{{
    union {{ float f; uint32_t i; }} vx = {{ x }};
    union {{ uint32_t i; float f; }} mx = {{ (vx.i & 0x007FFFFF) | 0x3f000000 }};
  
    float y = vx.i;
    y *= 1.1920928955078125e-7f;

    return y - 124.22551499f
           - 1.498030302f * mx.f 
           - 1.72587999f / (0.3520887068f + mx.f);
}}

float squareroot(float x)
{{
   unsigned int i = *(unsigned int*) &x; 
   // adjust bias
   i  += 127 << 23;
   // approximation of square root
   i >>= 1; 
   return *(float*) &i;
}}

float grng(uint32_t &state)
{{
	float mu = 0, sigma = 1;
	static const float epsilon = 1.7e-37;
	// static const double two_pi = 2.0*3.14159265358979323846;

	thread_local float z1;
	thread_local bool generate;
	generate = !generate;

	if (!generate)
	   return z1 * sigma + mu;

	float u1, u2;

    do
    {{
        u1 = (float)urng(state) / 4294967295.0f;
        u2 = (float)urng(state) / 4294967295.0f;
    }}
    while (u1 <= epsilon);

	float z0;
	z0 = squareroot(-2.0 * logarithm(u1)) * cosine(two_pi * u2);
	z1 = squareroot(-2.0 * logarithm(u1)) * sine(two_pi * u2);

	return z0 * sigma + mu;
}}

\t\t\t]]>
\t\t</SharedCode> 
\t\t<MessageTypes> 
\t\t\t<MessageType id="synapse"> 
\t\t\t\t<Message> 
\t\t\t\t\t<Scalar name="fired" type="uint32_t"/> 
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
\t\t</Properties>"""

def devicesGenBarrier(properties : str, states : str, inits : str, assignments : str, equations : str, threshold : str, onReset : str) -> str:
    """
    Generate the XML for the devices.
    
    xml.dom.minidom with prettyfying makes everything ugly so it is hard coded.

    Barrier version.

    """
    return f"""<DeviceType id="neuron"> 
\t\t\t\t<Properties> 
\t\t\t\t\t<Scalar name="seed" type="uint32_t"/>
\t\t\t\t\t<Scalar name="refractory" type="uint32_t" default="0"/> 
\t\t{properties} 
\t\t\t\t</Properties> 
\t\t\t\t<State> 
\t\t\t\t\t<Scalar name="rng" type="uint32_t"/> 
\t\t\t\t\t<Scalar name="t" type="uint32_t"/>
\t\t\t\t\t<Scalar name="finishRefractory" type="uint32_t"/>
\t\t\t\t\t<Scalar name="I" type="float"/> 
\t\t\t\t\t<Scalar name="Icount" type="uint32_t"/>
\t\t\t\t\t<Scalar name="fireValue" type="uint32_t"/> 
\t\t{states}
\t\t\t\t</State> 
\t\t\t\t<OnInit>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t// Initialise state values
\t\t{inits}\n
handler_log(1, "test init");
\t\t\t\t\tdeviceState->rng = deviceProperties->seed;
\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\tdeviceState->Icount=0;
\t\t\t\t\t]]>
\t\t\t\t</OnInit> 
\t\t\t\t<InputPin name="input" messageTypeId="spike"> 
\t\t\t\t\t<Properties> 
\t\t\t\t\t<Scalar name="weight" type="float"/> 
\t\t\t\t\t</Properties> 
\t\t\t\t\t<OnReceive>
\t\t\t\t\t\t<![CDATA[
handler_log(1, "TEST");
\t\t\t\t\t\t\tdeviceState->Icount++;
\t\t\t\t\t\t\tdeviceState->I += edgeProperties->weight;
\t\t\t\t\t\t]]>
\t\t\t\t\t</OnReceive> 
\t\t\t\t</InputPin> 
\t\t\t\t<OnHardwareIdle>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t\t{assignments} 
\t\t\t\t\t\tfloat &I=deviceState->I;
\t\t\t\t\t\t{equations}
\t\t\t\t\t\tdeviceState->t++;
\t\t\t\t\t\tbool fire = {threshold};
handler_log(1, "v=%f", devicesState->v);
\t\t\t\t\t\tif(fire){{
\t\t\t\t\t\t\t //handler_log(1, "FIRE! %i", deviceState->t);
\t\t\t\t\t\t\t// handler_log(1, "v = %f", deviceState->v);
\t\t\t\t\t\t\t{onReset}
\t\t\t\t\t\t}}
\t\t\t\t\t\tdeviceState->fireValue=fire;
\t\t\t\t\t\tdeviceState->I=deviceProperties->Ir * grng(deviceState->rng);
\t\t\t\t\t\tdeviceState->Icount=0;
\t\t\t\t\t]]>
\t\t\t\t</OnHardwareIdle>
\t\t\t\t<OutputPin name="fire" messageTypeId="spike" indexed="false">
\t\t\t\t<OnSend>
\t\t\t\t\t<![CDATA[
\t\t\t\t\t\tif(deviceState->t > graphProperties->max_t){{
\t\t\t\t\t\t\t*doSend=false;
\t\t\t\t\t\t\tfake_handler_exit(0);
\t\t\t\t\t\t}}
\t\t\t\t\t\t//// handler_log(1, "t = %u", deviceState->t);
\t\t\t\t\t\tdeviceState->fireValue=false;
\t\t\t\t\t]]>
\t\t\t\t</OnSend>
\t\t\t</OutputPin>
\t\t\t\t<ReadyToSend>
\t\t\t\t\t<![CDATA[ 
\t\t\t\t\t\t*readyToSend=0;
\t\t\t\t\t\tif(deviceState->fireValue){{
\t\t\t\t\t\t\t*readyToSend |= RTS_FLAG_fire;
\t\t\t\t\t\t}}
\t\t\t\t\t]]>
\t\t\t\t</ReadyToSend> 
\t\t\t</DeviceType>"""

def graphGenBarrier(name : str, devices : str, maxt: int) -> str:
    """
    Generate the XML for the entire graph, takes the devices and edges and attaches everyting together.

    Barrier version.
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
\t\t\tfloat grngOG(uint32_t &state)
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

// NEW SHIT

float const pi = 3.14159265358979323846;
float const two_pi = 2.0 * pi;
float const half_pi = 0.5 * pi;

float cosineCalc1(float x)
{{
    const float c1 = 0.9999932946;
    const float c2 = -0.4999124376;
    const float c3 = 0.0414877472;
    const float c4 = -0.0012712095;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * (c3 + c4 * x2)));
}}

float cosineCalc(float x)
{{
    const float c1 = 0.99940307;
    const float c2 = -0.49558072;
    const float c3 = 0.03679168;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * c3));
}}

// Driver for cosine function, simplifies maths
float cosine(float x)
{{
    //return cos(x);
    int quad; // quadrant

    
    // float modulo to get rid of x > 2pi
    while (x > two_pi)
        x -= two_pi;

    // cos -x = cos x
    if (x < 0)
        x = -x;
    

    quad = int(x/half_pi);
    switch (quad) {{
        case 0:
            return cosineCalc(x);
        case 1:
            return -cosineCalc(pi-x);
        case 2:
            return -cosineCalc(x-pi);
        case 3:
            return cosineCalc(two_pi-x);
    }}
}}

// sine is just cosine shifted by half pi
float sine(float x)
{{
    return cosine(half_pi - x);
}}

float logarithm(float x)
{{
    union {{ float f; uint32_t i; }} vx = {{ x }};
    union {{ uint32_t i; float f; }} mx = {{ (vx.i & 0x007FFFFF) | 0x3f000000 }};
  
    float y = vx.i;
    y *= 1.1920928955078125e-7f;

    return y - 124.22551499f
           - 1.498030302f * mx.f 
           - 1.72587999f / (0.3520887068f + mx.f);
}}

float squareroot(float x)
{{
   unsigned int i = *(unsigned int*) &x; 
   // adjust bias
   i  += 127 << 23;
   // approximation of square root
   i >>= 1; 
   return *(float*) &i;
}}

float grng(uint32_t &state)
{{
	float mu = 0, sigma = 1;
	static const float epsilon = 1.7e-37;
	// static const double two_pi = 2.0*3.14159265358979323846;

	thread_local float z1;
	thread_local bool generate;
	generate = !generate;

	if (!generate)
	   return z1 * sigma + mu;

	float u1, u2;

    do
    {{
        u1 = (float)urng(state) / 4294967295.0f;
        u2 = (float)urng(state) / 4294967295.0f;
    }}
    while (u1 <= epsilon);

	float z0;
	z0 = squareroot(-2.0 * logarithm(u1)) * cosine(two_pi * u2);
	z1 = squareroot(-2.0 * logarithm(u1)) * sine(two_pi * u2);

	return z0 * sigma + mu;
}}

\t\t\t]]>
\t\t</SharedCode> 
\t\t<MessageTypes> 
\t\t\t<MessageType id="spike"> 
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
\t\t</Properties>"""



