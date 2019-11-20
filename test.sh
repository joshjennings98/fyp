python3 test_generator.py

tools/compile_graph_as_provider.sh test_network.xml

mv -f test_network.graph.so providers

bin/epoch_sim test_network.xml

