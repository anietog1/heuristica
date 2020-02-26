#include <bits/stdc++.h>

using namespace std;
#define MAXN 1000
#define d(x) cout << "[DEBUG] " << #x << " = " << x << endl
#define forn(i, n) for(int i = 0; i < n; ++i)
#define fore(i, a, b) for(int i = a; i <= b; ++i)
#define INF (1 << 30)

int n = 0, m = 0, L = 0;
int p[MAXN][MAXN] = {};

int order[MAXN] = {};
int t[MAXN][MAXN] = {};

int calcZ(int j) {
  int curr = order[j], prev = order[j - 1];
  fore(k, 1, m)
    t[curr][k] = max(t[prev][k] + p[prev][k], t[curr][k - 1] + p[curr][k - 1]);
  return t[curr][m] + p[curr][m];
}

int calcZ() {
  fore(j, 1, n - 1)
    calcZ(j);
  return calcZ(n);
}

int calcZL(int j) {
  int curr = order[j], prev = order[j - 1];
  fore(k, 1, m) {
    int _t, _p = p[curr][k];
    _t = max(t[prev][k] + p[prev][k], t[curr][k - 1] + p[curr][k - 1]);
    if((_t + _p) / L == _t / L || (_t + _p) % L == 0 && _p <= L)
      t[curr][k] = _t;
    else
      t[curr][k] = _t + (L - _t % L);
  }
  return t[curr][m] + p[curr][m];
}

int calcZL() {
  fore(j, 1, n - 1)
    calcZL(j);
  return calcZL(n);
}

int calcLb() {
  pair<int, int> acum[n + 1];

  fore(j, 1, n) {
    acum[j].second = j;
    acum[j].first = 0;
    fore(k, 1, m) acum[j].first = p[j][k];
  }

  sort(acum + 1, acum + 1 + n);

  int lb = acum[n].first;
  fore(j, 1, n - 1) {
    lb += p[acum[j].second][m];
  }
  return lb;
}

int main() {
  cin >> n >> m >> L;
  fore(j, 1, n) fore(k, 1, m) cin >> p[j][k];
  fore(j, 0, n) order[j] = j;

  int z = INF, zL = INF, lb = INF;

  z = calcZ();
  cout << "z = " << z << endl;
  zL = calcZL();
  cout << "zL = " << zL << endl;
  cout << "order:";
  fore(i, 1, n) cout << " " << order[i];
  cout << endl;
  lb = calcLb();
  cout << "Lb = " << lb << endl;
}
