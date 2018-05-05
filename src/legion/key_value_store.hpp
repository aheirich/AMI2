//
//  key_value_store.hpp
//
//
//  Created by Heirich, Alan on 5/3/18.
//

#ifndef key_value_store_hpp
#define key_value_store_hpp

#include <stdio.h>

#include "legion.h"
using namespace Legion;

#include <nlohmann/json.hpp>
// for convenience
using json = nlohmann::json;


class KeyValueStore {
  
public:
  KeyValueStore();
  virtual ~KeyValueStore();

private:
};

#endif /* key_value_store_hpp */
