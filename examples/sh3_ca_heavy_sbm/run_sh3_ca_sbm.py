import os
import numpy as np
import subprocess as sb

import mdtraj as md

import model_builder as mdb
import model_builder.models.potentials as ptl
import simulation
import plot_eng

class HeavyStructureBasedModel(mdb.models.StructureBasedModel):

    def __init__(self, topology, mass, bead_repr=None):
        """Structure-based Model (SBM)

        Parameters
        ----------
        topology : mdtraj.Topology object
            An mdtraj Topology object that describes the molecular topology.

        bead_repr : str [CA, CACB]
            A code specifying the desired coarse-grain mapping. The all-atom 
        to coarse-grain mapping.

        """

        mdb.models.Model.__init__(self, topology, bead_repr=bead_repr)
        self.Hamiltonian = ptl.StructureBasedHamiltonian()
        self.mapping.add_atoms(mass=mass)

        self.Hamiltonian._default_parameters = {"kb":5., # kJ/(mol nm^2)
                                    "ka":2.*((np.pi/180.)**2),  # kJ/(mol deg^2)
                                    "kd":1.,     # kJ/mol
                                    "eps":1}     # kJ/(mol nm)

        self.Hamiltonian._default_potentials = {"bond":"HARMONIC_BOND",
                                "angle":"HARMONIC_ANGLE",
                                "dihedral":"COSINE_DIHEDRAL",
                                "improper_dihedral":"HARMONIC_DIHEDRAL",
                                "contact":"LJ1210"}

def sh3_ca_sbm():
    # Load all-atom pdb structure.
    traj = md.load("SH3.pdb")

    # Create CA structure-based model.
    model = HeavyStructureBasedModel(traj.top, 100, bead_repr="CA")
    #model = mdb.models.StructureBasedModel(traj.top, bead_repr="CA")

    # Create the Hamiltonian based off of the reference structure.
    model.set_reference(md.load("SH3.pdb"))

    model.assign_backbone()
    model.add_sbm_backbone()

    model.add_pairs(np.loadtxt("SH3.contacts", dtype=int) - 1)
    model.add_sbm_contacts()

    return model

def run_and_analyze():
    # Run the simulation
    sb.call("grompp_sbm -f run.mdp -c conf.gro -p topol.top -o topol.tpr", shell=True)
    sb.call("mdrun_sbm -s topol.tpr -table table.xvg -tablep tablep.xvg", shell=True)

    # Calculate each energy term
    sb.call("""g_energy_sbm -f ener.edr -s topol.tpr -xvg none -o Ebond_gmx.xvg << HERE
Bond
HERE""", shell=True)
    sb.call("""g_energy_sbm -f ener.edr -s topol.tpr -xvg none -o Eangle_gmx.xvg << HERE
Angle
HERE""", shell=True)
    sb.call("""g_energy_sbm -f ener.edr -s topol.tpr -xvg none -o Edih_gmx.xvg << HERE
Proper-Dih.
HERE""", shell=True)
    sb.call("""g_energy_sbm -f ener.edr -s topol.tpr -xvg none -o Epair_gmx.xvg << HERE
LJ-14
HERE""", shell=True)
    sb.call("""g_energy_sbm -f ener.edr -s topol.tpr -xvg none -o Epot_gmx.xvg << HERE
Potential
HERE""", shell=True)

if __name__ == "__main__":
    model = sh3_ca_sbm()

    ##################################
    # Run a constant Energy simlation
    ##################################
    if not os.path.exists("nve_data"):
        os.mkdir("nve_data")
    os.chdir("nve_data")

    # Save mdp file for NVE simulation (newtonian dynamics). We want to see the
    # oscillations in energy.
    with open("run.mdp", "w") as fout:
        fout.write(simulation.gromacs.mdp.constant_energy("1000000"))

    # Save remaining simulation files
    writer.write_simulation_files()
    run_and_analyze()
    plot_eng.plot_energy_terms(model, display=True)
    os.chdir("..")


    #######################################
    # Run a constant temperature simulation
    #######################################
    if not os.path.exists("nvt_data"):
        os.mkdir("nvt_data")
    os.chdir("nvt_data")

    # Save mdp file for NVT simulation (constant temperature).
    with open("run.mdp", "w") as fout:
        fout.write(simulation.gromacs.mdp.constant_temperature(10, "1000000"))

    # Save remaining simulation files
    writer.write_simulation_files()
    run_and_analyze()
    plot_eng.plot_energy_terms(model, display=True)

    os.chdir("..")
