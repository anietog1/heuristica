#include <bits/stdc++.h>

using namespace std;
#define MAXN 100
#define d(x) cout << #x << " = " << x << endl
// puedo llegar hasta O(n3) maxn sería ~~500
// aunque si n fuera 100000, solo podría O(nlogn)
// vamos por ese :D

// minimizar la suma de todas las tardanzas por el peso

struct proc {
  int id, p, d, w; // id, duracion, tiempo limite, peso
};

int n;
proc procs[MAXN];

bool comp_risk_first(proc a, proc b) {
  return (a.d - a.p) * a.w > (b.d - b.p) * b.w;
}

int calc_t() {
  int t = 0, res = 0;

  for(int i = 0; i < n; ++i) {
    t += procs[i].p;

    if(t > procs[i].d)
      res += (t - procs[i].d) * procs[i].w;
  }

  return res;
}

void solve_fixed_point() {
  int min_t = (1 << 30), curr_t = (1 << 30 - 1);
  proc min_ans[n], curr_ans[n];

  while(curr_t < min_t) {
    min_t = curr_t;
    for(int i = 0; i < n; ++i) min_ans[i] = curr_ans[i];

    for(int i = 0; i < n; ++i) {
      for(int j = 0; j < n; ++j) {
        swap(curr_ans[i], curr_ans[j]);
        int temp_t = calc_t();

        if(temp_t < curr_t) {
          swap(curr_ans[i], curr_ans[j]);
        } else {
          swap(curr_ans[i], curr_ans[j]);
        }
      }
    }
  }
}

void solven3() {
  sort(procs, procs + n, comp_risk_first);

  int min_t = calc_t();
  for(int i = 0; i < n; ++i) {
    for(int j = i; j < n; ++j) {
      for(int k = i; k < j; ++k) {
        swap(procs[j], procs[k]);
        int tmp_t = calc_t();
        if(tmp_t < min_t) min_t = tmp_t;
        else swap(procs[j], procs[k]);
      }
    }
  }
}

int main(int argc, char** argv, char** env) {
  cin >> n;
  for(int i = 0; i < n; ++i) {
    procs[i].id = i;
    cin >> procs[i].p >> procs[i].d >> procs[i].w;
  }

  //solve_fixed_point();
  solven3();

  cout << "id p d w" << endl;
  for(int i = 0; i < n; ++i) {
    cout << procs[i].id << " "
         << procs[i].p << " "
         << procs[i].d << " "
         << procs[i].w << endl;
  }
  cout << endl << "Tardanza ponderada total: " << calc_t() << endl;
}
