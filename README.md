# Hydrochemistry_Apps

## DO Calculator
Recalculates dissolved oxygen values for an entire analysis file.


## QC Table Stats
Provides statistics on specific samples that are contained in an exported .csv from the HyPro QCTable view.

## Hydrology Data Quick QC 
Reads in the exported .csv and .nc files from HyPro, plots the data and allows for a fast visual check of data quality. Flags from both files are also shown in a table, with differences highlighted.

## Baseline and Gain Offset Plotter
Takes in a folder that contains .slk files from a Seal auto analyser. Can plot the baseline offset and gain over time between all the files. Useful for determining if a flow cell is dirty or damaged.

## Iodate Normality
Calculates Iodate standard normality very accurately. Takes into account environmental conditions and corrects for glassware expansion and atmosphere buoyancy. 

## NC to CSV Checker
Checks for differences between the .csv and .nc files that HyPro exports. 

## Time Stamp Generator
Sometimes when running long nutrient analyses, such with underway AA100 analysis, AACE will not produce time stamps in the file. This GUI allows for the generation of these stamps to be pasted into the SLK file.
