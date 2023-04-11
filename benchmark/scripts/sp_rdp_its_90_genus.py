
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
        69.5,
        80.3,
        19.7,
        # BTOP
        63.7,
        73.4,
        26.6,
        # TOP
        62.4,
        72.1,
        27.9,
        # Microclass
        62.7,
        72.5,
        27.5,
        # KTOP
        62.4,
        72.2,
        27.8,
        # HiTaC_Filter
        64.8,
        69.3,
        10.3,
        # SINTAX50
        61.4,
        66.1,
        11.8,
        # SPINGO
        58.0,
        61.8,
        10.4,
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
