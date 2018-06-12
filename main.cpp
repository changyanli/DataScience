#include<stdio.h>
#include<stdlib.h> 
//#include<windows.h>
#include<time.h>
#include<vector>
using namespace std;
const int V = 500;//82168;
vector< vector<bool> > graph(V, vector<bool> (V, false)); 
vector<int> count =vector<int>(V, 0);
vector<int> list;
int maximal_clique = 0;
vector<bool> MAX_Clique;
/*
Set MAX_Clique;
Set intersect(Set S, int p){
	Set X;
	X.size = S.size;
	X.s = vector<bool>(V, false);
	for(int i = 0; i < V; ++i){
		X.s[i] = S.s[i];
		if(S.s[i] && !graph[p][i]){
			X.s[i] = false;
			X.size--;
		}	
	}
	return X;
}
*/
void backtrack(vector<bool>& R, vector<bool>& P, vector<bool>& X){
	int nodes_num = 0, index, pivot;
	for (index = 0; index < V; index++){
		if(P[index] || R[index])
			nodes_num ++;
		if(nodes_num > maximal_clique)
			break;
	}
	
	if(index == V)
		return;
	
	for (pivot = 0; pivot < V; pivot++)
		if(P[pivot] || X[pivot])
			break;
	if(pivot == V){
		int count = 0;
		for(int i = 0; i < V; i++)
			if(R[i])
				count ++;
		if(count > maximal_clique){
			maximal_clique = count;
			MAX_Clique = R;
		}
		return;
	}	
	for (int i = 0; i < V; i++)
		if(P[i] && !graph[pivot][i]){
			if(count[i] < maximal_clique)
				continue;
			vector<bool> P_new(V), R_new(R), X_new(V);
			int number = 0;
			for(int j = 0; j < V; j++){
				if(graph[i][j]){
					number++;
					if(P[j])
						P_new[j] = true;
					if(X[j])
						X_new[j] = true;
					if(number == count[i])
						break;
				}
			} 
			R_new[i] = true;
			backtrack(R_new, P_new, X_new);
			P[i] = false;
			X[i] = true;
		}
}
int main(int argc, char **argv) {
	FILE *fp = fopen(argv[1], "r");
	int from, to;
	int min_dim = 100;
	while(fscanf(fp, "%d %d", &from, &to) != EOF){
		graph[from][to] = true;
		graph[to][from] = true;
		count[from] ++;
		count[to] ++; 
	}
	vector<bool> R(V), P(V, true), X(V);
    for(int index = 0; index < graph.size(); index++){
		if(count[index] < min_dim){
			P[index] = false;
		}
	}
	backtrack(R, P, X);
	FILE *fout = fopen(argv[2], "w");
	printf("Maximal_clique %d ",maximal_clique);
	for(int i = 0; i < V; i++)
		if(MAX_Clique[i])
			fprintf(fout,"%d\n", i);
	return 0;
}

