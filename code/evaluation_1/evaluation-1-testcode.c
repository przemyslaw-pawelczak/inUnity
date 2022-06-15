#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "inunity.h"
#include "evaluation-1-productioncode.h"
#include "crc.h"

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

  int tmp;

  unsigned char  test[] = "123456789";
  crcSlow(test,9);
  crcInit();
  crcFast(test,9);

  tmp = UNITY_END();
  return tmp;
}
