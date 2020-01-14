# Generate network
python3 network_generator/main.py

# Compile network
graph_schema-4.2.0/tools/compile_graph_as_provider.sh test_gals.xml

# Remove old compiled graph
rm -f graph_schema-4.2.0/providers/test_gals.graph.so

# Move new compiled graph to providers
mv test_gals.graph.so graph_schema-4.2.0/providers

# CD into graph_schema thing because I can't do it directly
cd graph_schema-4.2.0

# Run epoch_sim
bin/epoch_sim /home/josh/fyp/test_gals.xml

# Go back to the main directory
cd ..

