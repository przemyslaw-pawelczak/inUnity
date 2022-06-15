#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "inunity.h"
#include "crc.h"

extern crc crcSlow(unsigned char const message[], int nBytes);

void setUp() {}
void tearDown() {}

void test_intermittent_war(void) {
  unsigned char  test[] = "123456789";
  TEST_ASSERT_WAR(crcSlow(test,9));
}

int main(void) {
  UNITY_BEGIN();

  RUN_TEST(test_intermittent_war);

  return UNITY_END();
}
