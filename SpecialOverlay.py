# ---------------------------------------------------------------------------
# SpecialOverlay.py
# Created on: 2014-04-18
#
# Description: This special tool will append data from one file to another. 
# The input are two polygon files and a field from the input layer (data
# features) to append to the target layer (overlay features).
# ---------------------------------------------------------------------------

import arcpy, sys

# Read in parameters
#  1. Data features
#  2. Overlay Features
#  3. Summary field
#  4. Summary expression
#  5. Output feature class name

data = sys.argv[1]
overlay = sys.argv[2]
field = sys.argv[3]
expression = sys.argv[4]
if expression == '#' or not expression:
    expression = "SUM"
output = sys.argv[5]
