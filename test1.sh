# Generate network
if [ $# -lt 2 ];
then
    python3 network_generator/nonConfigInitExample.py
    graph_schema-4.2.0/tools/compile_graph_as_provider.sh test_network.xml
    rm -f graph_schema-4.2.0/providers/test_network.graph.so
    mv test_network.graph.so graph_schema-4.2.0/providers
    cd graph_schema-4.2.0
    bin/epoch_sim /home/josh/fyp/test_network.xml
    cd ..
    exit 1
else
    python3 network_generator/main.py $2
    echo "nothing"
fi

# Compile network
graph_schema-4.2.0/tools/compile_graph_as_provider.sh $1.xml

# Remove old compiled graph
rm -f graph_schema-4.2.0/providers/$1.graph.so

# Move new compiled graph to providers
mv $1.graph.so graph_schema-4.2.0/providers

# CD into graph_schema thing because I can't do it directly
cd graph_schema-4.2.0

rm ../log.txt

# Run epoch_sim
bin/epoch_sim /home/josh/fyp/$1.xml 2> ../log2.txt

# Go back to the main directory
cd ..

python3 visualisation.py

