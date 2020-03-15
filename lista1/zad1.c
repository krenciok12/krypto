#include <stdlib.h>
#include <stdio.h>

int main()
{

    srandom(1472);
    long int a[10000];
    long int k1;
    long int k2;
    int num=0;
    int num2=0;
    for (int i=0;i<31;i++)
    {
        a[i] = random();
        //printf("%d: %ld\n",i,a[i]);
    }
    for (int i=31;i<10000;i++)
    {
        a[i] = random();
        k1=(a[i-31]+a[i-3]) % 2147483648;
        k2=(a[i-31]+a[i-3]+1) % 2147483648;
        if (a[i]==k1)
            num++;
        if (a[i]==k2)
            num2++;
    }
    printf("%d %d\n",num,num2);
}
