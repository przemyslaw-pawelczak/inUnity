#include "inunity.h"
#include "input4-productioncode.h"

void setUp() {}
void tearDown() {}

extern int val[4];

void test_intermittent_fresh(void) {
  TEST_ASSERT_FRESH_GLOBAL(sense(), val);
  //sense();
  //TEST_ASSERT_EQUAL_INT(42,1);
}

int main(void) {
  UNITY_BEGIN();

  RUN_TEST(test_intermittent_fresh);

  return UNITY_END();
}
