#include "inunity.h"
#include "input1-productioncode.h"

void setUp() {}
void tearDown() {}

void test_intermittent_fresh(void) {
  TEST_ASSERT_FRESH_RETURN(sense(), input);
  //sense();
  //TEST_ASSERT_EQUAL_INT(42,1);
}

int main(void) {
  UNITY_BEGIN();

  RUN_TEST(test_intermittent_fresh);

  return UNITY_END();
}
