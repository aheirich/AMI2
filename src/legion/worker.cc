//
//  worker.cc
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#include "worker.hpp"

int Worker::memberVariable;//placeholder


Worker::Worker() {
  
}

Worker::~Worker() {
  
}


void Worker::worker_task(const Task* task,
                         const std::vector<PhysicalRegion> &regions,
                         Context ctx, Runtime* runtime) {
  
  deserializeFromStore(task, regions, ctx, runtime);
  
  serializeToStore(task, regions, ctx, runtime);
}

void Worker::serialize(KeyValueStore::json& j) {
  j["memberVariable"] = memberVariable; //placeholder
}

void Worker::deserialize(KeyValueStore::json& j) {
  memberVariable = j["memberVariable"]; //placeholder
}
