#!/bin/bash

function deployer {
  
  set -e
  
  # set colors
  RED='\033[0;31m'
	BLUE='\033[0;34m'
	GREEN='\033[0;32m'
	GRAY='\033[0;37m'
	NC='\033[0m' # No Color
	
	# pass inline arg to var
	mode="${1:-update}"
	
	echo $mode
  
}

deployer $1