#!/bin/bash
for i in *.docking_freq
  do mv "$i" $(echo "$i" | awk '{ sub(/.docking_freq$/,""); print toupper($0) ".docking_freq" }')
  done
