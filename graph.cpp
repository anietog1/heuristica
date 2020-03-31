#include <bits/stdc++.h>

using namespace std;
#define d(x) cerr << "[DEBUG] " << #x << " = " << x << endl
#define INF (1 << 30)
#define MAXN 1000

int n, m, L;
int p[MAXN][MAXN];
int t[MAXN][MAXN];

int calcz(vector<int> const& jobs) {
  int curr, prev = -1;
  for(int j = 0; j < jobs.size(); ++j) {
    curr = jobs[j];

    for(int k = 0; k < m; ++k) {
      int _t = 0, _p = p[curr][k];

      if(prev != -1) {
        _t = max(_t, t[prev][k] + p[prev][k]);
      }

      if(k != 0) {
        _t = max(_t, t[curr][k - 1] + p[curr][k - 1]);
      }

      int c = _t + _p;
      if((c / L == _t / L) || ((c % L == 0) && (_p <= L))) {
        t[curr][k] = _t;
      } else {
        t[curr][k] = _t + (L - _t % L);
      }
    }

    prev = curr;
  }

  return t[curr][m - 1] + p[curr][m - 1];
}

int lb() {
  int maxsum = 0;

  for(int k = 0; k < m; ++k) {
    int sum = 0;

    for(int j = 0; j < n; ++j) {
      sum += p[j][k];
    }

    maxsum = max(maxsum, sum);
  }

  return maxsum;
}


void graph() {
  auto begin = chrono::steady_clock::now();

  int g[n][n] = {};
  for(int i = 0; i < n; ++i) {
    for(int j = 0; j < n; ++j) {
      g[i][j] = calcz({i, j});
    }
  }

  vector<int> order;
  bool visited[n] = {};

  int minz = (1 << 30), mini;
  for(int i = 0; i < n; ++i) {
    int tempz = calcz({i});

    if(tempz < minz) {
      minz = tempz;
      mini = i;
    }
  }

  order.push_back(mini);
  visited[mini] = true;

  while(order.size() != n) {
    int prev = order[order.size() - 1];
    minz = (1 << 30);

    for(int i = 0; i < n; ++i) {
      if(!visited[i] && g[prev][i] < minz) {
        minz = g[prev][i];
        mini = i;
      }
    }

    order.push_back(mini);
    visited[mini] = true;
  }

  int z = calcz(order);

  auto end = chrono::steady_clock::now();

  for(int k = 0; k < m; ++k) {
    for(int j = 0; j < n; ++j) {
      if(j != 0) {
        cout << " ";
      }

      cout << order[j] + 1 << " " << t[order[j]][k];
    }

    cout << endl;
  }

  int _lb = lb();
  cerr << chrono::duration_cast<chrono::microseconds>(end - begin).count()
       << " " << chrono::duration_cast<chrono::milliseconds>(end - begin).count() << endl;
  cerr << z << " " << _lb << " " << double(z - _lb) / _lb << endl;
}

int main() {
  cin >> n >> m >> L;

  for(int j = 0; j < n; ++j) {
    for(int k = 0; k < m; ++k) {
      cin >> p[j][k];
    }
  }

  graph();
}
