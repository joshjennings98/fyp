python3 test_network.py

graph_schema-4.2.0/tools/compile_graph_as_provider.sh test_network.xml

mv -f test_network.graph.so graph_schema-4.2.0/providers

cd graph_schema-4.2.0

bin/epoch_sim /home/josh/fyp/test_network.xml

cd ..

