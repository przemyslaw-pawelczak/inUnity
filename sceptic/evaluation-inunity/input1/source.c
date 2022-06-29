int i;
int val;
int sum = 0;

int main() {
  for(i=0;i<50;i++) {
    val = input();
    checkpoint();
    sum = sum+val;
  }

  return sum;
}
