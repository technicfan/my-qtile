#!/bin/bash

for model in $(ollama ps | awk 'NR!=1 {print $1}'); do ollama stop "$model"; done