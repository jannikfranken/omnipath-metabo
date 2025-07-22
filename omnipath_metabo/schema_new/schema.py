from django.db import models
from django.db.models.constraints import CheckConstraint
from django.db.models import F

class Structure(models.Model):
    """
    Represents a chemical structure.

    Attributes:
        structure_id (int): Unique identifier
        smiles (str): SMILES representation
        mol (str): MOL table representation
        is_polymer (bool): Whether the structure is a polymer
        has_stereo (bool): Whether the structure has stereochemistry
        has_conformation (bool): Whether the structure has a conformation
        complete_formula (bool): Whether the structure is a complete formula

    Notes:
        For Mol, define a new field type "MolType" like Forrest did. Create class which inherits from models.Field
        djanko-rdkit plugin (quite old)   
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
        identifier (str): Metabolite ID
        id_type (str): Identifier type

    Notes:
        
    """
    metabolite_identifier_id = models.AutoField(primary_key=True)
    identifier = models.CharField(max_length=1000)
    id_type = models.ForeignKey(Resource, on_delete=models.CASCADE)


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
    resource_id = models.ForeignKey(Resource, on_delete=models.CASCADE)
    authoritative = models.BooleanField()
    preferred = models.BooleanField()


## check the ondelete=CASCACE. what is the directionality? how does it work?


class Resource(models.Model):
    """
    Represents a resource.

    Attributes:
        resource_id (int): Unique identifier
        name (str): Resource name
    """
    resource_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)

## how does CORNETO represent reactions as hypergraphs? Maybe this can be used here

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
    evidence = models.ManyToManyField(Evidence)
    type = models.ForeignKey(ReactionType, on_delete=models.CASCADE)


class ReactionType(models.Model):
    """
    Represents a reaction type.

    Attributes:
        reaction_type_id (int): Unique identifier
        name (str): Reaction type name
    """
    reaction_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)


## what is a manytomany field in django?

class Participant(models.Model):
    """
    Represents a reaction participant for chemical reactions.

    Attributes:
        entity_group_id (int): Chemical group identifier
        reaction_id (int): Reaction identifier
        role (str): Participant role

    Notes:
        notes
    """
    participant_id = models.AutoField(primary_key=True)
    reaction_id = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    entity_group_id = models.ForeignKey(EntityGroup, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)



class Role(models.Model):   
    """
    Represents a role.

    Attributes:
        role_id (int): Unique identifier
        name (str): Role name (Enzyme, Catalysator, Product-Metabolite, Transporter, Inhibitor, ...)
    """
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)



class EntityGroup(models.Model):
    """
    Represents an entity group.

    Attributes:
        entity_group_id (int): Unique identifier
        name (str): Entity group name (Protein, metabolite, drug, amino acid, ...)
        type (str): Entity group type (compound, protein, ...)

    Notes:
        How does and EntityGroup look like?:
        Can be:
            - a set of compounds or structures, 
            - a set of chemical classes
            - a ChEBI key
            - a protein or protein class
    """
    entity_group_id = models.AutoField(primary_key=True)
    type = models.ForeignKey(EntityType.type, on_delete=models.CASCADE)
    structure_id = models.ForeignKey(Structure, on_delete=models.CASCADE)
    protein_state_id = models.ForeignKey(ProteinState, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            CheckConstraint(
                check=  '''
                        (structure_id IS NOT NULL AND protein_state_id IS NULL AND type = 'structure') OR
                        (protein_state_id IS NOT NULL AND structure_id IS NULL AND type = 'protein_state')
                        ''',  ## others will follow
                name='only_one_entity_id'
            )
        ]



class EntityType(models.Model):
    """
    Represents an entity type.

    Attributes:
        entity_type_id (int): Unique identifier
        name (str): Entity type name
    """
    class KnownTypes(models.IntegerChoices):
        structure = 1, "structure"
        protein = 2, "protein_state"

    type = models.PositiveSmallIntegerField(
        choices=KnownTypes.choices    
        ## default=KnownTypes.structure
    )



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
    enzyme_class_id = models.ManyToManyField(EnzymeClass)
    uniprot = models.CharField(max_length=50)
    genesymbol = models.CharField(max_length=50)
    organism = models.IntegerField()



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
    name = models.CharField(max_length=50)



class ProteinState(models.Model):
    """
    Represents a protein state.

    Attributes:
        protein_state_id (int): Unique identifier
        protein_id (int): Protein identifier

    Notes:
        A protein can have different states, like localizations, PTMs
        There might be a default state or an unknown state
    """
    protein_state_id = models.AutoField(primary_key=True)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)
    ptm = models.ManyToManyField(Ptm)
    localization = models.ManyToManyField(Localization)

##go over docstings everywhere

class Ptm(models.Model):
    """
    Represents a protein state attribute.

    Attributes:
        ptm_id (int): Unique identifier
        ...
    """
    ptm_id = models.AutoField(primary_key=True)
    redisue = models.CharField(max_length=1)  ## the amino acid
    offset = models.IntegerField()  ## number of amino acid in the proteins sequence
    type = models.CharField(max_length=1000)  ## acetylation, phosphorylation, ...



class Localization(models.Model):
    """
    Represents a protein state attribute.

    Attributes:
        localization_id (int): Unique identifier
        ...
    """
    localization_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=1000)



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
    resource_id = models.ForeignKey(Resource, on_delete=models.CASCADE)
    reference_id = models.ForeignKey(Reference)
    type = models.CharField(max_length=1000)



class Reference(models.Model):
    """
    Represents a reference.

    Attributes:
        reference_id (int): Unique identifier
        pmid (int): PubMed identifier
    """
    reference_id = models.AutoField(primary_key=True)
    pmid = models.IntegerField(unique=True)








# class ProteinRole(models.Model):
#     """
#     Represents a protein role.

#     Attributes:
#         protein_role_id (int): Unique identifier
#         protein_id (int): Protein identifier
#         role (str): Role

#     Notes:
#         ProteinRole for a protein could be enzyme, receptor, transporter, ...
#     """
#     protein_role_id = models.AutoField(primary_key=True)
#     protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)
#     role = models.CharField(max_length=1000)
