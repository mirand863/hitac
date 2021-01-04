import q2_hitac

from ._classify import classify

from q2_types.feature_data import (FeatureData, Taxonomy, Sequence)
import qiime2
from qiime2.plugin import (Plugin, Metadata, Citations, Int)

TaxonomicClassifier = qiime2.plugin.SemanticType('TaxonomicClassifier')

citations = Citations.load('citations.bib', package='q2_hitac')

PARAMETERS = {'metadata': Metadata}
PARAMETERS_DESC = {
    'metadata': 'The sample metadata.'
}

plugin = Plugin(
    name='hitac',
    version=q2_hitac.__version__,
    website='https://gitlab.com/dacs-hpi/hitac',
    package='q2_hitac',
    citations=Citations.load('citations.bib', package='q2_hitac'),
    description=('This QIIME 2 plugin wraps HiTaC and '
                 'supports hierarchical taxonomic classification.'),
    short_description='Plugin for hierarchical '
                      'taxonomic classification with HiTaC.'
)

plugin.methods.register_function(
    function=classify,
    inputs={'reference_reads': FeatureData[Sequence],
            'reference_taxonomy': FeatureData[Taxonomy],
            'query': FeatureData[Sequence]},
    parameters={'kmer': Int, 'threads': Int},
    outputs=[('classification', FeatureData[Taxonomy])],
    name='HiTaC',
    description='Hierarchical logistic regression classifier',
    citations=[citations['miranda2020hitac']]
)
