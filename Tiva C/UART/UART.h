#ifndef __UART_H__
#define __UART_H__

#include "src/tm4c123gh6pm.h"
void UART_Init(void);
unsigned char UART_InChar(void);
void UART_OutChar(unsigned char data);
void UART_OutString(char *pt);
void UART_InString(char *bufPt, unsigned short max);

// standard ASCII symbols
#define CR   0x0D
#define LF   0x0A
#define BS   0x08
#define ESC  0x1B
#define SP   0x20
#define DEL  0x7F

#endif
