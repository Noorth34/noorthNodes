import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from maya.cmds import listConnections, setAttr, flushUndo

node_name = "DynLockAttribute"
node_id = OpenMaya.MTypeId(0x100fff)

class DynLockAttribute(OpenMayaMPx.MPxNode):

	input = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute(self, plug, dataBlock):
		
		if plug == DynLockAttribute.connectedAttr:

			dataHandleInput = dataBlock.inputValue(DynLockAttribute.input)
			inputValue = dataHandleInput.asFloat()
			# dataHandleInput = dataBlock.inputValue(Sqrt.input)
			# inputValue = dataHandleInput.asFloat()

			list_connected_attr = listConnections("{}.input".format(self.name()), plugs=True)

			if list_connected_attr:
				connected_attr = list_connected_attr[0]
				# output = math.sqrt(inputValue)

				dataBlockHandleOutput = dataBlock.outputValue(DynLockAttribute.connectedAttr)
				dataBlockHandleOutput.setString(connected_attr)

				dataHandleWeight = dataBlock.inputValue(DynLockAttribute.weight)
				weight = dataHandleWeight.asFloat()

				if weight == 1:
					setAttr(connected_attr, lock=True)
				elif weight == 0:
					setAttr(connected_attr, lock=False)
				else:
					pass
				# dataHandleOutput = dataBlock.outputValue(Sqrt.output)
				# dataHandleOutput.setFloat(output)

				dataBlock.setClean(plug)

		else:
			return OpenMaya.kUnknownParameter


def node_dynlockattribute_creator():
	return OpenMayaMPx.asMPxPtr(DynLockAttribute())


def node_dynlockattribute_initialize():

	mFnAttr_input = OpenMaya.MFnNumericAttribute()
	mFnAttr_weight = OpenMaya.MFnNumericAttribute()
	mFnAttr_connectedAttr = OpenMaya.MFnTypedAttribute()

	DynLockAttribute.input = mFnAttr_input.create("input", "in", OpenMaya.MFnNumericData.kFloat, 0.0)
	# DynLockAttribute.input = mFnAttr_input.create("input", "in", 0)
	# mFnAttr_input.addField("None", 0)

	mFnAttr_input.setReadable(True)
	mFnAttr_input.setWritable(True)
	mFnAttr_input.setStorable(True)
	mFnAttr_input.setKeyable(False)

	DynLockAttribute.weight = mFnAttr_weight.create("weight", "wgt", OpenMaya.MFnNumericData.kFloat)

	DynLockAttribute.connectedAttr = mFnAttr_connectedAttr.create("attribute_to_lock", "atl", OpenMaya.MFnData.kString )

	mFnAttr_connectedAttr.setReadable(True)
	mFnAttr_connectedAttr.setWritable(True)
	mFnAttr_connectedAttr.setStorable(True)
	mFnAttr_connectedAttr.setKeyable(False)

	DynLockAttribute.addAttribute(DynLockAttribute.input)
	DynLockAttribute.addAttribute(DynLockAttribute.weight)
	DynLockAttribute.addAttribute(DynLockAttribute.connectedAttr)

	DynLockAttribute.attributeAffects(DynLockAttribute.input, DynLockAttribute.connectedAttr)
	DynLockAttribute.attributeAffects(DynLockAttribute.weight, DynLockAttribute.connectedAttr)


def initializePlugin(mobject):
    mplugin_dynlockattribute = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin_dynlockattribute.registerNode(node_name, node_id , node_dynlockattribute_creator, node_dynlockattribute_initialize )
    except:
        sys.stderr.write( "Failed to register command: {}".format(node_name) )


def uninitializePlugin(mobject):
    mplugin_dynlockattribute = OpenMayaMPx.MFnPlugin(mobject)

    try:
    	flushUndo()
        mplugin_dynlockattribute.deregisterNode( node_id )
    except:
        sys.stderr.write( "Failed to unregister command: {}".format(node_name) )