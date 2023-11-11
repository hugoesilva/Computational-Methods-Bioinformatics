/*
 * To compile this C program, placing the executable file in '6_and_7', type:
 *
 *      gcc -o 6_and_7 6_and_7.c
 *
 * To run the program, type:
 *
 *      ./6_and_7
 */

/* 
6. Modify the program global_alignment.c (or equivalent) so that it counts the total number of 
    optimal alignments for the two sequences.
    Test your program with the sequences "ATTA" and "ATTTTA". 
*/

/* 	
7. Modify the program global_alignment.c (or equivalent) so that it writes out all of the optimal
    alignments for the two sequences.
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct cell {
    int left;
    int up;
    int diag;
} typedef cell;

#define MAX_LENGTH	100

#define MATCH_SCORE	2
#define MISMATCH_SCORE	-1
#define GAP_PENALTY	2

#define STOP		0
#define UP		    1
#define LEFT		2
#define DIAG		3
#define TEST        4

int	F[MAX_LENGTH+1][MAX_LENGTH+1];		/* score matrix */
int	trace[MAX_LENGTH+1][MAX_LENGTH+1];	/* trace matrix */
cell cell_matrix[MAX_LENGTH+1][MAX_LENGTH+1];
int numPaths = 0;
char pathsX[100][100];
char pathsY[100][100];
int alignLengths[100];

void printPath(int i, int j, char* s1, char* s2, char* alignX, char* alignY, int alignLength) {

    int i_copy;
    int j_copy;
    int alignLength_copy;

    while (trace[i][j] != STOP) {

        int max_value = cell_matrix[i][j].diag;

        i_copy = i;
        j_copy = j;
        alignLength_copy = alignLength;

        switch (trace[i][j]) {

            case DIAG:
                alignX[alignLength] = s1[i-1];
                alignY[alignLength] = s2[j-1];
                i--;
                j--;
                alignLength++;
                alignX[alignLength] = '\0';
                alignY[alignLength] = '\0';
                break;

            case LEFT:
                alignX[alignLength] = '-';
                alignY[alignLength] = s2[j-1];
                j--;
                alignLength++;
                alignX[alignLength] = '\0';
                alignY[alignLength] = '\0';
                break;

            case UP:
                alignX[alignLength] = s1[i-1];
                alignY[alignLength] = '-';
                i--;
                alignLength++;
                alignX[alignLength] = '\0';
                alignY[alignLength] = '\0';
                break;

            case TEST:
                if (cell_matrix[i][j].up > max_value) {
                    max_value = cell_matrix[i][j].up;
                }
                if (cell_matrix[i][j].left > max_value) {
                    max_value = cell_matrix[i][j].left;
                }
                
                if (cell_matrix[i][j].diag == max_value) {
                    char* new_alignX = malloc(200 * sizeof(char));
                    char* new_alignY = malloc(200 * sizeof(char));
                    strcpy(new_alignX, alignX);
                    strcpy(new_alignY, alignY);
                    new_alignX[alignLength] = s1[i-1];
                    new_alignY[alignLength] = s2[j-1];
                    i--;
                    j--;
                    alignLength++;
                    new_alignX[alignLength] = '\0';
                    new_alignY[alignLength] = '\0';
                    printPath(i, j, s1, s2, new_alignX, new_alignY, alignLength);
                }

                i = i_copy;
                j = j_copy;
                alignLength = alignLength_copy;

                if (cell_matrix[i_copy][j_copy].up == max_value) {
                    char* new_alignX = malloc(200 * sizeof(char));
                    char* new_alignY = malloc(200 * sizeof(char));
                    strcpy(new_alignX, alignX);
                    strcpy(new_alignY, alignY);
                    new_alignX[alignLength] = s1[i-1];
                    new_alignY[alignLength] = '-';
                    i--;
                    alignLength++;
                    new_alignX[alignLength] = '\0';
                    new_alignY[alignLength] = '\0';
                    printPath(i, j, s1, s2, alignX, alignY, alignLength);
                }

                i = i_copy;
                j = j_copy;
                alignLength = alignLength_copy;

                if (cell_matrix[i][j].left == max_value) {
                    char* new_alignX = malloc(200 * sizeof(char));
                    char* new_alignY = malloc(200 * sizeof(char));
                    strcpy(new_alignX, alignX);
                    strcpy(new_alignY, alignY);
                    new_alignX[alignLength] = '-';
                    new_alignY[alignLength] = s2[j-1];
                    j--;
                    alignLength++;
                    new_alignX[alignLength] = '\0';
                    new_alignY[alignLength] = '\0';
                    printPath(i, j, s1, s2, new_alignX, new_alignY, alignLength);
                }

                return;
        }
    }
        
    strcpy(pathsX[numPaths], alignX);
    strcpy(pathsY[numPaths], alignY);
    alignLengths[numPaths] = alignLength;
    numPaths++;

}


int main() { 
	int	i, j;
	int	m, n;
	int	score, tmp;
	char	X[MAX_LENGTH+1] = "ATTA";
	char	Y[MAX_LENGTH+1] = "ATTTTA";
    int alignmentLength;

	char	alignX[MAX_LENGTH*2];		/* aligned X sequence */
	char	alignY[MAX_LENGTH*2];		/* aligned Y sequence */


	/*
	 * Find lengths of (null-terminated) strings X and Y
	 */
	m = 0;
	n = 0;
	while (X[m] != 0) {
		m++;
	}
	while (Y[n] != 0) {
		n++;
	}


	/*
	 * Initialise matrices
	 */

	F[0][0] = 0;
	trace[0][0] = STOP;
	for (i = 1 ; i <= m; i++) {
		F[i][0] = F[i-1][0] - GAP_PENALTY;
		trace[i][0] = STOP;
	}
	for (j = 1; j <= n; j++) {
		F[0][j] = F[0][j-1] - GAP_PENALTY;
		trace[0][j] = STOP;
	}


 	/*
	 * Fill matrices
	 */

	for (i = 1; i <= m; i++) {

		for (j = 1; j <= n; j++) {
	
			if (X[i-1] == Y[j-1]) {
				score = F[i-1][j-1] + MATCH_SCORE;
			} 
			else {
				score = F[i-1][j-1] + MISMATCH_SCORE;
			}
			trace[i][j] = DIAG;
            cell_matrix[i][j].diag = score;

			tmp = F[i-1][j] - GAP_PENALTY;
            cell_matrix[i][j].up = tmp;
			if (tmp > score) {
				score = tmp;
				trace[i][j] = UP;
			}
            else if (tmp >= score) {
                trace[i][j] = TEST;
            }

			tmp = F[i][j-1] - GAP_PENALTY;
            cell_matrix[i][j].left = tmp;
			if(tmp > score) {
				score = tmp;
				trace[i][j] = LEFT;
			}
            else if (tmp >= score) {
                trace[i][j] = TEST;
            }

			F[i][j] = score;
 		}
	}


	/*
	 * Print score matrix
	 */

	printf("Score matrix:\n      ");
	for (j = 0; j < n; ++j) {
		printf("%5c", Y[j]);
	}
	printf("\n");

	for (i = 0; i <= m; i++) {
		if (i == 0) {
			printf(" ");
		} 
		else {
			printf("%c", X[i-1]);
		}
		for (j=0 ; j <= n; j++) {
			printf("%5d", F[i][j]);
		}
		printf("\n");
	}
	printf("\n");


	/*
	 * Trace back from the lower-right corner of the matrix
	 */

	i = m;
	j = n;
	alignmentLength = 0;

    printPath(i, j, X, Y, alignX, alignY, 0);

    printf("Number of optimal alignments: %d\n\n", numPaths);

    //print paths
    for (int k = 0; k < numPaths; k++) {

        printf("Optimal Alignment Number: %d\n", k+1);

        for (int l = alignLengths[k] - 1; l >= 0; l--) {
            printf("%c", pathsX[k][l]);
        }

        printf("\n");

        for (int l = alignLengths[k] - 1; l >= 0; l--) {
            if (pathsX[k][l] == pathsY[k][l]) {
                printf("|");
            }
            else {
                printf(" ");
            }
        }
        printf("\n");

        for (int l = alignLengths[k] - 1; l >= 0; l--) {
            printf("%c", pathsY[k][l]);
        }

        printf("\n");
        printf("-------------\n");
    }

	return 0;
}
