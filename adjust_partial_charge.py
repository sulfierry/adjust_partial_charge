"""
    This script, is designed for adjusting the partial charges of hydrogen atoms in a molecular structure file (MOL2 format). 
    It ensures that the total charge of the molecule, particularly the ligand, is an integer (ideally neutral or a specific ionic charge). 
    The script reads the  original MOL2 file, calculates the sum of charges, and then distributes the necessary adjustments among the hydrogen 
    atoms to achieve the desired total charge. The adjustments are made with precision to minimize any impact on the molecular structure and charge 
    distribution, maintaining six decimal places accuracy. After the adjustments, the script saves the new MOL2 file with updated charges. It also 
    plots the percentage difference in charges of hydrogens before and after the adjustment for a visual representation of the changes. 
"""

import matplotlib.pyplot as plt

class ChargeAdjust:
    def __init__(self, input_name):
        self.input_name = input_name
        self.output_name = input_name.replace('.mol2', '_adjusted.mol2')
    
    def read_mol2_charges(self):
        charges = []
        with open(self.input_name, 'r') as file:
            start = False
            for line in file:
                if line.startswith("@<TRIPOS>ATOM"):
                    start = True
                    continue
                elif line.startswith("@<TRIPOS>"):
                    start = False
                if start:
                    parts = line.split()
                    if len(parts) > 8:
                        charge = float(parts[8])
                        charges.append(charge)
        return charges

    def adjust_hydrogen_charges(self, charges):
        original_charges = charges.copy()
        total_charge = sum(charges)
        adjustment_needed = -total_charge

        hydrogens = [i for i, charge in enumerate(charges) if charge > 0]
        if not hydrogens:
            print("Nenhum átomo de hidrogênio encontrado para ajuste.")
            return charges

        # Distribui o ajuste inicial
        adjustment_per_hydrogen = adjustment_needed / len(hydrogens)
        for i in hydrogens:
            charges[i] += adjustment_per_hydrogen
            charges[i] = round(charges[i], 6)

        # Ajuste final para correção de pequenas discrepâncias
        final_total_charge = sum(charges)
        if abs(final_total_charge) >= 0.000001:
            # Escolhe o hidrogênio com a menor variação absoluta após o ajuste
            min_variation_index = min(hydrogens, key=lambda i: abs((original_charges[i] + adjustment_per_hydrogen) - charges[i]))
            charges[min_variation_index] -= final_total_charge
            charges[min_variation_index] = round(charges[min_variation_index], 6)

        return charges

    def format_atom_line(self, line, charge):
        parts = line.split()
        formatted_charge = f"{charge:.6f}" if charge != -0.000000 else "0.000000"
        parts[8] = formatted_charge
        return "{:<7s}{:<11s}{:>10s}{:>10s}{:>10s} {:<5s}{:>4s} {:<4s}{:>10s}\n".format(*parts)

    def save_adjusted_mol2(self, adjusted_charges):
        with open(self.input_name, 'r') as file:
            lines = file.readlines()

        charge_index = 0
        for i in range(len(lines)):
            if lines[i].startswith("@<TRIPOS>ATOM"):
                start = i + 1
                break

        for i in range(start, len(lines)):
            if lines[i].startswith("@<TRIPOS>"):
                break
            parts = lines[i].split()
            if len(parts) > 8:
                lines[i] = self.format_atom_line(lines[i], adjusted_charges[charge_index])
                charge_index += 1

        with open(self.output_name, 'w') as file:
            file.writelines(lines)

    def store_charge_data(self, mol2_file):
        charge_data = []
        with open(mol2_file, 'r') as file:
            start = False
            
            for line in file:
                if line.startswith("@<TRIPOS>ATOM"):
                    start = True
                    continue
                elif line.startswith("@<TRIPOS>"):
                    start = False
                if start:
                    parts = line.split()
                    if len(parts) > 8:
                        atom = parts[1]
                        charge = float(parts[8])
                        charge_data.append((atom, charge))
        return charge_data

    def calculate_percentage_differences(self, initial_data, corrected_data):
        percentage_differences = []
        for (atom_initial, charge_initial), (atom_corrected, charge_corrected) in zip(initial_data, corrected_data):
            if 'H' in atom_initial:  # Considering only hydrogens
                percentage_difference = ((charge_corrected - charge_initial) / charge_initial) * 100 if charge_initial != 0 else 0
                percentage_differences.append((atom_initial, percentage_difference))
        return percentage_differences

    def plot_percentage_differences(self, percentage_differences):
        atoms, differences = zip(*percentage_differences)
        differences = [abs(difference) for difference in differences]  # Usa valores absolutos

        # Filtra diferenças para garantir que pequenas variações sejam visíveis
        min_diff_threshold = 0.001  # Define um limiar mínimo de diferença percentual para visualização
        filtered_differences = [diff if diff >= min_diff_threshold else min_diff_threshold for diff in differences]

        plt.figure(figsize=(12, 6))
        plt.bar(atoms, filtered_differences, color='purple')
        plt.xlabel("Hydrogen Atoms")
        plt.ylabel("Percentage Difference (%)")
        plt.title("Percentage Difference in Partial Charges of Hydrogens After Adjustment")
        plt.xticks(rotation=45)

        # Ajusta os limites do eixo Y de forma condicional
        if all(diff == min_diff_threshold for diff in filtered_differences):
            plt.ylim([0, min_diff_threshold * 2])  # Ajusta manualmente se todas as diferenças são mínimas
        else:
            plt.ylim([0, max(filtered_differences) * 1.1])  # Usa a maior diferença para definir o limite superior

        plt.savefig('adjust_partial_charge.png')
        plt.show()



    def main(self):
        charges_before = self.read_mol2_charges()
        total_charges_before = sum(charges_before)
        print(f"Total charge before adjustment: {total_charges_before:.6f}")

        adjusted_charges = self.adjust_hydrogen_charges(charges_before)
        total_charges_adjusted = sum(adjusted_charges)
        print(f"Total charge after adjustment: {total_charges_adjusted:.6f}")

        self.save_adjusted_mol2(adjusted_charges)

        initial_data = self.store_charge_data(self.input_name)
        corrected_data = self.store_charge_data(self.output_name)
        percentage_differences = self.calculate_percentage_differences(initial_data, corrected_data)
        self.plot_percentage_differences(percentage_differences)

if __name__ == "__main__":
    charge_adjuster = ChargeAdjust('ligand.mol2')
    charge_adjuster.main()
