#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "inunity.h"
#include "aescode.c"

extern void ShiftRows(void);

void setUp() {}
void tearDown() {}

void test_intermittent_war(void) {
  TEST_ASSERT_WAR(ShiftRows());
}

int main(void) {
  UNITY_BEGIN();

  RUN_TEST(test_intermittent_war);

  return UNITY_END();
}
