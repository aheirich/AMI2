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

#include "control_store.hpp"


class RobustTask {
  
public:
  RobustTask();
  virtual ~RobustTask();
  
protected:
  static void deserializeFromStore(const Task* task,
                                   const std::vector<PhysicalRegion> &regions,
                                   Context ctx, Runtime* runtime);
  static void serializeToStore(const Task* task,
                               const std::vector<PhysicalRegion> &regions,
                               Context ctx, Runtime* runtime);
  
private:
  static std::string key(const Task* task);
  static void serialize(KeyValueStore::json& j){};
  static void deserialize(KeyValueStore::json& j){};
};


#endif /* robust_task_hpp */

