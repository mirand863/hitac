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
        69.5,
        80.3,
        19.7,
        # HiTaC_Filter
        64.8,
        69.3,
        10.3,
        # RDP50
        63.9,
        70.6,
        18.6,
        # BTOP
        63.7,
        73.4,
        26.6,
        # Microclass
        62.7,
        72.5,
        27.5,
        # Q2_SK
        62.4,
        68.5,
        18.8,
        # KTOP
        62.4,
        72.2,
        27.8,
        # TOP
        62.4,
        72.1,
        27.9,
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
    'sp_rdp_its_90_genus.pdf',
    bbox_inches="tight",
)
