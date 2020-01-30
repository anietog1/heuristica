#include <bits/stdc++.h>

using namespace std;
#define MAXN 100000
// puedo llegar hasta O(n3) maxn sería ~~500
// aunque si n fuera 100000, solo podría O(nlogn)
// vamos por ese :D

// la idea es minimizar la suma de todos los
// (tiempo final de la actividad xi) * wi

struct proc {
  int id, p, w; // id, duracion, peso
  int t, tp; // tardanza, tardanza ponderada
};

int n;
proc procs[MAXN];

bool comp(proc a, proc b) {
  // Hipótesis: si Xi tiene un peso Wi y
  // este afecta al resultado haciendo que T = suma(Wi * Ti)
  // siendo Ti el tiempo final de la actividad i,
  // entonces es irrelevante si se realizan primero las actividades largas o las cortas
  // ya que la duración da igual
  // Todas las actividades de peso W se deberán considerar como una sola de peso W y así,
  // se deben priorizar las actividades de mayor peso
  if(a.w > b.w) return true;
  return a.p < b.p;
}

int calc_t() {
  int t = 0, res = 0;

  for(int i = 0; i < n; ++i) {
    t += procs[i].p;
    procs[i].t = t;
    procs[i].tp = t * procs[i].w;
    res += procs[i].tp;
  }

  return res;
}

int main(int argc, char** argv, char** env) {
  cin >> n;
  for(int i = 0; i < n; ++i) {
    procs[i].id = i;
    cin >> procs[i].p >> procs[i].w;
  }

  sort(procs, procs + n, comp);

  int ans = calc_t();

  cout << "id p w t tp" << endl;
  for(int i = 0; i < n; ++i) {
    cout << procs[i].id << " "
         << procs[i].p << " "
         << procs[i].w << " "
         << procs[i].t << " "
         << procs[i].tp << " "
         << endl;
  }
  cout << endl << "Flujo total: " << ans << endl;
}
