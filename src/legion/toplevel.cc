//
//  toplevel.cc
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#include "toplevel.hpp"


// static members of TopLevelTask
TopLevelTask::TaskIdEnum TopLevelTask::mDataSource;
unsigned TopLevelTask::mNumWorkers;
unsigned TopLevelTask::mNumGraphManagers;
unsigned TopLevelTask::mNumRobustnessMonitors;
FileDataSource TopLevelTask::mFileDataSource;
SharedMemoryDataSource TopLevelTask::mSharedMemoryDataSource;
Worker TopLevelTask::mWorker;
Collector TopLevelTask::mCollector;
GraphManager TopLevelTask::mGraphManager;
RobustnessMonitor TopLevelTask::mRobustnessMonitor;


TopLevelTask::TopLevelTask(){
  mDataSource = FILE_DATA_SOURCE_TASK;
  mNumWorkers = 1;
}

TopLevelTask::~TopLevelTask(){
}


void TopLevelTask::launchTelemetryProcessingTasks(Context ctx, Runtime* runtime) {
  
  Rect<1> launchBounds(0, mNumWorkers - 1);
  ArgumentMap argMap;
  IndexTaskLauncher dataSourceLauncher(mDataSource, launchBounds, TaskArgument(NULL, 0), argMap);
  FutureMap dataSourceFutureMap = runtime->execute_index_space(ctx, dataSourceLauncher);
  ArgumentMap workerArgMap(dataSourceFutureMap);
  IndexTaskLauncher workerLauncher(WORKER_TASK, launchBounds, TaskArgument(NULL, 0), workerArgMap);
  FutureMap workerFutureMap = runtime->execute_index_space(ctx, workerLauncher);
  ArgumentMap collectorArgMap(workerFutureMap);
  IndexTaskLauncher collectorLauncher(COLLECTOR_TASK, launchBounds, TaskArgument(NULL, 0), collectorArgMap);
  FutureMap collectorFutureMap = runtime->execute_index_space(ctx, collectorLauncher);
  
}

void TopLevelTask::launchGraphManagerTask(Context ctx, Runtime* runtime) {
  
  Rect<1> launchBounds(0, mNumGraphManagers - 1);
  ArgumentMap argMap;
  IndexTaskLauncher graphManagerLauncher(GRAPH_MANAGER_TASK, launchBounds, TaskArgument(NULL, 0), argMap);
  FutureMap graphManagerFutureMap = runtime->execute_index_space(ctx, graphManagerLauncher);
  
}

bool TopLevelTask::timeToMonitor() {
  return true;
}

void TopLevelTask::launchRobustnessMonitorTask(Context ctx, Runtime* runtime) {
  
  Rect<1> launchBounds(0, mNumRobustnessMonitors - 1);
  ArgumentMap argMap;
  IndexTaskLauncher robustnessMonitorLauncher(ROBUSTNESS_MONITOR_TASK, launchBounds, TaskArgument(NULL, 0), argMap);
  FutureMap robustnessMonitorFutureMap = runtime->execute_index_space(ctx, robustnessMonitorLauncher);
  
}

void TopLevelTask::maybeOpenFileDataSource() {
  if(const char* filePathBase = std::getenv("AMI2_FILE_PATH_BASE")) {
    mFileDataSource.selectFileDataSource(filePathBase);
  }
}



void TopLevelTask::top_level_task(const Task* task,
                                         const std::vector<PhysicalRegion> &regions,
                                         Context ctx, Runtime* runtime) {
  
  maybeOpenFileDataSource();
  
  do {
    
    launchTelemetryProcessingTasks(ctx, runtime);
    launchGraphManagerTask(ctx, runtime);
    
    if(timeToMonitor()) {
      launchRobustnessMonitorTask(ctx, runtime);
    }
    
  } while(true);
  
}





