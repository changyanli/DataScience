#include<stdio.h>
#include<stdlib.h>
#include<time.h> 
int main(int argc, char **argv) {
	srand(time(NULL));
	int nodes = 82168, edges = 2907369;
	int edge_count = 0;
	FILE* fp = fopen("test_data.txt", "w"); 
	bool **graph = new bool*[nodes - 1];
	for(int i = 0; i < nodes - 1; i++){
		graph[i] = new bool[nodes - 1 - i];
		for(int j = 0; j < nodes - 1 - i; j++){
			if(edge_count < edges && rand() % 10 == 0){
				edge_count++;
				graph[i][j] = true;
			}
			else
				graph[i][j] = false;
		}
	}
	for(int i = 0; i < nodes - 1; i++)
		for(int j = 0; j < nodes - 1 - i; j++)
			if(graph[i][j])
				fprintf(fp, "%d %d\n", i, i + j + 1);
	fclose(fp);
	return 0;
}

