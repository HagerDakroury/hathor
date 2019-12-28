#include <stdint.h>
#include "sysinit/sysinit.h"
#include "timer/timer0.h"
#include "UART/UART.h"
#include "tm4c123gh6pm.h"
#include <stdbool.h>
#include "inc/hw_gpio.h"
#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/pin_map.h"
#include "./driverlib/gpio.h"
#include "driverlib/pwm.h"
#include "timer/timer0.h"

#define tRate 500
#define xDir GPIO_PIN_0
#define yDir GPIO_PIN_0=1

int fx[500];
int fy[500];
int t[500];
char dirx[500];
char diry[500];
int getTicks(int freq);
void enable_pwm_x(int ticks);
void enable_pwm_y(int ticks);
void disable_pwms();

void draw_patch();

int getTicks(int freq){
   return 16000000/freq;

}


void setDir(char axis, int dir){
    if(axis=='x'){
        GPIOPinWrite(GPIO_PORTB_BASE, xDir, dir);
    }

    else{
        GPIOPinWrite(GPIO_PORTB_BASE, yDir, dir);


    }

}

void dir_init(){

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOB));
    GPIOPinTypeGPIOOutput(GPIO_PORTB_BASE, xDir | yDir);

}



void main(void){


      sys_init();
      UART_Init();
      dir_init();

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

          draw_patch();
          delaym(1000);

          if(j==size)
              break;

      }



      delaym(1000);

}

void enable_pwm_x (int ticks){
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_0, ticks);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_0, ticks/2);
    PWMGenEnable(PWM0_BASE, PWM_GEN_0);
    PWMOutputState(PWM0_BASE, (PWM_OUT_0_BIT ), true);
}

void enable_pwm_y(int ticks){
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_1, ticks);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_4, ticks/2);
    PWMGenEnable(PWM0_BASE, PWM_GEN_1);
    PWMOutputState(PWM0_BASE, (PWM_OUT_4_BIT ), true);
}

void disable_pwms(){
    PWMOutputState(PWM0_BASE, (PWM_OUT_0_BIT ), false);
    PWMOutputState(PWM0_BASE, (PWM_OUT_4_BIT ), false);
    PWMGenDisable(PWM0_BASE, PWM_GEN_0);
    PWMGenDisable(PWM0_BASE, PWM_GEN_1);
}



void draw_patch(){
    int i = 0;
    for(;i<88;i++){
        enable_pwm_x(getTicks(fx[i]));
        enable_pwm_y(getTicks(fy[i]));
        setdir('x',dirx[i]);
        setdir('y',diry[i]);
        delayu(t[i]);
        disable_pwms();

    }

}
