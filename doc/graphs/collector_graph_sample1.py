#
# collector graph sample1
#
# downsample data to display rate
# collect stripchart display points
also compute average across time
#

import AMI_graph as AMI

stripChartBuffer = []
stripChartBufferWidth = 128
stripChartBufferRollingSum = 0
timeAveragedStripChartBuffer = []
timeAveragedStripChartBufferWidth = 128

def collectorGraph(computationResult):

  if len(stripChartBuffer) >= stripChartBufferWidth:
    stripChartBufferRollingSum = stripChartBufferRollingSum - stripChartBuffer[0]
    stripChartBuffer = stripChartBuffer[1:]
  meanIntensity = computationResult[ 'cspadMeanIntensity' ]
  stripChartBuffer.append(meanIntensity)
  stripChartBufferRollingSum = stripChartBufferRollingSum + meanIntensity

  if len(timeAveragedStripChartBuffer) >= timeAveragedStripChartBufferWidth:
    timeAveragedStripChartBuffer = timeAveragedStripChartBuffer[1:]
  timeAveragedStripChartBuffer.append(stripChartBufferRollingSum / len(stripChartBuffer))

  return { 'stripChartBuffer' : stripChartBuffer, 'timeAveragedStripChartBuffer' : timeAveragedStripChartBuffer, 'cspad' : computationResult[ 'cspad' ], 'cspadMeanIntensity' : computationResult[ 'cspadMeanIntensity' ]  }

computationResult = AMI.getComputationResult()
AMI.collectorResultIs(collectorGraph(computationResult))
