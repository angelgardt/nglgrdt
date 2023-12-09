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
  	
		# check docs dir exists
  	if [ -d docs ]; then
  	# remove and created empty if does
  	    rm -rf docs
    	  echo -e "-----"
  			echo -e "${BLUE}docs directory removed${NC}"
  			echo -e "-----"
    	  mkdir docs
    	  touch docs/README.md
    	  echo -e "-----"
    	  echo -e "${BLUE}docs directory created${NC}"
    	  echo -e "-----"
    else 
		# create if not
		    mkdir docs
    	  touch docs/README.md
    	  echo -e "-----"
    	  echo -e "${BLUE}docs directory created${NC}"
    	  echo -e "-----"
  	fi
  	
  	if [ "$mode" = "reset" ]; then
  	    
  			ls -Ral docs
			  echo -e "${GREEN}=====${NC}"
			  echo -e "${GREEN}Reset completed${NC}"
			  echo -e "Now your docs directory contains only empty README.md file"
			  echo -e "${GREEN}=====${NC}"
		
		elif [ "$mode" = "update" ]; then
		    
		    {
		        # try
		        cp -R -v `echo _site/*` `echo docs`
		    } || {
		        # catch
		        echo -e "${RED}=====${NC}"
					  echo -e "${RED}Deploy not completed${NC}"
					  echo -e "${RED}File copying error${NC}"
					  echo -e "${RED}=====${NC}"
					  exit
		    }
		    
		    echo -e "-----"
				echo -e ${GRAY}"_site" ${BLUE}copied${NC}
				echo -e "-----"
		
		else
		
		    echo -e "${RED}=====${NC}"
		    echo -e "${RED}Deploy not completed${NC}"
		    echo -e "${RED}Unknown first inline argument${NC}"
		    echo -e "Valid options are ${GRAY}update${NC} (default) or ${GRAY}reset${NC}"
		    echo -e "${RED}=====${NC}"
		    exit
		    
		fi
		
		# print list of docs files
		ls -Ral docs
			
		# print deploy success
		echo -e "${GREEN}=====${NC}"
		echo -e "${GREEN}Deploy completed${NC}"
		echo -e "${GREEN}=====${NC}"
  
}

deployer $1