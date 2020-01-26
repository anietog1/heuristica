#include <bits/stdc++.h>

using namespace std;
// puedo llegar hasta O(n3) maxn sería ~~500
// aunque si n fuera 100000, solo podría O(nlogn)
// vamos por ese :D

// minimizar la suma de todas las tardanzas por el peso

struct proc {
  int id, p, d, w; // id, duracion, tiempo limite, peso
};

int main(int argc, char** argv, char** env) {
  int n; cin >> n;
  proc procs[n];
  for(int i = 0; i < n; ++i) {
    procs[i].id = i;
    cin >> procs[i].p >> procs[i].d >> procs[i].w;
  }

  cout << "Respuesta: " << endl;
  for(int i = 0; i < n; ++i)
    cout << procs[i].id << endl;
}
