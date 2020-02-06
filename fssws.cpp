#include <bits/stdc++.h>

using namespace std;
#define MAXN 100
#define d(x) cout << #x << " = " << x << endl
#define forn(i, n) for(int i = 0; i < n; ++i)

int n, m;
int p[MAXN][MAXN];

int main() {
  cin >> n >> m;
  forn(j, n) forn(k, m) cin >> p[j][k];
}
