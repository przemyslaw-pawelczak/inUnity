
#include "inunity.h"
//#include "aes.h"

//extern void ShiftRows();

void setUp() {}
void tearDown() {}

void test_intermittent_war(void) {
  TEST_ASSERT_WAR(ShiftRows());
}

int main(void) {
  //UNITY_BEGIN();

  //RUN_TEST(test_intermittent_war);

  //return UNITY_END();
}
