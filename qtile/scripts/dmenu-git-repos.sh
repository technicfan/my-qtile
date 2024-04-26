#!/bin/bash

main()
{
    chosen=$( (find "$HOME/git-repos" -mindepth 1 -maxdepth 1 -type d && find "$HOME/GitHub" -mindepth 1 -maxdepth 1 -type d) | sort -u | $DMENU 'Choose repo:')
    if [[ -n "$chosen" ]]
    then
        vscodium "$chosen"
    fi
}

main