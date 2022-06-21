#include "nvm.h"

nvm int a = 0;
int globalInputVariable;

int returnNumber(int value1) {
  return value1;
}

int inputFunction() {
  return 42;
}

int functionUnderTestFresh() {
  globalInputVariable = inputFunction();

  int temp = globalInputVariable + 5;
  //CHECKPOINT = 0; // This marks a CP
  //globalInputVariable = inputFunction();

  return globalInputVariable;
}

int functionUnderTest() {
  int b = a;
  //CHECKPOINT = 0; // This marks a CP
  a = b + 1;

  return a;
}
