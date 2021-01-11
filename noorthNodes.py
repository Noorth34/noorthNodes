import sys
import math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


nodeSqrt = "Sqrt"
nodeSqrtId = OpenMaya.MTypeId(0x100fff)

nodeReadVal = "ReadVal"
nodeReadValId = OpenMaya.MTypeId(0x101fff)

class Sqrt(OpenMayaMPx.MPxNode):

	input = OpenMaya.MObject()
	output = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute(self, plug, dataBlock):
		
		if plug == Sqrt.output:

			dataHandleInput = dataBlock.inputValue(Sqrt.input)
			inputValue = dataHandleInput.asFloat()

			output = math.sqrt(inputValue)

			dataHandleOutput = dataBlock.outputValue(Sqrt.output)
			dataHandleOutput.setFloat(output)

			dataBlock.setClean(plug)

		else:
			return OpenMaya.kUnknownParameter


class ReadVal(OpenMayaMPx.MPxNode):

	input = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute(self, plug, dataBlock):

		if plug == ReadVal.input:
			dataHandleInput = dataBlock.inputValue(ReadVal.input)
			value = dataHandleInput.asFloat()
			dataHandleInput.setFloat(value)
			dataBlock.setClean()

		else:
			return OpenMaya.kUnknownParameter


def node_sqrt_creator():
	return OpenMayaMPx.asMPxPtr(Sqrt())

def node_readval_creator():
	return OpenMayaMPx.asMPxPtr(ReadVal())


def node_sqrt_initialize():

	mFnAttr = OpenMaya.MFnNumericAttribute()

	Sqrt.input = mFnAttr.create("input", "in", OpenMaya.MFnNumericData.kFloat, 0.0)

	mFnAttr.setReadable(True)
	mFnAttr.setWritable(True)
	mFnAttr.setStorable(True)
	mFnAttr.setKeyable(True)

	Sqrt.output = mFnAttr.create("output", "out", OpenMaya.MFnNumericData.kFloat)

	mFnAttr.setReadable(True)
	mFnAttr.setWritable(False)
	mFnAttr.setStorable(False)
	mFnAttr.setKeyable(False)

	Sqrt.addAttribute(Sqrt.input)
	Sqrt.addAttribute(Sqrt.output)

	Sqrt.attributeAffects(Sqrt.input, Sqrt.output)


def node_readval_initialize():

	mFnAttr = OpenMaya.MFnNumericAttribute()

	ReadVal.input = mFnAttr.create("input", "in", OpenMaya.MFnNumericData.kFloat, 0.0)

	mFnAttr.setReadable(True)
	mFnAttr.setWritable(True)
	mFnAttr.setStorable(True)
	mFnAttr.setKeyable(True)

	ReadVal.addAttribute(ReadVal.input)


def initializePlugin(mobject):
    mplugin_sqrt = OpenMayaMPx.MFnPlugin(mobject)
    mplugin_readval = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin_sqrt.registerNode(nodeSqrt, nodeSqrtId , node_sqrt_creator, node_sqrt_initialize )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % nodeSqrt )

    try:
        mplugin_readval.registerNode(nodeReadVal, nodeReadValId , node_readval_creator, node_readval_initialize )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % nodeReadVal )


def uninitializePlugin(mobject):
    mplugin_sqrt = OpenMayaMPx.MFnPlugin(mobject)
    mplugin_readval = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin_sqrt.deregisterCommand( nodeSqrt )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % nodeSqrt )

    try:
        mplugin_readval.deregisterCommand( nodeReadVal )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % nodeReadVal )