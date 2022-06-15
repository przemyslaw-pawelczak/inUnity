#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "inunity.h"
#include "aes.h"

extern crc crcSlow(unsigned char const message[], int nBytes);

void setUp() {}
void tearDown() {}

int x = 0;

void test_intermittent_war(void) {
  unsigned char  test[] = "123456789";

  x = &test;

  TEST_ASSERT_WAR(crcSlow(test,9));
}

int main(void) {
  UNITY_BEGIN();

  RUN_TEST(test_intermittent_war);

  UNITY_END();
  return x;
}
