import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

results = pd.DataFrame(data={
    'method': [
        'HiTaC',
        'HiTaC',
        'HiTaC',
        'HiTaC_Filter',
        'HiTaC_Filter',
        'HiTaC_Filter',
        'RDP50',
        'RDP50',
        'RDP50',
        'BTOP',
        'BTOP',
        'BTOP',
        'Microclass',
        'Microclass',
        'Microclass',
        'Q2_SK',
        'Q2_SK',
        'Q2_SK',
        'KTOP',
        'KTOP',
        'KTOP',
        'TOP',
        'TOP',
        'TOP',
    ],
    'metric': [
        # HiTaC
        'Accuracy',
        'Sensitivity',
        'MCR',
        # HiTaC_Filter
        'Accuracy',
        'Sensitivity',
        'MCR',
        # RDP50
        'Accuracy',
        'Sensitivity',
        'MCR',
        # BTOP
        'Accuracy',
        'Sensitivity',
        'MCR',
        # Microclass
        'Accuracy',
        'Sensitivity',
        'MCR',
        # Q2_SK
        'Accuracy',
        'Sensitivity',
        'MCR',
        # KTOP
        'Accuracy',
        'Sensitivity',
        'MCR',
        # TOP
        'Accuracy',
        'Sensitivity',
        'MCR',
    ],
    'result': [
        # HiTaC
        100.0,
        100.0,
        0.0,
        # HiTaC_Filter
        97.8,
        97.8,
        0.0,
        # RDP50
        96.2,
        96.2,
        2.9,
        # BTOP
        100.0,
        100.0,
        0.0,
        # Microclass
        99.4,
        99.4,
        0.6,
        # Q2_SK
        95.3,
        95.3,
        0.8,
        # KTOP
        99.4,
        99.4,
        0.6,
        # TOP
        99.6,
        99.6,
        0.4,
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
