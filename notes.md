# Notes

## Old `grng()`

```c++
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
    float f = (acc-60.0f) * scale;
    
    return f; // >= 0 ? f : -1.0 * f;
}
```

Time for run:
```
real    1m36.715s
user    1m36.296s
sys     0m0.331s
```

Number of firings:
```
7348
```

## New `grng()`

```c++
float const pi = 3.14159265358979323846;
float const two_pi = 2.0 * pi;
float const half_pi = 0.5 * pi;

float cosineCalc(float x)
{
    const float c1 = 0.99940307;
    const float c2 = -0.49558072;
    const float c3 = 0.03679168;

    float x2;

    x2 = x * x; // x**2

    return (c1 + x2 * (c2 + x2 * c3));
}

// Driver for cosine function, simplifies maths
float cosine(float x)
{
    //return cos(x);
    int quad; // quadrant

    
    // float modulo to get rid of x > 2pi
    while (x > two_pi)
        x -= two_pi;

    // cos -x = cos x
    if (x < 0)
        x = -x;
    

    quad = int(x/half_pi);
    switch (quad) {
        case 0:
            return cosineCalc(x);
        case 1:
            return -cosineCalc(pi-x);
        case 2:
            return -cosineCalc(x-pi);
        case 3:
            return cosineCalc(two_pi-x);
    }
}

// sine is just cosine shifted by half pi
float sine(float x)
{
    return cosine(half_pi - x);
}

float logarithm(float x)
{
    union { float f; uint32_t i; } vx = { x };
    union { uint32_t i; float f; } mx = { (vx.i & 0x007FFFFF) | 0x3f000000 };
  
    float y = vx.i;
    y *= 1.1920928955078125e-7f;

    return y - 124.22551499f
           - 1.498030302f * mx.f 
           - 1.72587999f / (0.3520887068f + mx.f);
}

float squareroot(float x)
{
   unsigned int i = *(unsigned int*) &x; 
   // adjust bias
   i  += 127 << 23;
   // approximation of square root
   i >>= 1; 
   return *(float*) &i;
}  

float grng(uint32_t &state)
{
	float mu = 0, sigma = 1;
	static const float epsilon = std::numeric_limits<float>::min();
	// static const double two_pi = 2.0*3.14159265358979323846;

	thread_local float z1;
	thread_local bool generate;
	generate = !generate;

	if (!generate)
	   return z1 * sigma + mu;

	float u1, u2;

    do
    {
        u1 = (float)urng(state) / 4294967295.0f;
        u2 = (float)urng(state) / 4294967295.0f;
    }
    while (u1 <= epsilon);

	float z0;
	z0 = squareroot(-2.0 * logarithm(u1)) * cosine(two_pi * u2);
	z1 = squareroot(-2.0 * logarithm(u1)) * sine(two_pi * u2);

	return z0 * sigma + mu;
}
```

Time for run:
```
real    1m36.763s
user    1m36.236s
sys     0m0.456s
```

Number of firings:
```
12549
```