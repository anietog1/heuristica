#include <bits/stdc++.h>

using namespace std;
#define D(x) cerr << "[DEBUG] " << #x << " = " << x << endl
#define INF (1 << 30)

struct node_t {
  int id; /* id: j * n + k + 1*/
  int j, k; /* corresponds to job j on machine k */
  int es, ef; /* early start, early finish */
  int ls, lf; /* late start, late finish */
  int d, s; /* duration, slack */
  vector<int> prev; /* parent nodes (ids) */
  vector<int> next; /* child nodes (ids) */
  vector<int> resources; /* resource requirements */
};

struct problem_t {
  int n, m, L; /* n jobs, m machines, L turn time */
  vector<vector<int>> p; /* duration of each job on each machine */
  vector<vector<int>> t; /* start time of each job on each machine */
  vector<node_t> g; /* graph of jobs for rcsp */
};

int id(int j, int k, problem_t& p) {
  /* 0 is reserved for first, n * m + 1 is for last*/
  return j * p.m + k + 1;
}

void read_problem(problem_t& p) {
  /* basic */
  cin >> p.n >> p.m >> p.L;

  /* p */
  p.p.resize(p.n);
  for(auto& vec : p.p) {
    vec.resize(p.m);
  }

  for(int j = 0; j < p.n; ++j) {
    for(int k = 0; k < p.m; ++k) {
      cin >> p.p[j][k];
    }
  }

  /* t */
  p.t.resize(p.n);
  for(auto& vec : p.t) {
    vec.resize(p.m);
  }
}

void build_graph(problem_t& p) {
  p.g.resize(p.n * p.m + 2);
  for(int i = 0; i < p.g.size(); ++i) {
    p.g[i].id = i;
    p.g[i].resources.resize(p.m, 0);
  }

  auto& first = p.g.front();
  auto& last = p.g.back();

  for(int j = 0; j < p.n; ++j) {
    for(int k = 0; k < p.m; ++k) {
      auto& curr = p.g[id(j, k, p)];

      curr.j = j;
      curr.k = k;
      curr.resources[k] = 1;

      if(k > 0) {
        curr.prev.push_back(id(j, k - 1, p));
      } else {
        first.next.push_back(curr.id);
        curr.prev.push_back(first.id);
      }

      if(k < p.m - 1) {
        curr.next.push_back(id(j, k + 1, p));
      } else {
        curr.next.push_back(last.id);
        last.prev.push_back(curr.id);
      }
    }
  }
}

int main() {
  problem_t p;
  read_problem(p);
  build_graph(p);
}
