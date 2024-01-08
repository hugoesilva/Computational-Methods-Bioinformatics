## **Assignment 6 - Some Final Questions**
### **Hugo Manuel Alves Henriques e Silva, hugoalv@student.chalmers.se**

### **`Question 1` - Give four examples of the application simulated annealing: two in bioinformatics (at least one of which should not have been described in the course lectures) and two examples in another area (not related to bioinformatics). For each example, briefly describe (i) how solutions are generated and (ii) how solutions are scored.**

### - Simulated annealing

Simulated annealing is a metaheuristic optimization algorithm that is used to find the global minimum of a function. It is inspired by the annealing process in metallurgy, where a metal is heated and then slowly cooled down to increase its purity. In simulated annealing, the function to be minimized is analogous to the energy of the metal, and the temperature is analogous to the probability of accepting a worse solution. The algorithm starts with a high temperature, which means that it is more likely to accept a worse solution. As the temperature decreases, the algorithm becomes less likely to accept a worse solution. This is done to avoid getting stuck in a local minimum. The temperature is decreased according to a cooling schedule, which is a function that determines how fast the temperature decreases. The algorithm stops when the temperature reaches zero.

### - First Example (Course Lecture 14) - HOLE Analysis of Ion Channel Pore Dimensions

HOLE is a program that calculates the dimensions of a protein channel. The dimensions of a protein channel are a function of the position of the atoms in the protein. The goal of HOLE is to find the dimensions of the protein channel.

- (i) How solutions are generated

        Initially, the user provides an initial point p inside the ion channel, which acts as a reference for the first plane perpendicular to the assumed path of the channel, represented by the vector v.

        Regarding sphere placement, for each plane, the program tries to place the largest possible sphere within the channel's boundaries. The sphere's center lies on the plane, and its size is constrained by the channel walls.

        The Metropolis Monte Carlo aspect comes into play as the program makes small, random adjustments to the sphere's position and size. Each adjustment is evaluated, and if it results in a better fit (i.e. a larger sphere without intersecting the channel walls), it is more likely to be accepted.

        Finally, the annealing the part of the process involves a temperature parameter that controls the acceptance of changes. Early on, when the temperature is high, the program is more willing to accept changes, even those that don't improve the fit significantly. This encourages exploration of the solution space. As the temperature decreases, the algorithm becomes more selective, converging on the optimal solution.

- (ii) How solutions are scored

        The scoring mechanism for the HOLE program is based on the fit of the sphere within the channel:

        The goal is to find the largest sphere that fits within the channel at each plane without intersecting the channel walls. This is a maximization problem where the radius of the sphere is directly proportional to the score.

        In addition to individual fits, the program also considers the consistency of the sphere sizes across consecutive planes. The goal is to characterize the channel's shape as accurately as possible, which may involve ensuring that the channel's diameter does not fluctuate unrealistically from one plane to the next.

        To finalize, the algorithm proceeds along the length of the channel, from the initial point p in both the direction of v and −v, and stops when it places a sphere with a radius exceeding 5 Å, indicating a significant widening of the channel.


### - Second Example (regarding Bionformatics) - Phylogenetic Tree Construction

Phylogenetic tree construction is the process of constructing a phylogenetic tree, which is a tree that represents the evolutionary relationships between a set of organisms. The evolutionary relationships between a set of organisms are a function of the genetic sequences of the organisms.

- (i) How solutions are generated

        As for the initial tree, we start with a random phylogenetic tree.

        For the perturbations, we make small random changes to the tree's structure.

        We use the Metropolis criterion to probabilistically accept or reject new trees based on a scoring function and the system's "temperature."

- (ii) How solutions are scored

        In order to score we evaluate trees using likelihood or parsimony methods and also temperature control, where we initially accept worse solutions at a higher "temperature," allowing exploration. As the "temperature" decreases, the algorithm becomes more selective, improving the chance of finding the optimal tree.

### - Third Example - Urban Planning and Facility Location

Urban planning is the process of designing and developing the urban environment. Facility location is the process of determining the location of facilities such as hospitals, schools, and fire stations. The goal of urban planning and facility location is to maximize the quality of life of the people living in the urban environment. The quality of life of the people living in the urban environment is a function of the location of the facilities.

- (i) How solutions are generated

        We can rely on simulated annealing to explore different configurations of facility locations. The algorithm might start with a random distribution of facilities and then iteratively move, add, or remove facilities to find an optimal layout.

- (ii) How solutions are scored

        The scoring is typically based on factors such as accessibility for the population (e.g., average distance to the nearest facility), cost of land and construction, and compliance with zoning laws or environmental regulations.

### - Fourth Example - Circuit Design Optimization

Circuit design is the process of designing electronic circuits. The goal of circuit design is to find a circuit that meets certain specifications. The specifications of a circuit are a function of the components of the circuit.

- (i) How solutions are generated

        Simulated annealing is able to optimize the placement of components and routing of connections. The process starts with an initial layout and then iteratively moves components or reroutes connections to improve the design.

- (ii) How solutions are scored

        The scoring in this context is based on criteria like the total area of the chip, length of interconnections (affecting signal transmission time and power consumption), and thermal properties. Additional considerations might include minimizing crosstalk and ensuring compliance with design rules.


### **`Question 2` - On page 972 of the article by Morris et al. (2002) the authors state: "The presence of cis-peptides adds an extra complication that we have chosen to ignore". Discuss this "complication", and why the authors chose to ignore it.**

The complication that the authors state is the presence of cis-peptides in protein structures. Most peptides are in the trans conformation, which means that the amino and carboxyl groups of adjacent amino acids are on opposite sides of the peptide bond. This results in a more favourable conformation in terms of energy, although peptides can occasionally be found in the cis conformation, where these groups are on the same side of the peptide bond.

Some of the reasons why the authors chose to ignore this complications are the frequency in which cis-peptides are found compared to trans peptides. Cis-peptides are way less common. This way, the model may not be impacted significantly by ignoring cis-peptides. Another reason is that the authors would need to find a way to incorporate cis-peptides into the model which would increase the complexity of the model significantly and potentially make it less efficient.

As a consequence, ARP/wARP will introduce chain breaks at cis-peptides.


### **`Question 3` - On page 219 of the article by Simons et al. (1997) the authors state: "the similarity in topology is clear ... in the contact map (Figure 9B)". Explain what the authors mean by this.**

The authors observed that best structure obtained by their protein folding simulations has a toplogy that resembles the native structure. By analysing the contact map, this similarity is evident. The simulation successfully replicated three-dimensional arrangement of the protein's amino acids as shown by the matching patterns in the contact map. The computer simulation was pointed out to be very effective at predicting the shape of a protein. 


### **`Question 4 a)` - Discuss how the concept of mesostates (as described by Gong et al. (2005), or Chellapa and Rose (2012)) could be used in performing structural alignment.**

Firstly, while Taylor and Orengo's method performs better when handling sequence variations and structural displacements,
the inregration of both sequencial and structural alignment will possibly make it too intensive in terms of the computation.

The mesostates approach makes the alignment process simpler by focusing on stable structural repeated elements like alpha helices and beta strands. This makes this approach effective for aligning proteins that are distantly related or those with significant structural flexibility.

Mesostates overlook some details in protein structures that Taylor and Orengo's method can capture, particularly some which are important for atomic interactions. The choice between these methods could depend on the specific requirements of the alignment task, whether we need detailed analysis or computational efficiency and the focus on key structural elements.


### **`Question 4 b)` - When a chatbot (like ChatGPT) was asked to answer part (a), its response included the following: (...) Discuss whether this response is accurate or useful.**

From what I found from the papers that have been provided, there's no reference to the MESODOCK approach which is referred to have been developed by Gong. Also, the references that are in the chatbot's response are not the ones that are in the paper. So, I would say that the response is not accurate or useful.


### **`Question 5` - Schenk et al. (2008) chose to use PDB entry 1KCT in their work since it was found to have "less than 7 % annotated α-helix or β-strand". However, the paper describing the protein α1-antitrypsin (Song et al. 1995) shows that this protein has nine α-helices and extensive β-sheets. Thus, these papers have different views about the secondary structure content of α1-antitrypsin. Explain why 1KCT was identified as an example of a protein with a very low amount of secondary structure.**

1KCT was identified as an example of a protein with a very low amount of secondary structure because of the fact that this protein, α1-antitrypsin, appears to have a significantly distorted structure. In spite of the usage of X-ray crystallography, methods that recgonize secondary structures do not find similar structures in the protein data bank due to its distortion. This is the reason why 1KCT was identified as an example of a protein with a very low amount of secondary structure. So the descrepancy between the two papers is due to the specific structure captured by the X-ray crystallography in 1KCT. While α1-antitrypsin might usually have nine α-helices and extensive β-sheets, the particular conformation captured in 1KCT is anomalously low in these regular secondary structures, due to its distorted state, which leads to one paper considering it as a protein with a very low amount of secondary structure whereas the other indicates a more complex secondary structure for α1-antitrypsin.


### **`Question 6` - When protein-ligand docking predictions are evaluated by comparing with a structure obtained by x.ray crystallography, "the RMSD cutoff of of 2 Å is often used as a criterion of the correct bound structure prediction" (Trott and Olson, 2009). Describe how the coordinates of the atoms of the protein and the ligand of the predicted complex and those of the crystallographic structure can be used to calculate the RMSD. If you foresee cases where this approach would give an RMSD error that does not reflect fairly the quality of the docking prediction, give an example of such a case. (Depending on your answer to the first part of this question, there might not be any such cases.)**

The goal of RMSD is to measure the similarity between two structures. So in this case, it will, at atomic level, compare how closely the predicted position of the ligand matches the ligand's position in the experimentally determined crystal structure


RMSD is calculated by aligning the predicted protein-ligand complex with the crystal structure and then measuring the average distance between the atoms of the ligand in the predicted and the experimental structures.

The RMSD is calculated as follows:


![RMSD](https://latex.codecogs.com/gif.latex?RMSD%20%3D%20%5Csqrt%7B%5Cfrac%7B1%7D%7BN%7D%5Csum_%7Bi%3D1%7D%5E%7BN%7D%28%7B%7C%7Cr_%7Bi%7D%5E%7Bexp%7D%20-%20r_%7Bi%7D%5E%7Bpred%7D%7C%7C%7D%5E%7B2%7D%29%7D)


where N is the number of atoms in the ligand, r_i^exp is the position of atom i in the experimental structure, and r_i^pred is the position of atom i in the predicted structure.


However, there is a chance that this approach may give a misleading representation of the docking prediction's quality. For example, if the ligand has a flexible part that doesn't significantly impact the binding interaction, this part might assume a different position in the predicted structure compared to the crystal structure. The resulting RMSD could be high, suggesting a bad prediction, even though the crucial part of the ligand that interacts with the protein is accurately positioned. This scenario highlights that while RMSD is a useful metric, it should be interpreted carefully and in the context of the specific molecular interactions involved.
