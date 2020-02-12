#include <bits/stdc++.h>

using namespace std;
#define MAXN 100
#define d(x) cout << #x << " = " << x << endl
#define forn(i, n) for(int i = 0; i < n; ++i)
#define fore(i, a, b) for(int i = a; i <= b; ++i)
#define INF (1 << 30)
#define pii pair<int, int>

int n = 0, m = 0;
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

int calcZ10(int j) {
  int curr = order[j], prev = order[j - 1];
  fore(k, 1, m) {
    int _t, _p = p[curr][k];
    _t = max(t[prev][k] + p[prev][k], t[curr][k - 1] + p[curr][k - 1]);
    if((_t + _p) / 10 == _t / 10 || (_t + _p) % 10 == 0 && _p <= 10)
      t[curr][k] = _t;
    else
      t[curr][k] = _t + (10 - _t % 10);
  }
  return t[curr][m] + p[curr][m];
}

int calcZ10() {
  fore(j, 1, n - 1)
    calcZ10(j);
  return calcZ10(n);
}

int main() {
  cin >> n >> m;
  fore(j, 1, n) fore(k, 1, m) cin >> p[j][k];
  fore(j, 0, n) order[j] = j;

  int z = INF, z10 = INF;

  // los trabajos con mayor suma(p[j][k] ** 2) van primero
  // sorpresivamente da peor resultado que no sortear
  pii pondered[n + 1];
  fore(j, 1, n) {
    pondered[j].second = j;
    pondered[j].first = 0;
    fore(k, 1, m) pondered[j].first += p[j][k] * p[j][k];
  }
  sort(pondered + 1, pondered + 1 + n);
  fore(j, 1, n) order[j] = pondered[j].second;

  z = calcZ();
  cout << "z = " << z << endl;
  z10 = calcZ10();
  cout << "z10 = " << z10 << endl;
  cout << "order:";
  fore(i, 1, n) cout << " " << order[i];
  cout << endl;
}
