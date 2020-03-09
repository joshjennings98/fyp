# Generate network
python3 network_generator/main.py $1

# Compile network
graph_schema-4.2.0/tools/compile_graph_as_provider.sh $1.xml

# Remove old compiled graph
rm -f graph_schema-4.2.0/providers/$1.graph.so

# Move new compiled graph to providers
mv $1.graph.so graph_schema-4.2.0/providers

# CD into graph_schema thing because I can't do it directly
cd graph_schema-4.2.0

# Run epoch_sim
bin/epoch_sim /home/josh/fyp/$1.xml

# Go back to the main directory
cd ..

