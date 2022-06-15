int a __attribute__((section(".NVM"))) = 5;


int main() {
    for(int i = 0; i < 10; i++) {
        a++;
	checkpoint();
    }
    return a;
}
