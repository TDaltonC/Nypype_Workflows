Description & Goal

This model is designed to assess how many on screen items are requred to see dlPFC activity. 
Is 2 items enough? What about 3 items? Does it only work with a parametric regressor?
This should be compaired to model_Complex1

Regressors

0: Value - Parametric value (as provided by the max-likelihood model) of the on screen option
1: Difficulty - Parametric difference in values (as provided by the max-likelihood model) of the on screen option and the off screen option
2: TaskPos - Task regressor for all coice tials
3: ItmCount - Parametric regressor for the number of items on the screen. Then should be proportional to dlPFC activity

Contrasts

cont0 = ['TaskPos','T', ['TaskPos'],[1]]
cont1 = ['ItmCount','T', ['ItmCount'],[1]]
