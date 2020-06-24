#include<iostream>
#include<cmath>
#include<chrono>

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
    while (x >= two_pi)
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

int main()
{
    
    int x;
    double max = 2 * pi, step = 2 * pi / 26000000;
    /*
    auto start = std::chrono::high_resolution_clock::now(); 

    for (float i = 0; i < max; i+=step) {
        x = std::cos(i);
    }

    auto stop = std::chrono::high_resolution_clock::now(); 

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start); 

    std::cout << "Time for normal function for " << max / step << " evals: " << duration.count() << " microseconds" << std::endl;

    start = std::chrono::high_resolution_clock::now(); 

    for (float i = 0; i < max; i+=step) {
        x = cosine(i);
    }

    stop = std::chrono::high_resolution_clock::now(); 

    duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start); 

    std::cout << "Time for custom function for " << max / step << " evals: " << duration.count() << " microseconds" << std::endl;
    */

    std::cout << "yData = [" << std::endl;
    for (double i = 0; i <= max; i += (max / 20)) {
        std::cout << "    " << std::abs(cosine(i) - std::cos(i)) << "," << std::endl;
    }
    std::cout << "]" << std::endl;
    
    std::cout << "xData = [" << std::endl;
    for (double i = 0; i <= max; i += (max / 20)) {
        std::cout << "    " << i << "," << std::endl;
    }
    std::cout << "]" << std::endl;

    std::cout << "yCosActual = [" << std::endl;
    for (double i = 0; i <= max; i += (max / 20)) {
        std::cout << "    " << std::cos(i) << "," << std::endl;
    }
    std::cout << "]" << std::endl;

    std::cout << "yCosApprox = [" << std::endl;
    for (double i = 0; i <= max; i += (max / 20)) {
        std::cout << "    " << cosine(i) << "," << std::endl;
    }
    std::cout << "]" << std::endl;
    
    return 0;
}

// compile with clear && g++ -O3 testtrig.cpp -o testtrig && ./testtrig