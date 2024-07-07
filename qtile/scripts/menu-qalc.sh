#!/bin/bash

# taken from https://github.com/BarbUk/menu-qalc
# and modified for own needs

usage()
{
    echo "$(tput bold)menu-calc$(tput sgr0)"
    echo "A calculator for Rofi/dmenu(2)"
    echo
    echo "$(tput bold)Usage:$(tput sgr0)"
    echo "    = 4+2"
    echo "    = (4+2)/(4+3)"
    echo "    = 4^2"
    echo "    = sqrt(4)"
    echo "    = c(2)"
    echo "    = anything(ANS) -> ANS gets replaced with the result of previous calculation"
    echo
    echo "$(tput bold)Force Rofi/dmenu(2):$(tput sgr0)"
    echo "By default, if rofi exists, it will be used. To force menu-calc to"
    echo "use one or the other, use the --dmenu argument"
    echo
    echo "    = --dmenu=<dmenu_executable>"
    echo
    echo "The answer can be copied to the clipboard and used for further calculations inside (or outside) Rofi/dmenu."
    echo
    echo "If launched outside of Rofi/dmenu the expression may need quotation marks."
    exit
}

# Process CLI parameters
for arg in "$@"
do
    case $arg in
    -h|--help)
        usage
        ;;
    -d=*|--dmenu=*)
        menu=$(echo "$arg" | awk -F "=" '{print $2}')
        ;;
    esac
done

# Grab the answer
if [ -n "$1" ]
then
    answer=$(qalc +u8 -t "$1")
fi

# Path to menu application
if [ -z "$menu" ]
then
    if [[ -n $(command -v dmenu) ]]
    then
        menu=$(command -v dmenu)
    else
        >&2 echo "dmenu not found and no other menu specified"
        exit
    fi
fi

action=$(echo -e "Copy to clipboard\nClear" | $menu -p "= $answer")

# check if ANS in action and replace it
if [[ "$action" = *"ANS"* && -n "$answer" ]]
then
    action=${action//ANS/$answer}
	answer=""
fi

case $action in
"Clear")
    $0
    ;;
"Copy to clipboard")
    echo -n "$answer" | xclip -selection clipboard
    ;;
"")
    ;;
*)
    $0 "$answer $action" "--dmenu=$menu"
    ;;
esac
