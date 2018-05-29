#
# computation graph sample1
#
# display cspad image
# compute average pixel intensity in ROI, display in stripchart
# scale cspad image according to average pixel intensity (in the client)
#

import AMI_graph as AMI

cspadSum = numpy.array([ 0 ])
nextDisplayableTimestamp = 0
displayInterval = 10 # units

def computationGraph(telemetryFrame):
  timestamp = telemetryFrame[ 'timestamp' ]
  cspad = telemetryFrame[ 'cspad' ]
  cspadSum = AMI.mergeCspad(cspad, cspadSum)
  cspadROI = [ 100, 100, 200, 200 ]
  meanPixelIntensity = AMI.meanPixelIntensity(cspad, cspadROI)
  
  global nextDisplayableTimestamp
  if timestamp >= nextDisplayableTimestamp:
    nextDisplayableTimestamp = nextDisplayableTimestamp + displayInterval
    return { 'timestamp' : 0, 'cspad' : cspad, 'cspadMeanIntensity' : meanPixelIntensity }
  else:
    return {}

telemetryFrame = AMI.ingestTelemetryFrame()
AMI.computationResultIs(computationGraph(telemetryFrame))
