#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "inunity.h"
#include "fourier.h"

extern unsigned NumberOfBitsNeeded ( unsigned PowerOfTwo );

void setUp() {}
void tearDown() {}

void test_intermittent_war(void) {

  TEST_ASSERT_WAR(NumberOfBitsNeeded(4));
}

int main(void) {
  UNITY_BEGIN();

  RUN_TEST(test_intermittent_war);

  return UNITY_END();
}
