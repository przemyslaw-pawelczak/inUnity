#ifndef INUNIT_H_INCLUDED
#define INUNIT_H_INCLUDED

#include "unity/src/unity_internals.h"
#include "unity/src/unity.h"
#include "unity/src/unity.c"

// TEST_ASSERT_WAR -----------------------------------------------------------
#define TEST_ASSERT_WAR(func)                           __asm__("WARSTART:"); WAR_FAILED_FLAG=0; func; __asm__("WAREND:"); checkFail(WAR_FAILED_FLAG);
#define TEST_ASSERT_WAR_MESSAGE(func,msg)               __asm__("WARSTART:"); WAR_FAILED_FLAG=0; func; __asm__("WAREND:"); checkFailMsg(WAR_FAILED_FLAG,msg);

int WAR_FAILED_FLAG;

// TEST_ASSERT_ATOMIC -----------------------------------------------------------
#define TEST_ASSERT_ATOMIC(func)                        __asm__("ATOMICSTART:"); ATOMIC_FAILED_FLAG=0; func; __asm__("ATOMICEND:"); checkFail(ATOMIC_FAILED_FLAG);
#define TEST_ASSERT_ATOMIC_MESSAGE(func,msg)            __asm__("ATOMICSTART:"); ATOMIC_FAILED_FLAG=0; func; __asm__("ATOMICEND:"); checkFailMsg(ATOMIC_FAILED_FLAG,msg);

int ATOMIC_FAILED_FLAG;

// TEST_ASSERT_FRESH -----------------------------------------------------------
#define TEST_ASSERT_FRESH_GLOBAL(func,var)              FRESH_GLOBAL_ADDRESS=(void*)&var; __asm__("FRESHSTART:"); FRESH_FAILED_FLAG=0; func; __asm__("FRESHEND:"); checkFail(FRESH_FAILED_FLAG);
#define TEST_ASSERT_FRESH_RETURN(func,var)              FRESH_RETURN_ADDRESS=(void*)var; __asm__("FRESHSTART:"); FRESH_FAILED_FLAG=0; func; __asm__("FRESHEND:"); checkFail(FRESH_FAILED_FLAG);
#define TEST_ASSERT_FRESH_GLOBAL_MESSAGE(func,var,msg)  FRESH_GLOBAL_ADDRESS=(void*)&var; __asm__("FRESHSTART:"); FRESH_FAILED_FLAG=0; func; __asm__("FRESHEND:"); checkFailMsg(FRESH_FAILED_FLAG,msg);
#define TEST_ASSERT_FRESH_RETURN_MESSAGE(func,var,msg)  FRESH_RETURN_ADDRESS=(void*)var; __asm__("FRESHSTART:"); FRESH_FAILED_FLAG=0; func; __asm__("FRESHEND:"); checkFailMsg(FRESH_FAILED_FLAG,msg);

int FRESH_FAILED_FLAG;
void* FRESH_GLOBAL_ADDRESS = 0;
void* FRESH_RETURN_ADDRESS = 0;

// GLOBAL FUNCTION -------------------------------------------------------------
void checkFail(int flag) {
  if (flag != 0) {
      TEST_FAIL(); // Switch callback for other frameworks
  }
}

void checkFailMsg(int flag, char* msg) {
  if (flag != 0) {
      TEST_FAIL_MESSAGE(msg);  // Switch callback for other frameworks 
  }
}

#endif
