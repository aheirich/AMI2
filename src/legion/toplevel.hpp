//
//  toplevel.hpp
//
//
//  Created by Heirich, Alan on 5/3/18.
//

#ifndef toplevel_hpp
#define toplevel_hpp

#include <stdio.h>

#include "legion.h"
using namespace Legion;

#include "worker.hpp"
#include "shared_memory_data_source.hpp"
#include "file_data_source.hpp"
#include "graph_manager.hpp"
#include "robustness_monitor.hpp"
#include "control_store.hpp"
#include "robust_task.hpp"
#include "collector.hpp"



class TopLevelTask : public RobustTask {
public:
  enum TaskIdEnum {
    TOP_LEVEL_TASK,
    WORKER_TASK,
    COLLECTOR_TASK,
    SHARED_MEMORY_DATA_SOURCE_TASK,
    FILE_DATA_SOURCE_TASK,
    GRAPH_MANAGER_TASK,
    ROBUSTNESS_MONITOR_TASK
  };

  
public:
  TopLevelTask();
  virtual ~TopLevelTask();
  static void top_level_task(const Task* task,
                   const std::vector<PhysicalRegion> &regions,
                   Context ctx, Runtime* runtime);
private:
  static TaskIdEnum mDataSource;
  static unsigned mNumWorkers;
  static unsigned mNumGraphManagers;
  static unsigned mNumRobustnessMonitors;
  static FileDataSource mFileDataSource;
  static SharedMemoryDataSource mSharedMemoryDataSource;
  static Worker mWorker;
  static Collector mCollector;
  static GraphManager mGraphManager;
  static RobustnessMonitor mRobustnessMonitor;

  static void launchTelemetryProcessingTasks(Context ctx, Runtime* runtime);
  static void launchGraphManagerTask(Context ctx, Runtime* runtime);
  static bool timeToMonitor();
  static void launchRobustnessMonitorTask(Context ctx, Runtime* runtime);
  static void maybeOpenFileDataSource();
  
};


#endif /* toplevel_hpp */
