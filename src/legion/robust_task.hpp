//
//  robust_task.hpp
//  
//
//  Created by Heirich, Alan on 5/4/18.
//

#ifndef robust_task_hpp
#define robust_task_hpp

#include <stdio.h>

#include "legion.h"
using namespace Legion;


class RobustTask {
  
public:
  RobustTask();
  virtual ~RobustTask();
  static void deserializeFromStore();
  static void serializeToStore();

private:
};


#endif /* robust_task_hpp */