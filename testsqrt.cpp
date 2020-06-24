#include<iostream>
#include<cmath>
#include<chrono>

float squareroot(float x)
{
   unsigned int i = *(unsigned int*) &x; 
   // adjust bias
   i  += 127 << 23;
   // approximation of square root
   i >>= 1; 
   return *(float*) &i;
}

int main()
{
    /*
    float x;
    double max = 100000000, step = 0.001;
    
    auto start = std::chrono::high_resolution_clock::now(); 

    for (double i = 0; i < max; i+=step) {
        x = std::sqrt(i);
    }

    auto stop = std::chrono::high_resolution_clock::now(); 

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start); 

    std::cout << "Time for normal function for " << max / step << " evals: " << duration.count() << " microseconds" << std::endl;

    start = std::chrono::high_resolution_clock::now(); 

    for (double i = 0; i < max; i+=step) {
        x = squareroot(i);
    }

    stop = std::chrono::high_resolution_clock::now(); 

    duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start); 

    std::cout << "Time for custom function for " << max / step << " evals: " << duration.count() << " microseconds" << std::endl;
    */

    std::cout << "yData = [" << std::endl;
    for (float i = 0; i <= 100; i += 1) {
        std::cout << "    " << std::abs(squareroot(i) - std::sqrt(i)) << "," << std::endl;
    }
    std::cout << "]" << std::endl;
    
    std::cout << "xData = [" << std::endl;
    for (float i = 0; i <= 100; i += 1) {
        std::cout << "    " << i << "," << std::endl;
    }
    std::cout << "]" << std::endl;

    std::cout << "ySqrtActual = [" << std::endl;
    for (float i = 0; i <= 100; i += 1) {
        std::cout << "    " << std::sqrt(i) << "," << std::endl;
    }
    std::cout << "]" << std::endl;

    std::cout << "ySqrtApprox = [" << std::endl;
    for (float i = 0; i <= 100; i += 1) {
        std::cout << "    " << squareroot(i) << "," << std::endl;
    }
    std::cout << "]" << std::endl;

    return 0;
}

// compile with clear && g++ -O3 testsqrt.cpp -o testsqrt && ./testsqrt