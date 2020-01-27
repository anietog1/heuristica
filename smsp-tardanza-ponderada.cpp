#include <bits/stdc++.h>

using namespace std;
#define MAXN 600
#define d(x) cout << #x << " = " << x << endl
// puedo llegar hasta O(n3) maxn sería ~~500
// aunque si n fuera 100000, solo podría O(nlogn)
// vamos por ese :D

// minimizar la suma de todas las tardanzas por el peso

struct proc {
  int id, p, d, w; // id, duracion, tiempo limite, peso
  int t, tp; // tardanza, tardanza ponderada
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
    procs[i].t = max(0, (t - procs[i].d));
    procs[i].tp = procs[i].t * procs[i].w;
    res += procs[i].tp;
  }

  return res;
}

// void solve_fixed_point() {
//   int min_t = (1 << 30), curr_t = (1 << 30 - 1);
//   proc min_ans[n], curr_ans[n];

//   while(curr_t < min_t) {
//     min_t = curr_t;
//     for(int i = 0; i < n; ++i) min_ans[i] = curr_ans[i];

//     for(int i = 0; i < n; ++i) {
//       for(int j = 0; j < n; ++j) {
//         swap(curr_ans[i], curr_ans[j]);
//         int temp_t = calc_t();

//         if(temp_t < curr_t) {
//           swap(curr_ans[i], curr_ans[j]);
//         } else {
//           swap(curr_ans[i], curr_ans[j]);
//         }
//       }
//     }
//   }
// }

void solven3() {
  sort(procs, procs + n, comp_risk_first);

  int min_t = calc_t();
  // [ i k j ]
  // i asegura un lower bound que dejaremos de mover,
  // j determina el elemento que estamos acomodando actualmente
  // k sirve de indice para ir cambiando con j
  // el concepto es similar al bubble sort, donde vamos acomodando elemento por elemento "optimamente"
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

  solven3();

  int ans = calc_t();
  cout << "id p d w t tp" << endl;
  for(int i = 0; i < n; ++i) {
    cout << procs[i].id << " "
         << procs[i].p << " "
         << procs[i].d << " "
         << procs[i].w << " "
         << procs[i].t << " "
         << procs[i].tp << " "
         << endl;
  }
  cout << endl << "Tardanza ponderada total: " << ans << endl;
}
