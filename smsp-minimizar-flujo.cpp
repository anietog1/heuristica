#include <bits/stdc++.h>

using namespace std;
// puedo llegar hasta O(n3) maxn sería ~~500
// aunque si n fuera 100000, solo podría O(nlogn)
// vamos por ese :D

// la idea es minimizar la suma de todos los
// (tiempo final de la actividad xi) * wi

struct proc {
  int id, p, w; // id, duracion, peso
};

int main(int argc, char** argv, char** env) {
  int n; cin >> n;
  proc procs[n];
  for(int i = 0; i < n; ++i) {
    procs[i].id = i;
    cin >> procs[i].p >> procs[i].w;
  }

  cout << "Respuesta: " << endl;
  for(int i = 0; i < n; ++i)
    cout << procs[i].id << endl;
}
