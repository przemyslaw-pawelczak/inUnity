int a = 0;
int b = 0;

// Functions
void variable() {
  a = 0;
  checkpoint();
  b = a;
  b = b+1;
  a = b;
}

int stack2() {
  // do nothing
  return 2;
}

int stack() {
  // do nothing
  checkpoint();
  return 1;
}

void heap() {
  int *p;
  p = malloc(sizeof(p));
  *p=5;
  checkpoint();
  int c=*p+7;
  free(p);
}

int main(void)
{
  // Globar Variable
  checkpoint();
  variable();
  checkpoint();

  // Stack
  checkpoint();
  stack();
  stack2();
  checkpoint();

  // Heap
  checkpoint();
  heap();
  checkpoint();

  return 0;
}   /* main() */
