Description & Goal

This model is designed to assess if the value signal if different tasks is encoded in different places. 

Regressors
0: ValueC - Parametric value (as provided by the MLE) of the on screen option (control only)
1: DifficultyC - Parametric difference in values (as provided by the MLE) of the on screen option and the off screen option (control only)
2: ValueS - Parametric value (as provided by the MLE) of the on screen option (Scaling only)
3: DifficultyS - Parametric difference in values (as provided by the MLE) of the on screen option and the off screen option (Scaling only)
4: ValueB - Parametric value (as provided by the MLE) of the on screen option (Bundling only)
5: DifficultyB - Parametric difference in values (as provided by the MLE) of the on screen option and the off screen option (Bundling only)
6: Control - Task regressor for Control trials
7: Scaling - Task regressor for Scaling trials
8: Bundling - Task regressor for Bundling trials

# Contrasts
cont0 = ['ValueC','T', ['ValueC'],[1]]
cont1 = ['DifficultyC','T', ['DifficultyC'],[1]]
cont2 = ['ValueS','T', ['ValueS'],[1]]
cont3 = ['DifficultyS','T', ['DifficultyS'],[1]]
cont4 = ['ValueB','T', ['ValueB'],[1]]
cont5 = ['DifficultyB','T', ['DifficultyB'],[1]]

contrasts = [cont0,cont1,cont2,cont3,cont4,cont5]