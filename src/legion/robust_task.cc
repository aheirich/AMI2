//
//  robust_task.cc
//
//
//  Created by Heirich, Alan on 5/4/18.
//

#include "robust_task.hpp"
#include "control_store.hpp"

RobustTask::RobustTask() {
}

RobustTask::~RobustTask() {
}

std::string RobustTask::key(const Task* task) {
  char buffer[256];
  sprintf(buffer, "_%s_%lld", task->get_task_name(), task->get_unique_id());
  return std::string(buffer);
}


void RobustTask::deserializeFromStore(const Task* task,
                                      const std::vector<PhysicalRegion> &regions,
                                      Context ctx, Runtime* runtime) {
  
}

void RobustTask::serializeToStore(const Task* task,
                                  const std::vector<PhysicalRegion> &regions,
                                  Context ctx, Runtime* runtime) {
  ControlStore::json j;
  //mRobustTask->serialize(j);
  std::string s = j.dump();
  //mControlStore->put(key(task), s);
}

