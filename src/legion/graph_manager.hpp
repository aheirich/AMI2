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
using namespace legion;


class GraphManager {
  
public:
  GraphManager();
  virtual void ~GraphManager();
  void graph_manager_task(const Task* task,
                          const std::vector<PhysicalRegion> &regions,
                          Context ctx, Runtime* runtime);
private:
};

#endif /* graph_manager_hpp */
