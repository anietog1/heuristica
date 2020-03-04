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

  return t[curr][m - 1];
}

int neh() {
  vector<int> chosen, available;

  for(int i = 0; i < n; ++i) {
    available.push_back(i);
  }

  while(available.size() != 0) {
    int minz = (1 << 30), minj, index;

    for(int i = 0; i <= chosen.size(); ++i) {
      for(int j = 0; j < available.size(); ++j) {
        vector<int> temp(chosen.begin(), chosen.begin() + i);
        temp.push_back(available[j]);
        temp.insert(temp.end(), chosen.begin() + i, chosen.end());

        int tempz = calcz(temp);
        if(tempz < minz) {
          minz = tempz;
          minj = j;
          index = i;
        }
      }
    }

    chosen.insert(chosen.begin() + index, available[minj]);
    available.erase(available.begin() + minj);
  }

  int z = calcz(chosen);

  for(int k = 0; k < m; ++k) {
    for(int j = 0; j < n; ++j) {
      if(j != 0) {
        cout << " ";
      }

      cout << chosen[j] + 1 << " " << t[chosen[j]][k];
    }

    cout << endl;
  }

  return z;
}

int main() {
  auto begin = chrono::steady_clock::now();
  cin >> n >> m >> L;

  for(int j = 0; j < n; ++j) {
    for(int k = 0; k < m; ++k) {
      cin >> p[j][k];
    }
  }

  cerr << neh() << endl;

  auto end = chrono::steady_clock::now();
  cerr << "Time elapsed = "
       << chrono::duration_cast<chrono::microseconds>(end - begin).count()
       << "[μs] = "
       << chrono::duration_cast<chrono::milliseconds>(end - begin).count()
       << "[ms]" << endl;
}
