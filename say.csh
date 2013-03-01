#!/bin/csh

set counter=0

while (1) 
    sleep 5

    @ counter = $counter + 5

    echo "I have slept $counter seconds."
end
