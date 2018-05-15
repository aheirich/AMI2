//
//  toplevel.cc
//  
//
//  Created by Heirich, Alan on 5/3/18.
//


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
  TopLevelTask(){
    mDataSource = FILE_DATA_SOURCE_TASK;
    mNumWorkers = 1;
  }
  
  virtual ~TopLevelTask(){ }
  
  enum TaskIdEnum {
    TOP_LEVEL_TASK,
    WORKER_TASK,
    COLLECTOR_TASK,
    SHARED_MEMORY_DATA_SOURCE_TASK,
    FILE_DATA_SOURCE_TASK,
    GRAPH_MANAGER_TASK,
    ROBUSTNESS_MONITOR_TASK
  };
  
private:
  static TaskIdEnum mDataSource;
  static unsigned mNumWorkers;
  static unsigned mNumGraphManagers;
  static unsigned mNumRobustnessMonitors;
  
  static void launchTelemetryProcessingTasks(Context ctx, Runtime* runtime) {
    
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
  
  static void launchGraphManagerTask(Context ctx, Runtime* runtime) {
    Rect<1> launchBounds(0, mNumGraphManagers - 1);
    ArgumentMap argMap;
    IndexTaskLauncher graphManagerLauncher(GRAPH_MANAGER_TASK, launchBounds, TaskArgument(NULL, 0), argMap);
    FutureMap graphManagerFutureMap = runtime->execute_index_space(ctx, graphManagerLauncher);
  }
  
  static bool timeToMonitor() {
    return false;
  }
  
  static void launchRobustnessMonitorTask(Context ctx, Runtime* runtime) {
    Rect<1> launchBounds(0, mNumRobustnessMonitors - 1);
    ArgumentMap argMap;
    IndexTaskLauncher robustnessMonitorLauncher(ROBUSTNESS_MONITOR_TASK, launchBounds, TaskArgument(NULL, 0), argMap);
    FutureMap robustnessMonitorFutureMap = runtime->execute_index_space(ctx, robustnessMonitorLauncher);
  }
  
  
  
public:
  static void top_level_task(const Task* task,
                             const std::vector<PhysicalRegion> &regions,
                             Context ctx, Runtime* runtime) {
    
    do {
      
      launchTelemetryProcessingTasks(ctx, runtime);
      launchGraphManagerTask(ctx, runtime);
      
      if(timeToMonitor()) {
        launchRobustnessMonitorTask(ctx, runtime);
      }
      
    } while(true);
    
  }
  
};

// static members of TopLevelTask
TopLevelTask::TaskIdEnum TopLevelTask::mDataSource;
unsigned TopLevelTask::mNumWorkers;
unsigned TopLevelTask::mNumGraphManagers;
unsigned TopLevelTask::mNumRobustnessMonitors;


static void preregisterTasks() {
  TaskVariantRegistrar registrar(TopLevelTask::TOP_LEVEL_TASK, "top_level_task");
  Runtime::preregister_task_variant<TopLevelTask::top_level_task>(registrar, "top_level_task");
  registrar.set_leaf();
  Runtime::preregister_task_variant<Worker::worker_task>(registrar, "worker_task", TopLevelTask::WORKER_TASK);
  registrar.set_leaf();
  Runtime::preregister_task_variant<Collector::collector_task>(registrar, "collector_task", TopLevelTask::COLLECTOR_TASK);
  registrar.set_leaf();
  Runtime::preregister_task_variant<SharedMemoryDataSource::task>(registrar, "shared_memory_data_source_task", TopLevelTask::SHARED_MEMORY_DATA_SOURCE_TASK);
  registrar.set_leaf();
  Runtime::preregister_task_variant<FileDataSource::task>(registrar, "file_data_source_task", TopLevelTask::FILE_DATA_SOURCE_TASK);
  registrar.set_leaf();
  Runtime::preregister_task_variant<GraphManager::graph_manager_task>(registrar, "graph_manager_task", TopLevelTask::GRAPH_MANAGER_TASK);
  registrar.set_leaf();
  Runtime::preregister_task_variant<RobustnessMonitor::robustness_monitor_task>(registrar, "robustness_monitor_task", TopLevelTask::ROBUSTNESS_MONITOR_TASK);
}




int main(int argc, char *argv[]) {
  Runtime::set_top_level_task_id(TopLevelTask::TOP_LEVEL_TASK);
  preregisterTasks();
  return Runtime::start(argc, argv);
}
