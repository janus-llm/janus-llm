#!/bin/bash
mkdir -p $HOME/.janus
mkdir -p $HOME/.janus/bin
mkdir -p $HOME/.janus/lib
script_dir=$(dirname $0)
wget -O $HOME/.janus/lib/plantuml.jar https://github.com/plantuml/plantuml/releases/download/v1.2024.6/plantuml-mit-1.2024.6.jar
#cp $script_dir/plantuml $HOME/.janus/bin
#chmod +x $HOME/.janus/bin/plantuml
#echo "add PATH=\$PATH:$HOME/.janus/bin to your .bashrc or .zshrc file"
