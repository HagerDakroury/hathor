#include "sysinit/sysinit.h"
#include "timer/timer0.h"
#include "UART/UART.h"

#include "tm4c123gh6pm.h"

#define tRate 500


//debug code
void main(void){
  sys_init();

      UART_Init();
      int fx[500];
      int fy[500];
      int t[500];
      char dirx[500];
      char diry[500];
      char pen[500];
      int sumfx=0;
      int sumfy=0;
      int sumt=0;


      unsigned char a;
      unsigned char b;
      unsigned char c;
      unsigned char d;
      int j=0;
      int k=0;
      int n=0;


      UART_OutChar('a');
      a=(int)UART_InChar();
      b=(int)UART_InChar();
      c=(int)UART_InChar();
      d=(int)UART_InChar();

      int size=(int)(a| b<<8 | c<<17 | d<<24);

      int i;

      while(1)
      {

       UART_OutChar('a');

       for (i=0 ;i<tRate;i++){


           UART_OutChar('a');

          a=(int)UART_InChar();
          b=(int)UART_InChar();
          c=(int)UART_InChar();
          d=(int)UART_InChar();

          fx[i]=(int)(a| b<<8 | c<<17 | d<<24);

          a=(int)UART_InChar();
          b=(int)UART_InChar();
          c=(int)UART_InChar();
          d=(int)UART_InChar();

          fy[i]=(int)(a| b<<8 | c<<17 | d<<24);

          a=(int)UART_InChar();
          b=(int)UART_InChar();
          c=(int)UART_InChar();
          d=(int)UART_InChar();
          int t1=(int)(a| b<<8 | c<<17 | d<<24);
          a=(int)UART_InChar();
          b=(int)UART_InChar();
          c=(int)UART_InChar();
          d=(int)UART_InChar();
          int t2=(int)(a| b<<8 | c<<17 | d<<24);

          t[i]=t1*1000+t2;

          j++;
          if(j==size)
            break;

          }

       for (i=0 ;i<tRate;i++){

           UART_OutChar('a');

           a=(int)UART_InChar();
           dirx[i]=a;

           a=(int)UART_InChar();
           diry[i]=a;

           a=(int)UART_InChar();
           pen[i]=a;

           k++;
           if(k==size)
             break;

           }

       for (i=0 ;i<tRate;i++){

               sumfx+=fx[i];
               sumfy+=fy[i];
               sumt+=t[i];
               n++;
                if(n==size)
                    break;

               }


       //pwm code goes here
          delaym(1000);

          if(j==size)
              break;

      }



      delaym(1000);

}
