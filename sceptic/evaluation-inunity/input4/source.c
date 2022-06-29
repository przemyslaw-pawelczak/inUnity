int i;
int val[4];
int sum = 0;

int main() {
  for(i=0;i<50;i++) {
    val[0] = input0();
    val[1] = input1();
    checkpoint();
    val[2] = input2();
    val[3] = input3();
    sum = sum+val[0]+val[1]+val[2]+val[3];
  }

  return sum;
}
