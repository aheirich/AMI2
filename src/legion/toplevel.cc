//
//  toplevel.cpp
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




void top_level_task(const Task* task,
                    const std::vector<PhysicalRegion> &regions,
                    Context ctx, Runtime* runtime) {
  
}



static void preregisterTasks() {
  TaskVariantRegistrar registrar(TOP_LEVEL_TASK, "top_level_task");
  Runtime::preregister_task_variant<top_level_task>(registrar, "top_level_task");
  Runtime::preregister_task_variant<Worker::worker_task>(registrar, "worker_task");
  Runtime::preregister_task_variant<SharedMemoryDataSource::task>(registrar, "shared_memory_data_source");
  Runtime::preregister_task_variant<FileDataSource::task>(registrar, "file_data_source");
  Runtime::preregister_task_variant<GraphManager::graph_manager_task>(registrar, "graph_manager_task");
  Runtime::preregister_task_variant<RobustnessMonitor::robustness_monitor_task>(registrar, "robustness_monitor_task");
}


int main(int argc, char *argv[]) {
  Runtime::set_top_level_task_id(TOP_LEVEL_TASK);
  preregisterTasks();
  return Runtime::start(argc, argv);
}
