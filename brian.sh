rm brianTest.txt

echo "BRIAN TEST SCRIPT\n"
echo "Running 10 neuron test."
echo "BRIAN 10 Neurons:\n" >> brianTest.txt

python3 izhikevich_brian_cpp.py 10 false >> brianTest.txt

echo "10 neuron test complete.\n"
echo "Running 100 neuron test."
echo "BRIAN 100 Neurons:\n" >> brianTest.txt

python3 izhikevich_brian_cpp.py 100 false >> brianTest.txt

echo "100 neuron test complete.\n"
echo "Running 1000 neuron test."
echo "BRIAN 1000 Neurons:\n" >> brianTest.txt

python3 izhikevich_brian_cpp.py 1000 false >> brianTest.txt

echo "1000 neuron test complete.\n"
echo "Running 10000 neuron test."
echo "BRIAN 10000 Neurons:\n" >> brianTest.txt

python3 izhikevich_brian_cpp.py 10000 false >> brianTest.txt

echo "10000 neuron test complete.\n"
echo "Running 100000 neuron test."
echo "BRIAN 100000 Neurons:\n" >> brianTest.txt

python3 izhikevich_brian_cpp.py 100000 false >> brianTest.txt

echo "100000 neuron test complete.\n"
echo "All BRIAN tests complete."
