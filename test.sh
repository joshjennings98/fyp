# Generate network
python3 test_generator_1.py

# Compile network
graph_schema-4.2.0/tools/compile_graph_as_provider.sh test_network.xml

# Remove old compiled graph
rm -f graph_schema-4.2.0/providers/test_network.graph.so

# Move new compiled graph to providers
mv test_network.graph.so graph_schema-4.2.0/providers

# CD into graph_schema thing because I can't do it directly
cd graph_schema-4.2.0

# Run epoch_sim
bin/epoch_sim /home/josh/fyp/test_network.xml

# Go back to the main directory
cd ..

