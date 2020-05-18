#include <bits/stdc++.h>

using namespace std;
#define d(x) cerr << "[DEBUG] " << #x << " = " << x << endl
#define INF (1 << 30)
#define MAXN 1000

int n, m, L;
int p[MAXN][MAXN];
int t[MAXN][MAXN];
map<list<int>, bool> visited;

int calcz(list<int> const& jobs) {
  int curr, prev = -1;
  for(auto j = jobs.begin(); j != jobs.end(); ++j) {
    curr = *j;

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

void neh(int tries, int tofail) {
  auto begin = chrono::steady_clock::now();

  list<int> chosen, available;

  for(int i = 0; i < n; ++i) {
    available.push_back(i);
  }

  int duration[n] = {};
  for(int i = 0; i < n; ++i) {
    duration[i] = calcz({i});
  }

  available.sort([&duration](int j1, int j2) {
                   return duration[j1] < duration[j2];
                 });

  while(available.size() != 0) {
    int j = available.front();
    available.pop_front();

    int minz = (1 << 30);
    auto mini = chosen.end();

    bool last = false;
    for(auto i = chosen.begin(); !last; ++i) {
      chosen.insert(i, j);
      int tempz = calcz(chosen);

      if(tempz < minz) {
        minz = tempz;
        mini = i;
      }

      chosen.erase(prev(i));

      if(i == chosen.end()) {
        last = true;
      }
    }

    chosen.insert(mini, j);
  }

  visited[chosen] = true;
  int z = calcz(chosen);

  random_device rd;
  mt19937 gen(rd());
  uniform_int_distribution<> dis(0, n - 1);

  for(int i = 0; i < tries; ++i) {
    list<int> tmpchosen;

    int cnt = 0;
    do {
      tmpchosen = chosen;
      int idx1 = dis(gen), idx2 = dis(gen);
      auto it1 = tmpchosen.begin(), it2 = tmpchosen.begin();
      advance(it1, idx1);
      advance(it2, idx2);
      swap(*it1, *it2);
    } while(cnt++ < tofail && visited[tmpchosen]);

    visited[tmpchosen] = true;
    int tmpz = calcz(tmpchosen);

    if(tmpz < z) {
      chosen = tmpchosen;
      z = tmpz;
    }
  }

  calcz(chosen);

  auto end = chrono::steady_clock::now();

  for(int k = 0; k < m; ++k) {
    bool first = true;
    for(auto j : chosen) {
      if(first) {
        first = false;
      } else {
        cout << " ";
      }

      cout << j + 1 << " " << t[j][k];
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

  neh(1000, 20);
}
