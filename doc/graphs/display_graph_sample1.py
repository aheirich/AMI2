#
# display graph sample1
#
# scale cspad intensities according to average pixel intensity in ROI
#

import AMI_graph as AMI

def displayGraph(collectorResult):
  meanIntensity = collectorResult[ 'cspadMeanIntensity' ]
  cspad = collectorResult[ 'cspad' ]
  scaledCspad = AMI.scaleCspad(cspad, 1.0 / meanIntensity)
  return {'stripChartBuffer' : collectorResult[ 'stripChartBuffer' ], 'timeAveragedStripChartBuffer' : collectorResult[ 'timeAveragedStripChartBuffer' ], 'cspad' : collectorResult[ 'cspad' ], 'cspadMeanIntensity' : collectorResult[ 'cspadMeanIntensity' ] }

collectorResult = AMI.getCollectorResult()
AMI.displayResultIs(displayGraph(collectorResult))
