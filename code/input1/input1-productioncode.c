int i;
int val;
int sum = 0;

void out() {}
int input() { return 0; }

int sense() {
  for(i=0;i<50;i++) {
    val = input();
    checkpoint();
    sum = sum+val;
  }

  return sum;
}
