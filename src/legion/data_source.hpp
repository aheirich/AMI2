//
//  data_source.hpp
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#ifndef data_source_hpp
#define data_source_hpp

#include <stdio.h>

#include "legion.h"
using namespace legion;


class DataSource {
  
public:
  DataSource();
  virtual void ~DataSource();
  virtual void task(const Task* task,
                    const std::vector<PhysicalRegion> &regions,
                    Context ctx, Runtime* runtime) = 0;
private:
};


#endif /* data_source_hpp */
