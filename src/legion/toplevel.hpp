//
//  toplevel.hpp
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#ifndef toplevel_hpp
#define toplevel_hpp

#include "legion.h"
using namespace legion;

#include <stdio.h>

enum TaskId {
  TOP_LEVEL_TASK,
  WORKER_TASK,
  SHARED_MEMORY_DATA_SOURCE_TASK,
  FILE_DATA_SOURCE_TASK,
  GRAPH_MANAGER_TASK,
  ROBUSTNESS_MONITOR_TASK
};


#endif /* toplevel_hpp */
