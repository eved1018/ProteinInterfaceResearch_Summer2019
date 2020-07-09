#!/bin/sh

cd /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Star
awk 'FNR <= 5244' RFStarinterface.csv >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Star/head1RFStarinterface.csv
awk 'FNR <= 5244' RFStarnoninterface.csv >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Star/head1RFStarnoninterface.csv
awk 'FNR <= 5244' logStarinterface.csv >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Star/head1logStarinterface.csv
awk 'FNR <= 5244' logStarnoninterface.csv >> /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/Logistic_regresion_corrected/CrossVal/Star/head1logStarnoninterface.csv