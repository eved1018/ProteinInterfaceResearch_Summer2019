#!/bin/bash
for i in ~/Desktop/Research_Mordechai/Data_Files/Dock_freq/*.docking_freq
  do j="${i%.docking_freq}"
     mv "$i" "${j^^}.docking_freq"
  done
  
