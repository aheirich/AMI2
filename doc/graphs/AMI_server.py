#
# AMI_server.py
#

import numpy
import AMI_common as AMI

def computationGraph():
  return AMI.receiveGraphByClass('ComputationGraph')

def collectorGraph():
  return AMI.receiveGraphByClass('CollectorGraph')

def displayGraph():
  return AMI.receiveGraphByClass('DisplayGraph')

def ingestTelemetryFrame():
  return {} # TODO

