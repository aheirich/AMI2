//
//  worker.cpp
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#include "worker.hpp"


Worker::Worker() {
  
}

virtual void Worker::~Worker() {
  
}


void Worker::worker_task(const Task* task,
                         const std::vector<PhysicalRegion> &regions,
                         Context ctx, Runtime* runtime) {
  
}
