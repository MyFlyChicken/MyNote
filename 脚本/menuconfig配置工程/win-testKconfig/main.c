#include "test.h"

extern void test1(void);
extern void test2(void);
extern void test3(void);

int main(void)
{
    test1();
    test2();
    test3();

    return 0;
}
