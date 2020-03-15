#include <iostream>
#include <vector>
using namespace std;

class lcg
{
    private:
    long int state;
    long int a=445777;
    long int c=4546785;
    long int m=6748202;
    public:
    lcg(long int seed)
    {
        this->state=seed;
    }

    long int next()
    {
        this->state=(this->a*this->state+this->c)%this->m;
        return this->state;
    }
};

struct rozw
{
    long int a;
    long int c;
    long int m;
};

struct gcd_struct
{
    long int x;
    long int a;
    long int b;

    gcd_struct(long int x, long int a, long int b):x(x),a(a),b(b)
    {

    }

};

long int increment(long int a, long int m, std::vector < long int>s)
{
    return (s[1] - s[0]*a) % m;
}

gcd_struct mygcd(long int a, long int b)
{
    if (a==0)
        return gcd_struct(b,0,1);
    else
    {
        gcd_struct str= mygcd(b%a,a);
        return gcd_struct(str.x,str.b - (b/a)*str.a,str.a);
    }
}

long int mymod(long int a, long int b)
{
    gcd_struct str=mygcd(a,b);
    return str.a%b;
}

long int multipler(long int m, std::vector < long int> s)
{
    return (s[2] - s[1]) * mymod(s[1] - s[0], m) % m;
}

long int gcd(long int a, long int b)
{
    if (a == 0)
        return b;
    return gcd(b % a, a);
}

long int multgcd(std::vector < long int> v)
{
    long int result = v[0];
    for (size_t i=0; i<v.size()-1;i++)
    {
        result = gcd(result,v[i]);
    }
    return result;
}

long int modulu(std::vector < long int> s)
{
    std::vector < long int> d;
    for (size_t i =0;i<s.size()-1;i++)
    {
        d.push_back(s[i+1]-s[i]);
    }
    std::vector < long int> z;
    for (size_t i =0;i<d.size()-2;i++)
    {
        z.push_back(d[i+2]*d[i]-d[i+1]*d[i+1]);
    }


    return abs(multgcd(z));
}

int main()
{
    lcg gen(1211);
    std::vector < long int> states;
    for(int i=0;i<6;i++)
    {
        states.push_back(gen.next());
    }
    long int m = modulu(states);
    long int a=multipler(m,states);
    long int c = increment(a,m,states);
    cout<<a<<", "<<c<<","<<m<<endl;
}
