#!/bin/bash
mkdir -p $HOME/.janus
mkdir -p $HOME/.janus/lib
if [ $# -ge 1 ]
then
	if [ "$1" = "-h" ] || [ "$1" = "--help" ]
	then
		echo "install_plantuml Usage: install_plantuml.sh [VERSION]"
		echo "Default version 1.2024.6"
		exit
	else
		VERSION=$1
	fi
else
	VERSION=1.2024.6
fi
wget -O $HOME/.janus/lib/plantuml.jar https://github.com/plantuml/plantuml/releases/download/v${VERSION}/plantuml-mit-${VERSION}.jar
