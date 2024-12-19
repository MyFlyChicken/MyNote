#include "mbed.h"
#include "tasks.h"
#include <stdio.h>
#include <errno.h>

Ticker  systick;

void ontick(){
    UpdateTimers();
}

int main()
{  
    systick.attach(&ontick,0.001);  

    while(1) {        
        runtasks();   
    }
}
