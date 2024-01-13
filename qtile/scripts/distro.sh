#!/bin/sh

distro=$(distro | grep -n "" | grep -oiP "1:name:\s\K.*")

printf $distro