#
# generateGraphs.py
#

import AMI_graph as AMI



if __name__ == '__main__':

  from PyQt5.QtGui import *
  from PyQt5.QtWidgets import *
  from PyQt5.QtCore import *

  import sys
  import client_sample1
  app = QApplication(sys.argv)
  mainWindow = client_sample1.MainWindow()
  computationGraph = AMI.computationGraph()
  print("computation graph")
  for line in computationGraph:
    print(line)
  collectorGraph = AMI.collectorGraph()
  print("collector graph")
  for line in collectorGraph:
    print(line)
  displayGraph = AMI.displayGraph()
  print("display graph")
  for line in displayGraph:
    print(line)

