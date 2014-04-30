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

data = arcpy.GetParameterAsText(0)
overlay = arcpy.GetParameterAsText(1)
field = arcpy.GetParameterAsText(2)
expression = arcpy.GetParameterAsText(3)        # default value is hard coded as SUM
output = arcpy.GetParameterAsText(4)

# Create field name variables
areaOrig = "AREA"                               # original area
ratio = "RATIO"
newVal = "VAL_" + str(expression)

# Add new field to data features
arcpy.AddField_management(data, areaOrig, "FLOAT")
arcpy.AddMessage("\n" + areaOrig + " field added")

# Calculate area for area field in square meters
arcpy.CalculateField_management(data, areaOrig, "!shape.area@squaremeters!", "PYTHON_9.3", "")
arcpy.AddMessage(areaOrig + " field calculated")

# Identity: computes geometric intersection between two feature classes (intermediate data)
dataSlice = arcpy.Identity_analysis(data, overlay, "in_memory", "NO_FID")
arcpy.AddMessage("Identity tool completed")

# Add ratio field to dataSlice (identity) feature class
arcpy.AddField_management(dataSlice, ratio, "FLOAT")
arcpy.AddMessage(ratio + " field added")

# Calculate ratio of original area to new (slice) area
arcpy.CalculateField_management(dataSlice, "RATIO", "!SHAPE_Area! / !AREA!", "PYTHON_9.3", "")
arcpy.AddMessage(ratio + " field calculated")

# Calculate new field value based on summary method
arcpy.AddField_management(dataSlice, newVal , "FLOAT")

# Create variable for ratio formula
formula = "!" + str(field) + "! * !RATIO!"

# Calculate new value field based on ratio fieldarcpy.CalculateField_management(dataSlice, newVal, formula, "PYTHON_9.3", "")
arcpy.AddMessage("New " + field + " field calculated")

# Spatial join slice and overlay using correct summary method
#-------------------------------------------------------------------------

# Create a new fieldmappings and add the two input feature classes
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(dataSlice)
fieldmappings.addTable(overlay)

fieldIndex = fieldmappings.findFieldMapIndex(newVal)
fieldmap = fieldmappings.getFieldMap(fieldIndex)

#Get the output field's properties as a field object
finalField = fieldmap.outputField

# Rename the field and pass the updated field object back into the field map
finalField.name = "VAL_FINAL"
finalField.aliasName = "Final Value"

# Set the merge rule
#if expression == "MEAN":
#   fieldmap.mergeRule = 'Mean'
#else:
fieldmap.mergeRule = "Sum"

# Replace old field map with the updated one 
fieldmappings.replaceFieldMap(fieldIndex, fieldmap)

#Run the Spatial Join tool
arcpy.SpatialJoin_analysis(overlay, dataSlice, output, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings, "CONTAINS")
arcpy.AddMessage("Spatial Join completed")
arcpy.AddMessage(output + "created")

# Delete area field from data features
# arcpy.DeleteField_management(data, area)
arcpy.AddMessage("\n")
