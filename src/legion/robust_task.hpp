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
  static void deserializeFromStore(const Task* task);
  static void serializeToStore(const Task* task);
  virtual void serialize(KeyValueStore::json& j){ }
  virtual void deserialize(KeyValueStore::json& j){ }
  void taskIs(RobustTask* task){ mRobustTask = task; }

private:
  static std::string key(const Task* task);
  static ControlStore* mControlStore;
  static RobustTask* mRobustTask;
};


#endif /* robust_task_hpp */
