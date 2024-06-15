#!/bin/bash

checkselected()
{
	for color in ${colors[@]}
	do
		if [[ "$color" = "$1" ]]
		then
			return 0
		fi
	done
	return 1
}

setcolor()
{
	for file in $(ls | grep "$1")
	do
		link=$(echo "$file" | awk -F "-$1" '{print $2}')
		prefix=$(echo "$file" | awk -F "-$1" '{print $1}')
		ln -sfn "$file" "$prefix$link"
	done
}

main()
{
	cd ~/.icons/Gruvbox-Plus-Dark/places/scalable/ || exit 1

	colors=$(ls | grep linux.svg | awk -F "-" '{print $2}' | grep -v .svg)

	selected=$(echo "${colors}" | $DMENU "Icon Colors:")

	if [[ -n $selected ]]
	then
		if checkselected "$selected"
		then
			answer=$(echo -e "No\nYes" | $DMENU "Choose $selected?")
			
			if [[ $answer == "Yes" ]]
			then
				setcolor "$selected"
				notify-send "Your folder icons are now $selected"
				exit 0
			else
				exit 1
			fi
		else
			notify-send "\"$selected\" is not a valid color"
			main
		fi
	else
		exit 0
	fi
}

main
