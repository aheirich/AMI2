//
//  file_data_source.hpp
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#ifndef file_data_source_hpp
#define file_data_source_hpp

#include <stdio.h>

#include "legion.h"
using namespace Legion;

#include "data_source.hpp"


class FileDataSource : public DataSource {
  
public:
  FileDataSource();
  virtual ~FileDataSource();
  static void task(const Task* task,
                   const std::vector<PhysicalRegion> &regions,
                   Context ctx, Runtime* runtime);
private:
};


#endif /* file_data_source_hpp */
