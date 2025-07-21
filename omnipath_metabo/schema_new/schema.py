from django.db import models


class Structure(models.Model):
    """
    Represents a chemical structure.

    Attributes:
        structure_id (int): Unique identifier
        smiles (str): SMILES representation
        mol (str): MOL representation
        is_polymer (bool): Whether the structure is a polymer
        has_stereo (bool): Whether the structure has stereochemistry
        has_conformation (bool): Whether the structure has a conformation
        complete_formula (bool): Whether the structure is a complete formula

    Notes:
         A chemical structure is connected to a identifier. Which one?
    """
    structure_id = models.AutoField(primary_key=True)
    smiles = models.CharField(max_length=1000, unique=True)
    mol = models.TextField()
    is_polymer = models.BooleanField()
    has_stereo = models.BooleanField()
    has_conformation = models.BooleanField()
    complete_formula = models.BooleanField()



class MetaboliteIdentifier(models.Model):
    """
    Represents a metabolite identifier

    Attributes:
        metabolite_identifier_id (int): Unique identifier
        identifier (str): Metabolite identifier
        id_type (str): Identifier type

    Notes:
        MetaboliteIdentifyer -> connection to structure?
    """
    metabolite_identifier_id = models.AutoField(primary_key=True)
    identifier = models.CharField(max_length=1000)
    id_type = models.CharField(max_length=1000)
    chemical_group_id = models.ForeignKey(ChemicalGroup, on_delete=models.CASCADE)


class StructureIdentifyer(models.Model):
    """
    Represents a structure identifier.

    Attributes:
        structure_identifier_id (int): Unique identifier
        structure_id (int): Structure identifier
        identifier_id (int): Metabolite identifier

    Notes:
        A StructureIdentifier is connected to a Structure (structure and a MetaboliteIdentifier)?
    """
    structure_identifier_id = models.AutoField(primary_key=True)
    structure_id = models.ForeignKey(Structure, on_delete=models.CASCADE)
    metabolite_identifier_id = models.ForeignKey(MetaboliteIdentifier, on_delete=models.CASCADE)
    chemical_group_id = models.ForeignKey(ChemicalGroup, on_delete=models.CASCADE)


class PreferredName(models.Model):
    """
    Represents a preferred name of a molecule.

    Attributes:
        preferred_name_id (int): Unique identifier
        name (str): Preferred name
        id_type (str): Identifier type
    
    Notes:
        For lipids, the LipidMaps name is preferred
        For other molecules, the HMDB name is preferred. If there is no HMDB name, then Reactome
        Others might be PubChem, chEMBL, Rxnorm for drugs
    """
    preferred_name_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    id_type = models.CharField(max_length=1000)



class Reaction(models.Model):
    """
    Represents a chemical reaction.

    Attributes:
        reaction_id (int): Unique identifier
        smiles (str): SMILES representation
        mol (str): MOL representation

    Notes:
        A chemical reaction can be specifief by a smiles string or mol table
    """
    reaction_id = models.AutoField(primary_key=True)
    smiles = models.CharField(max_length=1000)
    mol = models.TextField()
    participants = models.ManyToManyField(ReactionParticipant)



class ReactionParticipant(models.Model):
    """
    Represents a reaction participant for chemical reactions.

    Attributes:
        reaction_participant_id (int): Unique identifier
        chemical_group_id (int): Chemical group identifier
        reaction_id (int): Reaction identifier
        role (str): Participant role

    Notes:
        notes
    """
    reaction_participant_id = models.AutoField(primary_key=True)
    reaction_id = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    chemical_group_id = models.ForeignKey(ChemicalGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=1000)



class ReactionEvidence(models.Model):
    """
    Represents a reaction evidence for a chemical reaction.

    Attributes:
        reaction_evidence_id (int): Unique identifier
        reaction_id (int): Reaction identifier
        evidence_id (int): Evidence identifier

    Notes:
        notes
    """
    reaction_evidence_id = models.AutoField(primary_key=True)
    reaction_id = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    evidence_id = models.CharField(max_length=1000)



class Evidence(models.Model):
    """
    Represents a general evidence entry.

    Attributes:
        evidence_id (int): Unique identifier
        resource_id (str): Resource identifier
        reference_id (str): Reference identifier
        type (str): Evidence type (experimental, prediction, ...)

    Notes:
        resource_id: A specific publication, database entry, ...
    """
    evidence_id = models.AutoField(primary_key=True)
    resource_id = models.CharField(max_length=1000)
    reference_id = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)


class ChemicalGroup(models.model):
    """
    Represents a chemical group.

    Attributes:
        chemical_group_id (int): Unique identifier
        smiles (str): SMILES representation
        mol (str): MOL representation

    Notes:
        Which kind of chemical group is a compound/metabolite/protein/...
    """
    chemical_group_id = models.AutoField(primary_key=True)
    smiles = models.CharField(max_length=1000)
    mol = models.TextField()


class EnzymeClass(models.Model):
    """
    Represents an enzyme class.

    Attributes:
        enzyme_class_id (int): Unique identifier
        name (str): Enzyme class name

    Notes:
        Which kind of enzyme class is a enzyme/protein/...
    """
    enzyme_class_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)


class Participant(models.Model):
    """
    Represents a participant.

    Attributes:
        participant_id (int): Unique identifier
        name (str): Participant name

    Notes:
        A participant can be involved in other things like a normal reaction?
    """
    participant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)



class Protein(models.Model):
    """
    Represents a protein.

    Attributes:
        protein_id (int): Unique identifier
        uniprot (str): UniProt identifier
        genesymbol (str): Gene symbol
        enzyme_class_id (int): Enzyme class identifier
        organism (str): Organism
    """
    protein_id = models.AutoField(primary_key=True)
    enzyme_class_id = models.ForeignKey(EnzymeClass, on_delete=models.CASCADE)
    uniprot = models.CharField(max_length=1000)
    genesymbol = models.CharField(max_length=1000)
    organism = models.CharField(max_length=1000)


class ProteinRole(models.Model):
    """
    Represents a protein role.

    Attributes:
        protein_role_id (int): Unique identifier
        protein_id (int): Protein identifier
        role (str): Role

    Notes:
        ProteinRole for a protein could be enzyme, receptor, transporter, ...
    """
    protein_role_id = models.AutoField(primary_key=True)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)
    role = models.CharField(max_length=1000)


class ProteinState(models.Model):
    """
    Represents a protein state.

    Attributes:
        protein_state_id (int): Unique identifier
        protein_id (int): Protein identifier
        state (str): State

    Notes:
        A protein can have different states, like localizations, PTMs
        There might be a default state or an unknown state
    """
    protein_state_id = models.AutoField(primary_key=True)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)
    state = models.CharField(max_length=1000, default="unknown")


class ProteinAttribute(models.Model):
    """
    Represents a protein attribute.

    Attributes:
        protein_attribute_id (int): Unique identifier
        type (str): Attribute type
        value (str): Attribute value

    Notes:
        need to figure out the differences betweent ProteinState and ProteinAttribute
    """
    protein_attribute_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=1000)
    value = models.CharField(max_length=1000)


class ProteinStateAttribute(models.Model):
    """
    Represents a protein state attribute.

    Attributes:
        protein_state_attribute_id (int): Unique identifier
        protein_state_id (int): Protein state identifier
        type (str): Attribute type
        value (str): Attribute value

    Notes:
        Also need to figure this one out
    """
    protein_state_attribute_id = models.AutoField(primary_key=True)
    protein_state_id = models.ForeignKey(ProteinState, on_delete=models.CASCADE)
    protein_attribute_id = models.ForeignKey(ProteinAttribute, on_delete=models.CASCADE)


class ReactionCausality(models.Model):
    """
    Represents a reaction causality.

    Attributes:
        reaction_causality_id (int): Unique identifier
        reaction_id (int): Reaction identifier
        participant_id_a (int): Participant identifier
        participant_id_b (int): Participant identifier
        effect (str): Effect

    Notes:
        A reaction can have different effects, like stimulation, inhibition, ...
    """
    reaction_causality_id = models.AutoField(primary_key=True)
    reaction_id = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    participant_id_a = models.ForeignKey(Participant, on_delete=models.CASCADE)
    participant_id_b = models.ForeignKey(Participant, on_delete=models.CASCADE)
    effect = models.CharField(max_length=1000)


class MetaboliteProteinInteraction(models.Model):
    """
    Represents a metabolite-protein interaction.

    Attributes:
        metabolite_protein_interaction_id (int): Unique identifier
        metabolite_identifier_id (int): Metabolite identifier
        protein_id (int): Protein identifier
        effect (str): Effect of interaction (activation, inhibition, ...)
        type (str): Type of interaction (allosteric, ligand-receptor, ...)

    Notes:
        notes
    """
    metabolite_protein_interaction_id = models.AutoField(primary_key=True)
    metabolite_identifier_id = models.ForeignKey(MetaboliteIdentifier, on_delete=models.CASCADE)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)
    effect = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)



class InteractionEvidence(models.Model):
    """
    Represents an interaction evidence.

    Attributes:
        interaction_evidence_id (int): Unique identifier
        interaction_id (int): Interaction identifier
        evidence_id (int): Evidence identifier

    Notes:
        notes
    """
    interaction_evidence_id = models.AutoField(primary_key=True)
    interaction_id = models.ForeignKey(MetaboliteProteinInteraction, on_delete=models.CASCADE)
    evidence_id = models.ForeignKey(Evidence, on_delete=models.CASCADE)



class InteractionBindingAffinity(models.Model):
    """
    Represents an interaction binding affinity.

    Attributes:
        interaction_binding_affinity_id (int): Unique identifier
        interaction_id (int): Interaction identifier
        binding_affinity (float): Binding affinity

    Notes:
        which type of data is binding_affinity?
        normalize similar to pChembl?
    """
    interaction_binding_affinity_id = models.AutoField(primary_key=True)
    interaction_id = models.ForeignKey(MetaboliteProteinInteraction, on_delete=models.CASCADE)
    binding_affinity = models.FloatField(default=0.0)













