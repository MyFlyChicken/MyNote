#define TimeDef             unsigned short
#define LineDef             unsigned char
#define END                 ((TimeDef)-1)
#define LINE                ((__LINE__%(LineDef)-1)+1)  

#define me  (*cp)
#define TaskFun(TaskName)   TimeDef TaskName(C##TaskName *cp)

#define _SS                 switch(me.task.lc){default:
#define Exit                do { me.task.lc=0; return END; }  while(0)
#define _EE                 ;}; Exit;

#define Restart             do { me.task.lc=0; return 0; }  while(0)

#define WaitX(ticks)        do { me.task.lc=LINE; return ((ticks)); case LINE:;} while(0)
#define WaitUntil(A)        do { while(!(A)) WaitX(1);} while(0)
#define WaitUtilT(A,TimeOut)    do { static TimeDef _count=(TimeOut); do { WaitX(1); _count--; } while((!(A))&&(_count>0));} while(0);

#define UpdateTimer(TaskVar)    do { if((TaskVar.task.timer!=0)&&(TaskVar.task.timer!=END)) TaskVar.task.timer--; }  while(0)
#define RunTask(TaskFunName,TaskVar)  do { if (TaskVar.task.timer==0) { TimeDef d=TaskFunName(&(TaskVar)); while(TaskVar.task.timer!=d) TaskVar.task.timer=d;} }  while(0); 
#define CallSub(SubTaskFunName,SubTaskVar)    do { WaitX(0);SubTaskVar.task.timer=SubTaskFunName(&(SubTaskVar));      \
                                                    if(SubTaskVar.task.timer!=END) return SubTaskVar.task.timer;} while(0)
    
#define TClass(type)         typedef struct C##type C##type; \
                             TaskFun(type); \
                             struct C##type { struct C_task task;
#define TEND     };
                             
struct C_task
{
  TimeDef timer;
  LineDef lc;
};
