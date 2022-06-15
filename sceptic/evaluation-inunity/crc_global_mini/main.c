/**********************************************************************
 *
 * Filename:    main.c
 * 
 * Description: A simple test program for the CRC implementations.
 *
 * Notes:       To test a different CRC standard, modify crc.h.
 *
 * 
 * Copyright (c) 2000 by Michael Barr.  This software is placed into
 * the public domain and may be used for any purpose.  However, this
 * notice must not be changed or removed and no warranty is either
 * expressed or implied by its publication or distribution.
 **********************************************************************/
#include "./bareBench.h"
#include <stdio.h>
#include <string.h>

#include "crc.h"


int
main(void)
{
	unsigned char  test[] = "123456789";
	crcSlow(test,9);

  return 0;
}   /* main() */
