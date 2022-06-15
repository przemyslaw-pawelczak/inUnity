int i __attribute__((section(".NVM")));
int res[100] __attribute__((section(".NVM")));

void main() {
    i = 0;
    checkpoint();
    for(; i < 100; i++) {
        sceptic_log("i", i);
        sceptic_reset("conditional", i == 3);
        res[i] = i;
        sceptic_log("res_i", res[i]);
        sceptic_reset("conditional", i == 2);
        sceptic_reset("clock", 2);
    }
}
