#include "xxddqv2.h"

TClass(Task1)
   int state; 
TEND

TClass(Task2)
  int state;
  int i;
TEND

void runtasks();
void UpdateTimers();

extern CTask1 task1;
extern CTask2 task2;
