from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D  # Needed to show molecules
from matplotlib import colors as mcolors

colors = [
    'lightpink',
    'lime',
    'yellow',
    'lightskyblue',
    'lavender',
    'gold',
    'azure',
    'beige',
]


class ArtistModel:
    def __init__(self, mm=False, predictions=[], layout=False):
        self.predictions = predictions
        self.layout = layout
        self.mol = mm.mol

    @classmethod
    def draw_ir(cls, mm=False, predictions=[], layout=False):
        instance = cls(mm=mm, predictions=predictions, layout=layout)
        svgs = instance.__draw_ir()
        return svgs

    def __draw_ir(self):
        fgs = [x['sma'] for x in self.predictions]
        drawer = rdMolDraw2D.MolDraw2DSVG(400, 400)

        for i, fg in enumerate(fgs):
            fg = Chem.MolFromSmarts(fg)
            target_atoms = self.mol.GetSubstructMatch(fg)

            target_bonds = []
            for idx, b in enumerate(self.mol.GetBonds()):
                bb = b.GetBeginAtomIdx()
                be = b.GetEndAtomIdx()
                if bb in target_atoms and be in target_atoms:
                    target_bonds.append(idx)

            farber = colors[i % len(colors)]
            color_atoms = {}
            for t in target_atoms:
                color_atoms[t] = mcolors.to_rgba(farber)
            color_bonds = {}
            for t in target_bonds:
                color_bonds[t] = mcolors.to_rgba(farber)

            drawer.DrawMolecule(
                self.mol,
                highlightAtoms=target_atoms,
                highlightAtomColors=color_atoms,
                highlightBonds=target_bonds,
                highlightBondColors=color_bonds,
            )
        svg = drawer.GetDrawingText().replace('svg:', '')
        return [svg]

    @classmethod
    def draw_nmr(cls, mm=False, predictions=[], layout=False):
        instance = cls(mm=mm, predictions=predictions, layout=layout)
        svgs = instance.__draw_nmr()
        return svgs

    def __identify_targets(self):
        atom_symbol = 'C' if self.layout == '13C' else 'H'

        targets = []
        for idx in range(self.mol.GetNumAtoms()):
            if self.mol.GetAtomWithIdx(idx).GetSymbol() == atom_symbol:
                targets.append(idx)
        return targets

    def __draw_nmr(self):
        targets = self.__identify_targets()
        colors = {}

        drawer = rdMolDraw2D.MolDraw2DSVG(400, 400)
        opts = drawer.drawOptions()

        for t in targets:
            opts.atomLabels[t] = str(t + 1)
            colors[t] = mcolors.to_rgba('yellow')

        drawer.DrawMolecule(
            self.mol,
            highlightAtoms=targets,
            highlightAtomColors=colors,
            highlightBonds=[]
        )
        drawer.FinishDrawing()

        svg = drawer.GetDrawingText().replace('svg:', '')
        return [svg]
