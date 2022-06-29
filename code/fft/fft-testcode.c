#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "fourier.h"
#include "./bareBench.h"

#include "inunity.h"

int invfft=0;
unsigned MAXSIZE; // small 4096, 8192 inverse, 512 for memory-limited systems
unsigned MAXWAVES=4; //large has 8
static float realin[1024];
static float imagin[1024];
static float realout[1024];
static float imagout[1024];
static float Coeff[16];
static float Amp[16];

void setUp() {}
void tearDown() {}

void test_intermittent_war(void) {
  unsigned i,j;
	float *RealIn;
	float *ImagIn;
	float *RealOut;
	float *ImagOut;
	float *coeff;
	float *amp;

  RealIn = realin;
  ImagIn = imagin;
  RealOut = realout;
  ImagOut = imagout;
  coeff = Coeff;
  amp = Amp;

  srand(1);
  MAXSIZE = 128;

  for(i=0;i<MAXWAVES;i++)
	{
		coeff[i] = rand()%1000;
		amp[i] = rand()%1000;
	}
 for(i=0;i<MAXSIZE;i++)
 {
   /*   RealIn[i]=rand();*/
	 RealIn[i]=0;
	 for(j=0;j<MAXWAVES;j++)
	 {
		 /* randomly select sin or cos */
		 if (rand()%2)
		 {
		 		RealIn[i]+=coeff[j]*cos(amp[j]*i);
			}
		 else
		 {
		 	RealIn[i]+=coeff[j]*sin(amp[j]*i);
		 }
  	 ImagIn[i]=0;
	 }
 }

  //TEST_ASSERT_WAR(fft_float(MAXSIZE,invfft,RealIn,ImagIn,RealOut,ImagOut));
  fft_float(MAXSIZE,invfft,RealIn,ImagIn,RealOut,ImagOut);
  TEST_ASSERT_EQUAL_INT(42,1);
}

int main() {
    UNITY_BEGIN();

    RUN_TEST(test_intermittent_war);

    return UNITY_END();
}
