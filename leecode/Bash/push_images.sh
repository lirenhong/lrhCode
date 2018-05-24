#!bin/bash

echo_r() {
    [ $# -ne 1 ] && return 0
    echo -e "\033[31m$1\033[0m"
}

echo_g() {
    [ $# -ne 1 ] && return 0
    echo -e "\033[32m$1\033[0m"
}

echo_y() {
    [ $# -ne 1 ] && return 0
    echo -e "\033[33m$1\033[0m"
}

echo_b() {
    [ $# -ne 1 ] && return 0
    echo -e "\033[34m$1\033[0m"
}

echo_r() {
    [ $# -ne 1 ] && return 0
    echo -e "\033[31m$1\033[0m"
}

usage() {
    docker images
    echo "Usage: $0 registry1:tag1 [registry2:tag2...]"
}



