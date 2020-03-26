
# Compile network
graph_schema-4.2.0/tools/compile_graph_as_provider.sh test_clock2.xml
# graph_schema-4.2.0/tools/compile_graph_as_provider.sh $1.xml


# Remove old compiled graph
rm -f graph_schema-4.2.0/providers/clocked_izhikevich.graph.so
# rm -f graph_schema-4.2.0/providers/$1.graph.so

# Move new compiled graph to providers
mv clocked_izhikevich.graph.so graph_schema-4.2.0/providers
# mv $1.graph.so graph_schema-4.2.0/providers

# CD into graph_schema thing because I can't do it directly
cd graph_schema-4.2.0

# Run epoch_sim
bin/epoch_sim /home/josh/fyp/test_clock2.xml 2> ../log_clocked_epoch.txt

# Run graph_sim
bin/graph_sim /home/josh/fyp/test_clock2.xml 2> ../log_clocked_graph.txt

# Go back to the main directory
cd ..

#python3 visualisation.py

