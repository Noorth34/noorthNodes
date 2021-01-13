import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from maya.cmds import listConnections, setAttr, flushUndo


class DynLockAttribute(OpenMayaMPx.MPxNode):

	API_VERSION = "Any"
	NODE_NAME = "dynLockAttribute"
	NODE_ID = OpenMaya.MTypeId(0x100fff)

	PLUGIN_VERSION = "0.0.1"
	AUTHOR = "Gabriel Vidal"

	REGISTER_SUCCESS_MESSAGE = "Plugin registered successfully: {}\n".format(NODE_NAME)
	DEREGISTER_SUCCESS_MESSAGE = "Plugin deregistered successfully: {}\n".format(NODE_NAME)

	REGISTER_FAILURE_MESSAGE = "Failed to register plugin: {}\n".format(NODE_NAME)
	DEREGISTER_FAILURE_MESSAGE = "Failed to deregister plugin: {}\n".format(NODE_NAME)

	input = OpenMaya.MObject()


	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)


	def compute(self, plug, dataBlock):
		
		if plug == DynLockAttribute.connectedAttr:

			dataHandleInput = dataBlock.inputValue(DynLockAttribute.input)
			inputValue = dataHandleInput.asFloat()

			list_connected_attr = listConnections("{}.input".format(self.name()), plugs=True)

			if list_connected_attr:
				connected_attr = list_connected_attr[0]

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

				dataBlock.setClean(plug)

		else:
			return OpenMaya.kUnknownParameter


	@staticmethod
	def _create_node():
		return OpenMayaMPx.asMPxPtr(DynLockAttribute())


	@staticmethod
	def _initialize_node():

		mFnAttr_input = OpenMaya.MFnNumericAttribute()
		mFnAttr_weight = OpenMaya.MFnNumericAttribute()
		mFnAttr_connectedAttr = OpenMaya.MFnTypedAttribute()

		DynLockAttribute.input = mFnAttr_input.create("input", "in", OpenMaya.MFnNumericData.kFloat, 0.0)

		mFnAttr_input.setReadable(True)
		mFnAttr_input.setWritable(True)
		mFnAttr_input.setStorable(True)
		mFnAttr_input.setKeyable(False)

		DynLockAttribute.weight = mFnAttr_weight.create("weight", "wgt", OpenMaya.MFnNumericData.kFloat)

		mFnAttr_weight.setReadable(True)
		mFnAttr_weight.setWritable(True)
		mFnAttr_weight.setStorable(True)
		mFnAttr_weight.setKeyable(False)

		DynLockAttribute.connectedAttr = mFnAttr_connectedAttr.create("attribute_to_lock", "atl", OpenMaya.MFnData.kString )

		mFnAttr_connectedAttr.setReadable(True)
		mFnAttr_connectedAttr.setWritable(True)
		mFnAttr_connectedAttr.setStorable(True)
		mFnAttr_connectedAttr.setKeyable(False)

		DynLockAttribute.addAttribute(DynLockAttribute.input)
		DynLockAttribute.addAttribute(DynLockAttribute.weight)
		DynLockAttribute.addAttribute(DynLockAttribute.connectedAttr)

		mFnAttr_input.addToCategory("Hi Darling")
		mFnAttr_connectedAttr.addToCategory("Hi Darling")
		mFnAttr_weight.addToCategory("Hi Darling")

		DynLockAttribute.attributeAffects(DynLockAttribute.input, DynLockAttribute.connectedAttr)
		DynLockAttribute.attributeAffects(DynLockAttribute.weight, DynLockAttribute.connectedAttr)


def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject,
    								DynLockAttribute.AUTHOR,
    								DynLockAttribute.PLUGIN_VERSION,
    								"Any")

    try:
        mplugin.registerNode(DynLockAttribute.NODE_NAME,
        					 DynLockAttribute.NODE_ID,
        					 DynLockAttribute._create_node,
        					 DynLockAttribute._initialize_node,
        					 OpenMayaMPx.MPxNode.kDependNode)

    	sys.stdout.write(DynLockAttribute.REGISTER_SUCCESS_MESSAGE)

    except:
        sys.stderr.write(DynLockAttribute.REGISTER_FAILURE_MESSAGE)


def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin.deregisterNode( DynLockAttribute.NODE_ID )
        sys.stdout.write(DynLockAttribute.DEREGISTER_SUCCESS_MESSAGE)

    except:
        sys.stderr.write(DynLockAttribute.DEREGISTER_FAILURE_MESSAGE)