#include "tasks.h"
#include "mbed.h"


int Running=1;

CTask1 task1;
CTask2 task2;

#define SYSLED PA_11
#define DO1  PB_1
#define MKEN  PA_12

DigitalOut myled(SYSLED);
DigitalOut relay1(DO1);


TaskFun(Task1)
{   
    _SS
    
    WaitX(100);
    
    while(Running) {
        WaitX(1500);
        myled=1;
        WaitX(1500);
        myled=0;
    }
    _EE
}

TaskFun(Task2)
{
    _SS

    while(Running) 
    {     
        WaitX(1000);
        relay1=1;
        WaitX(1000);
        relay1=0;
    }
    _EE
}

void UpdateTimers(){
    UpdateTimer(task1);
    UpdateTimer(task2);
}

void runtasks()
{
    RunTask(Task1,task1);
    RunTask(Task2,task2);
}