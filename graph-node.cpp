#include <bits/stdc++.h>

using namespace std;
#define d(x) cerr << "[DEBUG] " << #x << " = " << x << endl
#define INF (1 << 30)
#define MAXN 1000

int n, m, L;

int g[MAXN][MAXN] = {};
int p[MAXN][MAXN] = {};
int t[MAXN][MAXN] = {};
int visited[MAXN] = {};

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

// if i == -1 => choosefirst
int chooseNext(int prev) { // proporcion: 4 3 3
  vector<pair<int, int>> next;

  if(prev == -1) {
    for(int i = 0; i < n; ++i) {
      next.push_back(make_pair(g[i][i], i));
    }
  } else {
    for(int i = 0; i < n; ++i) {
      if(!visited[i]) {
        next.push_back(make_pair(g[prev][i], i));
      }
    }
  }

  sort(next.begin(), next.end());
  uniform_real_distribution<> dist(0.0, 1.0); 

  std::random_device rd;
  std::mt19937 gen(rd());
  double value = dist(gen);

  int answer = next[0].second;

  if(value > 0.5 && next.size() >= 2) {
    answer = next[1].second;
  }

  if(value > 0.8 && next.size() >= 3) {
    answer = next[2].second;
  }

  return answer;
}

void graph() {
  auto begin = chrono::steady_clock::now();

  int tries = 100;
  int globalminz = (1 << 30);
  vector<int> globalminorder;

  while(tries--) {
    for(int i = 0; i < n; ++i) {
      for(int j = 0; j < n; ++j) {
        g[i][j] = calcz({i, j}) - calcz({j});
      }
    }

    uniform_real_distribution<> dist(0.0, 1.0); 
    std::random_device rd;
    std::mt19937 gen(rd());

    for(int i = 0; i < n; ++i) {
      for(int j = 0; j < n; ++j) {
        double rand = dist(gen);
        if(rand <= 0.03) {
          g[i][j] = (1 << 30);
        }
      }
    }

    vector<int> order;
    for(int i = 0; i < n; ++i) visited[i] = false;

    int first = chooseNext(-1);
    order.push_back(first);
    visited[first] = true;

    while(order.size() != n) {
      int prev = order[order.size() - 1];
      int next = chooseNext(prev);
      order.push_back(next);
      visited[next] = true;
    }

    int localz = calcz(order);

    if(localz < globalminz) {
      globalminz = localz;
      globalminorder = order;
    }
  }

  int z = globalminz;
  vector<int> order = globalminorder;

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
