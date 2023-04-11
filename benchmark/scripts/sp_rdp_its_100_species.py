import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

results = pd.DataFrame(data={
    'method': [
        'HiTaC',
        'HiTaC',
        'HiTaC',
        'BTOP',
        'BTOP',
        'BTOP',
        'TOP',
        'TOP',
        'TOP',
        'Microclass',
        'Microclass',
        'Microclass',
        'KTOP',
        'KTOP',
        'KTOP',
        'HiTaC_Filter',
        'HiTaC_Filter',
        'HiTaC_Filter',
        'SINTAX50',
        'SINTAX50',
        'SINTAX50',
        'SPINGO',
        'SPINGO',
        'SPINGO',
    ],
    'metric': [
        # HiTaC
        'Accuracy',
        'Sensitivity',
        'Misclassification rate',
        # BTOP
        'Accuracy',
        'Sensitivity',
        'Misclassification rate',
        # TOP
        'Accuracy',
        'Sensitivity',
        'Misclassification rate',
        # Microclass
        'Accuracy',
        'Sensitivity',
        'Misclassification rate',
        # KTOP
        'Accuracy',
        'Sensitivity',
        'Misclassification rate',
        # HiTaC_Filter
        'Accuracy',
        'Sensitivity',
        'Misclassification rate',
        # SINTAX50
        'Accuracy',
        'Sensitivity',
        'Misclassification rate',
        # SPINGO
        'Accuracy',
        'Sensitivity',
        'Misclassification rate',
    ],
    'result': [
        # HiTaC
        100.0,
        100.0,
        0.0,
        # BTOP
        100.0,
        100.0,
        0.0,
        # TOP
        99.6,
        99.6,
        0.4,
        # Microclass
        99.4,
        99.4,
        0.6,
        # KTOP
        99.4,
        99.4,
        0.6,
        # HiTaC_Filter
        97.8,
        97.8,
        0.0,
        # SINTAX50
        97.4,
        97.4,
        0.4,
        # SPINGO
        96.8,
        96.8,
        0.0,
    ]
})

sns.set_theme(
    style="whitegrid",
    font_scale=3,
)

# Draw a nested barplot
g = sns.catplot(
    data=results,
    kind="bar",
    x="method",
    y="result",
    hue="metric",
    errorbar=None,
    palette="dark",
    alpha=.8,
    # height=6,
    aspect=4,
)
g.despine(left=True)
g.set_axis_labels("", "")
g.legend.set_title("")
# g._legend.remove()
plt.ylim(0, 100)
plt.yticks([0, 25, 50, 75, 100], [0, 25, 50, 75, 100])
plt.xticks(rotation=25)
# plt.show()
plt.savefig(
    'sp_rdp_its_100_species.pdf',
    bbox_inches="tight",
)
