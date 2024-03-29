This script is designed to adjust the partial charges of hydrogen atoms in a molecular structure file (MOL2 format). It ensures that the total charge of the molecule, particularly the ligand, is an integer (ideally neutral or a specific ionic charge). The script reads the original MOL2 file, calculates the sum of charges, and then distributes the necessary adjustments among the hydrogen atoms to achieve the desired total charge. The adjustments are made with precision to minimize any impact on the molecular structure and charge distribution, maintaining six decimal places of accuracy. After the adjustments, the script saves the new MOL2 file with updated charges. It also plots the percentage difference in charges of hydrogens before and after the adjustment for a visual representation of the changes.

### Key Steps and Equations

1. **Total Charge Calculation:**
   The total charge of the molecule is calculated as the sum of charges of all atoms in the molecule:
   $$Q_{total} = \sum_{i=1}^{n} q_i$$

2. **Adjustment Determination:**
   To achieve a desired total charge ($Q_{obj}\$) (e.g., 0 for neutral molecules), the necessary adjustment ($\Delta Q\$) is calculated as:
   $$\Delta Q = Q_{obj} - Q_{total}$$

3. **Distribution of Adjustment Among Hydrogens:**
   The adjustment per hydrogen ($\Delta q\$) is ideally distributed equally among all ($m\$) hydrogen atoms identified for adjustment:
   $$\Delta q = \frac{\Delta Q}{m}$$

### Implementation Details

The script includes functions for reading charges from a MOL2 file, adjusting hydrogen charges, formatting and saving the adjusted MOL2 file, and plotting the percentage differences in hydrogen charges. It is designed to be easily integrated into workflows requiring precise charge adjustments in molecular modeling projects.

### Motivation and Context

Adjusting the partial charges of hydrogen atoms is crucial for accurate molecular modeling and simulations. Incorrect charge distributions can lead to inaccurate predictions of molecular behavior, impacting the results of energy calculations, docking studies, and dynamic simulations. This script ensures the molecular charge is appropriately balanced, enhancing the reliability of molecular modeling projects.

### Limitations and Considerations

This script is optimized for small to medium-sized organic molecules. For large biomolecules or highly charged systems, additional validation of the adjusted charges is recommended to ensure accuracy.

### Contributions and Feedback

We welcome contributions and feedback on this script. If you have suggestions for improvements or have found an issue, please submit a pull request or open an issue on the GitHub repository page.
