//
//  robustness_monitor.cc
//  
//
//  Created by Heirich, Alan on 5/4/18.
//

#include <stdio.h>

#include "robustness_monitor.hpp"

int RobustnessMonitor::memberVariable;//placeholder

RobustnessMonitor::RobustnessMonitor() {
  
}

RobustnessMonitor::~RobustnessMonitor() {
  
}


void RobustnessMonitor::robustness_monitor_task(const Task* task,
                                                const std::vector<PhysicalRegion> &regions,
                                                Context ctx, Runtime* runtime) {
  
  deserializeFromStore(task, regions, ctx, runtime);
  
  serializeToStore(task, regions, ctx, runtime);
}

void RobustnessMonitor::serialize(KeyValueStore::json& j) {
  j["memberVariable"] = memberVariable; //placeholder
}

void RobustnessMonitor::deserialize(KeyValueStore::json& j) {
  memberVariable = j["memberVariable"]; //placeholder
}
