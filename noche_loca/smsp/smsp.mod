/*********************************************
 * OPL 12.9.0.0 Model
 * Author: agustin
 * Creation Date: Jan 31, 2020 at 5:15:54 AM
 *********************************************/
int M = 100000;

int n = ...;

range J = 1..n;

int p[J] = ...;
int d[J] = ...;
int w[J] = ...;

dvar int+ f[J];
dvar int+ t[J];
dvar int+ T[J];
dvar boolean x[J][J];

//minimize sum(j in J) w[j] * T[j]; // (tardanza ponderada)
minimize sum(j in J) w[j] * f[j]; // flujo

subject to {
	forall(j in J) {
	  f[j] == t[j] + p[j];
	  T[j] >= f[j] - d[j];
	  x[j][j] == 0;
	}

	forall(i in J) {
	  forall(j in J) {
	    if(i != j)
	    	t[j] >= f[i] - M * (1 - x[i][j]);
	    if(i < j)
	    	x[i][j] + x[j][i] == 1;
   	  }
    }
}

execute DISPLAY {
	var acum = 0;
	for(var j in J) acum = acum + T[j];
	writeln(acum);
}