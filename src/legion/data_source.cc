//
//  data_source.cpp
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#include "data_source.hpp"

DataSource::DataSource() {
  
}

virtual void DataSource::~DataSource() {
  
}


void DataSource::task(const Task* task,
                      const std::vector<PhysicalRegion> &regions,
                      Context ctx, Runtime* runtime) {
  
}

