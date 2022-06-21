#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "inunity.h"
#include "aescode.c"

extern void ShiftRows(void);

void setUp() {}
void tearDown() {}

void test_intermittent_war(void) {
  // set-up test-case
  uint8_t plain_text[16] = { (uint8_t) 0x6b, (uint8_t) 0xc1, (uint8_t) 0xbe, (uint8_t) 0xe2, (uint8_t) 0x2e, (uint8_t) 0x40, (uint8_t) 0x9f, (uint8_t) 0x96, (uint8_t) 0xe9, (uint8_t) 0x3d, (uint8_t) 0x7e, (uint8_t) 0x11, (uint8_t) 0x73, (uint8_t) 0x93, (uint8_t) 0x17, (uint8_t) 0x2a };

  state = (state_t*)plain_text;

  TEST_ASSERT_WAR(SubBytes());
  //SubBytes();
  //TEST_ASSERT_EQUAL_INT(42,1);
}

int main(void) {
  UNITY_BEGIN();

  RUN_TEST(test_intermittent_war);

  return UNITY_END();
}
