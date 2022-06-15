int i;
int val;
int sum = 0;
int critical = 10000;

int main() {
	for(i = 0; i < 50; i++) {
		val = input();
		checkpoint();
		sum = sum + val;
		
		if(sum > critical) {
			out('Error: critical value exceeded!');
		}
	}
	
	out(sum);
}
