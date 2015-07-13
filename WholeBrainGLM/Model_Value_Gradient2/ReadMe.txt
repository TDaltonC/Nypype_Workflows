Description & Goal

This model is designed to assess if the value signal if different tasks is encoded in different places. 

Regressors
0: AverageValueC - Parametric value (as provided by the item based value model) of the on screen option (control only) (same as the value of the only item on the screen)
1: DifficultyC - Parametric difference in values (as provided by the item based value model) of the on screen option and the off screen option (control only)
2: AverageValueS - Parametric value (as provided by the item based value model) of the on screen option (Scaling only)
3: DifficultyS - Parametric difference in values (as provided by the item based value model) of the on screen option and the off screen option (Scaling only)
4: AverageValueB - Parametric value (as provided by the item based value model) of the on screen option (Bundling only)
5: DifficultyB - Parametric difference in values (as provided by the item based value model) of the on screen option and the off screen option (Bundling only)
6: Control - Task regressor for Control trials
7: Scaling - Task regressor for Scaling trials
8: Bundling - Task regressor for Bundling trials

# Contrasts
cont0 = ['AverageValueC','T', ['AverageValueC'],[1]]
cont1 = ['AverageDifficultyC','T', ['AverageDifficultyC'],[1]]
cont2 = ['AverageValueS','T', ['AverageValueS'],[1]]
cont3 = ['AverageDifficultyS','T', ['AverageDifficultyS'],[1]]
cont4 = ['AverageValueB','T', ['AverageValueB'],[1]]
cont5 = ['AverageDifficultyB','T', ['AverageDifficultyB'],[1]]

contrasts = [cont0,cont1,cont2,cont3,cont4,cont5]