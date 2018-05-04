//
//  shared_memory_data_source.hpp
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#ifndef shared_memory_data_source_hpp
#define shared_memory_data_source_hpp

#include <stdio.h>

#include "legion.h"
using namespace legion;

#include "data_source.hpp"


class SharedMemoryDataSource : public DataSource {
  
public:
  SharedMemoryDataSource();
  virtual void ~SharedMemoryDataSource();
  void task(const Task* task,
            const std::vector<PhysicalRegion> &regions,
            Context ctx, Runtime* runtime);
private:
};


#endif /* shared_memory_data_source_hpp */
