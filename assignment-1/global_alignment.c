/*
 * To compile this C program, placing the executable file in 'global', type:
 *
 *      gcc -o global global_alignment.c
 *
 * To run the program, type:
 *
 *      ./global
 */

#include <stdio.h>

#define MAX_LENGTH	100

#define MATCH_SCORE	2
#define MISMATCH_SCORE	-1
#define GAP_PENALTY	2

#define STOP		0
#define UP		    1
#define LEFT		2
#define DIAG		3


int main() { 
	int	i, j;
	int	m, n;
	int	alignmentLength, score, tmp;
	char	X[MAX_LENGTH+1] = "ATCGAT";
	char	Y[MAX_LENGTH+1] = "ATACGT";

	int	F[MAX_LENGTH+1][MAX_LENGTH+1];		/* score matrix */
	int	trace[MAX_LENGTH+1][MAX_LENGTH+1];	/* trace matrix */
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

			tmp = F[i-1][j] - GAP_PENALTY;
			if (tmp > score) {
				score = tmp;
				trace[i][j] = UP;
			}

			tmp = F[i][j-1] - GAP_PENALTY;
			if(tmp > score) {
				score = tmp;
				trace[i][j] = LEFT;
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

	while (trace[i][j] != STOP) {

		switch (trace[i][j]) {

			case DIAG:
				alignX[alignmentLength] = X[i-1];
				alignY[alignmentLength] = Y[j-1];
				i--;
				j--;
				alignmentLength++;
				break;

			case LEFT:
				alignX[alignmentLength] = '-';
				alignY[alignmentLength] = Y[j-1];
				j--;
				alignmentLength++;
				break;

			case UP:
				alignX[alignmentLength] = X[i-1];
				alignY[alignmentLength] = '-';
				i--;
				alignmentLength++;
		}
	}

	/*
	 * Unaligned beginning
	 */

	while ( i>0 ) {
		alignX[alignmentLength] = X[i-1];
		alignY[alignmentLength] = '-';
		i--;
		alignmentLength++;
	}

	while ( j>0 ) {
		alignX[alignmentLength] = '-';
		alignY[alignmentLength] = Y[j-1];
		j--;
		alignmentLength++;
	}

	/*
	 * Print alignment
	 */

	for (i = alignmentLength - 1; i >= 0 ; i--) {
		printf("%c",alignX[i]);
	}
	printf("\n");

	/* ------------------------------------------------------------------------------------------------ */

	/* 
		1. Modify the program global_alignment.c (or equivalent) so that an extra line of output is printed
		 between the two aligned sequence, indicating exact matches with the character "|", e.g.
	*/

	for (i = alignmentLength - 1; i >= 0; i--) {
		if (alignX[i] == alignY[i]) {
			printf("|");
		} 
		else {
			printf(" ");
		}
	}
	printf("\n");

	/* ------------------------------------------------------------------------------------------------ */

	for (i = alignmentLength - 1; i >= 0; i--) {
		printf("%c",alignY[i]);
	}
	printf("\n");

	/* ------------------------------------------------------------------------------------------------ */

	/* 
		2. Modify the program global_alignment.c (or equivalent) so that the percent identity between the two 
		 sequences is written out.Add a comment to your program explaining how you have decided to calculate 
		 the percent identity.
	*/

	/*
		To calculate the percent identity, we can use various different methods. The possibilities are dividing
		the number of matching characters by:
		- the length of the shortest sequence
		- the length of the longest sequence
		- the length of the alignment
		- the average length of the sequences
		- the number of non-gap positions
		- the number of equivalenced positions excluding overhangs

		I decided to use the length of the alignment as a way of calculating the percent identity.
	*/

	// calculate the number of matches

	int matches = 0;
	for (i = alignmentLength - 1; i >= 0; i--) {
		if (alignX[i] == alignY[i]) {
			matches++;
		}
	}

	// calculate the percent identity

	float percentIdentity = (float) matches / alignmentLength * 100;

	printf("Percent identity: %.2f%%\n", percentIdentity);

	/* ------------------------------------------------------------------------------------------------ */

	/* 
		3. Modify the program global_alignment.c (or equivalent) to output the Hamming distance between 
		 the aligned sequence strings.
	*/

	// The Hamming distance is the number of positions at which the corresponding characters are different.
	// It is important to note that the Hamming distance is only defined for strings of equal length. To make
	// both strings the same size, a "-" character is added to the beginning of the shorter string. Furthermore
	// "-" is being considered as a character, so it is not ignored.

	int hammingDistance = 0;
	for (i = alignmentLength - 1; i >= 0; i--) {
		if (alignX[i] != alignY[i]) {
			hammingDistance++;
		}
	}

	printf("Hamming distance: %d\n", hammingDistance);

	/* ------------------------------------------------------------------------------------------------ */

	return 0;
}
