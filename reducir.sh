!/bin/bash

#Verificar el argumento que se obtiene el argumento del flag -x o
while test $# -gt 0; do
        case "$1" in
            -x)
                shift
                first_argument=$1
                shift
                ;;
            *)
                echo "$1 is not a recognized flag!"
                exit
                ;;
        esac
done

#Verificar la instalacion de python3.6 y ejecutar el Reductor
lines=$(which python3.6|wc -l)
if [ $lines -eq 1 ];
then
    cd Reductor/
    python3.6 main.py $first_argument
else
    apt-get install software-properties-common -y
    add-apt-repository ppa:jonathonf/python-3.6
    apt-get update -y
    apt-get install python3.6 -y
    cd Reductor/
    python3.6 main.py $first_argument
fi
