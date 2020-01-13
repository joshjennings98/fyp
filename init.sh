# Install vagrant and virtualbox
sudo apt install vagrant virtualbox -y

# Set up provision thing
sh graph_schema-4.2.0/provision_ubuntu18.sh

# See if working
cd graph_schema-4.2.0
make test
cd ..

# Run test thing
sh test.sh