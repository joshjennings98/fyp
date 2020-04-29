
# Compile network
#graph_schema-4.2.0/tools/compile_graph_as_provider.sh test_network.xml
# graph_schema-4.2.0/tools/compile_graph_as_provider.sh $1.xml


# Remove old compiled graph
#rm -f graph_schema-4.2.0/providers/test_network.graph.so
# rm -f graph_schema-4.2.0/providers/$1.graph.so

# Move new compiled graph to providers
#mv test_network.graph.so graph_schema-4.2.0/providers

# CD into graph_schema thing because I can't do it directly
cd graph_schema-4.2.0

# Run epoch_sim
bin/epoch_sim /home/josh/fyp/test_network.xml 2> ../log2.txt

# Go back to the main directory
cd ..

#python3 visualisation.py log2.txt quantity 2000 1000 barrier graph

