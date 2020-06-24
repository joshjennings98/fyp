/*=====================================================================*
 *                   Copyright (C) 2011 Paul Mineiro                   *
 * All rights reserved.                                                *
 *                                                                     *
 * Redistribution and use in source and binary forms, with             *
 * or without modification, are permitted provided that the            *
 * following conditions are met:                                       *
 *                                                                     *
 *     * Redistributions of source code must retain the                *
 *     above copyright notice, this list of conditions and             *
 *     the following disclaimer.                                       *
 *                                                                     *
 *     * Redistributions in binary form must reproduce the             *
 *     above copyright notice, this list of conditions and             *
 *     the following disclaimer in the documentation and/or            *
 *     other materials provided with the distribution.                 *
 *                                                                     *
 *     * Neither the name of Paul Mineiro nor the names                *
 *     of other contributors may be used to endorse or promote         *
 *     products derived from this software without specific            *
 *     prior written permission.                                       *
 *                                                                     *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND              *
 * CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,         *
 * INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES               *
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE             *
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER               *
 * OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,                 *
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES            *
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE           *
 * GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR                *
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF          *
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT           *
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY              *
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE             *
 * POSSIBILITY OF SUCH DAMAGE.                                         *
 *                                                                     *
 * Contact: Paul Mineiro <paul@mineiro.com>                            *
 *=====================================================================*/

#include<iostream>
#include<cmath>
#include<chrono>

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

int main()
{
    /*
    float x;
    double max = 100000000, step = 0.001;

    auto start = std::chrono::high_resolution_clock::now(); 

    for (double i = 0; i < max; i+=step) {
        x = std::log(i);
    }

    auto stop = std::chrono::high_resolution_clock::now(); 

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start); 

    std::cout << "Time for normal function for " << max / step << " evals: " << duration.count() << " microseconds" << std::endl;

    start = std::chrono::high_resolution_clock::now(); 

    for (double i = 0; i < max; i+=step) {
        x = logarithm(i);
    }

    stop = std::chrono::high_resolution_clock::now(); 

    duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start); 

    std::cout << "Time for custom function for " << max / step << " evals: " << duration.count() << " microseconds" << std::endl;
    */
   /*
   std::cout << "yData = [" << std::endl;
    for (float i = 0.0001; i <= 7; i += 0.05) {
        std::cout << "    " << std::abs(logarithm(i) - std::log2(i)) << "," << std::endl;
    }
    std::cout << "]" << std::endl;
    
    std::cout << "xData = [" << std::endl;
    for (float i = 0.0001; i <= 7; i += 0.05) {
        std::cout << "    " << i << "," << std::endl;
    }
    std::cout << "]" << std::endl;
    */
    std::cout << "yLogActual = [" << std::endl;
    for (float i = 0.0001; i <= 7; i += 0.05) {
        std::cout << "    " << std::log2(i) << "," << std::endl;
    }
    std::cout << "]" << std::endl;

    std::cout << "yLogApprox = [" << std::endl;
    for (float i = 0.0001; i <= 7; i += 0.05) {
        std::cout << "    " << logarithm(i) << "," << std::endl;
    }
    std::cout << "]" << std::endl;
    
    return 0;
}

// compile with clear && g++ -O3 testlog.cpp -o testlog && ./testlog