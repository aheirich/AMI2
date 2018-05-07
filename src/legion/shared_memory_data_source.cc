//
//  shared_memory_data_source.cc
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#include "shared_memory_data_source.hpp"

int SharedMemoryDataSource::memberVariable;//placeholder

SharedMemoryDataSource::SharedMemoryDataSource() {
  
}

SharedMemoryDataSource::~SharedMemoryDataSource() {
  
}


void SharedMemoryDataSource::task(const Task* task,
                                  const std::vector<PhysicalRegion> &regions,
                                  Context ctx, Runtime* runtime) {
  
  deserializeFromStore(task, regions, ctx, runtime);
  
  serializeToStore(task, regions, ctx, runtime);
}

void SharedMemoryDataSource::serialize(KeyValueStore::json& j) {
  j["memberVariable"] = memberVariable; //placeholder
}

void SharedMemoryDataSource::deserialize(KeyValueStore::json& j) {
  memberVariable = j["memberVariable"]; //placeholder
}
