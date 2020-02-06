#include <bits/stdc++.h>

using namespace std;
#define MAXN 100
#define d(x) cout << #x << " = " << x << endl
#define forn(i, n) for(int i = 0; i < n; ++i)
#define fore(i, a, b) for(int i = a; i <= b; ++i)
#define INF (1 << 30)

int n = 0, m = 0;
int p[MAXN][MAXN] = {};

int order[MAXN] = {};
int t[MAXN][MAXN] = {};

int calcZ() {
  int curr, prev;

  fore(j, 1, n) {
    curr = order[j];
    prev = order[j - 1];

    fore(k, 1, m)
      t[curr][k] = max(t[prev][k] + p[prev][k], t[curr][k - 1] + p[curr][k - 1] + 1);
  }

  return t[curr][m] + p[curr][m];
}

int main() {
  cin >> n >> m;
  fore(j, 1, n) fore(k, 1, m) cin >> p[j][k];
  fore(j, 0, n) order[j] = j;
  do cout << calcZ() << endl;
  while(next_permutation(order + 1, order + n + 1));
}
