//
//  file_data_source.cc
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#include "file_data_source.hpp"

FileDataSource::FileDataSource() {
  
}

FileDataSource::~FileDataSource() {
  
}


void FileDataSource::task(const Task* task,
                          const std::vector<PhysicalRegion> &regions,
                          Context ctx, Runtime* runtime) {
  deserializeFromStore(task);
  
  serializeToStore(task, regions, ctx, runtime);
}


void FileDataSource::serialize(KeyValueStore::json& j) {
  j["memberVariable"] = memberVariable; //placeholder
}

void FileDataSource::deserialize(KeyValueStore::json& j) {
  memberVariable = j["memberVariable"]; //placeholder
}
