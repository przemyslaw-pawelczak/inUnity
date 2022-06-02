#include <stdint.h>

#include "inunity.h"
#include "example-productioncode.h"

extern int globalInputVariable;

void setUp() {}
void tearDown() {}

void test_basic(void) {
  TEST_ASSERT_EQUAL_INT(42, returnNumber(42));
}

void test_intermittent_war(void) {
  TEST_ASSERT_WAR(functionUnderTest());
}

void test_intermittent_atomic(void) {
  TEST_ASSERT_ATOMIC(functionUnderTest());
}

void test_intermittent_fresh(void) {
  TEST_ASSERT_FRESH_GLOBAL(functionUnderTestFresh(), globalInputVariable);
  //TEST_ASSERT_FRESH_RETURN(functionUnderTestFresh(), inputFunction);

}

int main(void) {
  UNITY_BEGIN();

  RUN_TEST(test_basic); // basic test case that will pass
  RUN_TEST(test_intermittent_war);
  RUN_TEST(test_intermittent_atomic);
  RUN_TEST(test_intermittent_fresh);

  return UNITY_END();;
}
