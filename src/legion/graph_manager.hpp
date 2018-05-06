//
//  graph_manager.hpp
//  
//
//  Created by Heirich, Alan on 5/3/18.
//

#ifndef graph_manager_hpp
#define graph_manager_hpp

#include <stdio.h>

#include "legion.h"
using namespace Legion;

#include "robust_task.hpp"

class GraphManager : public RobustTask {
  
public:
  GraphManager();
  virtual ~GraphManager();
  static void graph_manager_task(const Task* task,
                                 const std::vector<PhysicalRegion> &regions,
                                 Context ctx, Runtime* runtime);
protected:
  void serialize(KeyValueStore::json& j);
  void deserialize(KeyValueStore::json& j);
  
private:
};

#endif /* graph_manager_hpp */
