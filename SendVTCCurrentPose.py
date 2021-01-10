#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file SendVTCCurrentPose.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import math
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
from send_zmq import req

INIT_POSE_X = 261.149453125
INIT_POSE_Y = 150.492119140625


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
sendvtccurrentpose_spec = ["implementation_id", "SendVTCCurrentPose",
		 "type_name",         "SendVTCCurrentPose",
		 "description",       "ModuleDescription",
		 "version",           "1.0.0",
		 "vendor",            "maruryota",
		 "category",          "Category",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 "conf.default.host", "localhost",
		 "conf.default.port", "54321",
		 "conf.default.endpoint", "PuffinBP_2",

		 "conf.__widget__.host", "text",
		 "conf.__widget__.port", "text",
		 "conf.__widget__.endpoint", "text",

         "conf.__type__.host", "string",
         "conf.__type__.port", "string",
         "conf.__type__.endpoint", "string",

		 ""]
# </rtc-template>

##
# @class SendVTCCurrentPose
# @brief ModuleDescription
#
#
class SendVTCCurrentPose(OpenRTM_aist.DataFlowComponentBase):

	##
	# @brief constructor
	# @param manager Maneger Object
	#
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_currentPose = OpenRTM_aist.instantiateDataType(RTC.TimedPose2D)
		"""
		"""
		self._currentPoseOut = OpenRTM_aist.OutPort("currentPose", self._d_currentPose)





		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  host
		 - DefaultValue: localhost
		"""
		self._host = ['localhost']
		"""
		
		 - Name:  port
		 - DefaultValue: 54321
		"""
		self._port = ['54321']
		"""
		
		 - Name:  endpoint
		 - DefaultValue: PuffinBP_2
		"""
		self._endpoint = ['PuffinBP_2']

		# </rtc-template>



	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry()
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("host", self._host, "localhost")
		self.bindParameter("port", self._port, "54321")
		self.bindParameter("endpoint", self._endpoint, "PuffinBP_2")

		# Set InPort buffers

		# Set OutPort buffers
		self.addOutPort("currentPose",self._currentPoseOut)

		# Set service provider to Ports

		# Set service consumers to Ports

		# Set CORBA Service Ports

		return RTC.RTC_OK

	###
	##
	## The finalize action (on ALIVE->END transition)
	## formaer rtc_exiting_entry()
	##
	## @return RTC::ReturnCode_t
	#
	##
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK

	###
	##
	## The startup action when ExecutionContext startup
	## former rtc_starting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The shutdown action when ExecutionContext stop
	## former rtc_stopping_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK

	##
	#
	# The activated action (Active state entry action)
	# former rtc_active_entry()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onActivated(self, ec_id):
		self.send_zmq_req = req.SendZMQRequest(
			host = self._host[0],
			port = self._port[0]
		)

		return RTC.RTC_OK

	###
	##
	## The deactivated action (Active state exit action)
	## former rtc_active_exit()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK

	##
	#
	# The execution action that is invoked periodically
	# former rtc_active_do()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onExecute(self, ec_id):
		ret = self.send_zmq_req.receive_data()
		data = ret["Report"]["Data"]
		self._d_currentPose.data.heading = float(data["yaw"]) * math.pi / 180  # [rad]
		self._d_currentPose.data.position.x = float(data["position"]["x"]) / 100 - INIT_POSE_X  # [m]
		self._d_currentPose.data.position.y = float(data["position"]["y"]) / 100 - INIT_POSE_Y  # [m]
		print(self._d_currentPose)
		self._currentPoseOut.write()
	
		return RTC.RTC_OK

	###
	##
	## The aborting action when main logic error occurred.
	## former rtc_aborting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The error action in ERROR state
	## former rtc_error_do()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The reset action that is invoked resetting
	## This is same but different the former rtc_init_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The state update action that is invoked after onExecute() action
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##

	##
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The action that is invoked when execution context's rate is changed
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK




def SendVTCCurrentPoseInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=sendvtccurrentpose_spec)
    manager.registerFactory(profile,
                            SendVTCCurrentPose,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    SendVTCCurrentPoseInit(manager)

    # Create a component
    comp = manager.createComponent("SendVTCCurrentPose")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

