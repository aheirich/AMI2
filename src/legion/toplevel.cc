//
//  toplevel.cc
//  
//
//  Created by Heirich, Alan on 5/3/18.
//


#include "toplevel.hpp"
#include "worker.hpp"
#include "shared_memory_data_source.hpp"
#include "file_data_source.hpp"
#include "graph_manager.hpp"
#include "robustness_monitor.hpp"
#include "control_store.hpp"
#include "robust_task.hpp"


class TopLevelTask : public RobustTask {
public:
  TopLevelTask(){ }
  virtual ~TopLevelTask(){ }
  
private:
  static int memberVariable;//placeholder

  static bool topLevelStateIsChanged() {
    return false;
  }
  
  
  static void launchTelemetryProcessingTasks() {
    // index launch: current data source, worker
  }
  
  static void launchGraphManagerTask() {
    
  }
  
  static bool timeToMonitor() {
    return false;
  }
  
  static void launchRobustnessMonitorTask() {
    
  }
  
  void serialize(KeyValueStore::json& j) {
    j["memberVariable"] = memberVariable; //placeholder
  }
  
  void deserialize(KeyValueStore::json& j) {
    memberVariable = j["memberVariable"]; //placeholder
  }

  
public:
  static void top_level_task(const Task* task,
                      const std::vector<PhysicalRegion> &regions,
                      Context ctx, Runtime* runtime) {
    
    do {
      if(topLevelStateIsChanged()) {
        deserializeFromStore(task, regions, ctx, runtime);
      }
      
      launchTelemetryProcessingTasks();
      launchGraphManagerTask();
      
      if(timeToMonitor()) {
        launchRobustnessMonitorTask();
      }
      
      serializeToStore(task, regions, ctx, runtime);
      
    } while(true);
    
  }
  
};



static void preregisterTasks() {
  TaskVariantRegistrar registrar(TOP_LEVEL_TASK, "top_level_task");
  Runtime::preregister_task_variant<TopLevelTask::top_level_task>(registrar, "top_level_task");
  Runtime::preregister_task_variant<Worker::worker_task>(registrar, "worker_task");
  Runtime::preregister_task_variant<SharedMemoryDataSource::task>(registrar, "shared_memory_data_source_task");
  Runtime::preregister_task_variant<FileDataSource::task>(registrar, "file_data_source_task");
  Runtime::preregister_task_variant<GraphManager::graph_manager_task>(registrar, "graph_manager_task");
  Runtime::preregister_task_variant<RobustnessMonitor::robustness_monitor_task>(registrar, "robustness_monitor_task");
}


int main(int argc, char *argv[]) {
  Runtime::set_top_level_task_id(TOP_LEVEL_TASK);
  preregisterTasks();
  return Runtime::start(argc, argv);
}
