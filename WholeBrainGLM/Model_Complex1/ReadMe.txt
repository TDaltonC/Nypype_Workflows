Description & Goal

This model is designed to assess how many on screen items are requred to see dlPFC activity. 
Is 2 items enough? What about 3 items? Does it only work with a parametric regressor?
This should be compaired to model_Complex2

Regressors

0: Value - Parametric value (as provided by the max-likelihood model) of the on screen option
1: Difficulty - Parametric difference in values (as provided by the max-likelihood model) of the on screen option and the off screen option
2: Control - Task regressor for Control trials
3: TwoItems - Task regressor for when 2 items are on screen
4: ThreeItems - Task regressor for when 3 items are on screen
5: FourItems - Task regressor for when 4 items are on screen

Contrasts

cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Difficulty','T', ['Difficulty'],[1]]
cont3 = ['TwoItems','T', ['TwoItems'],[1]]
cont4 = ['ThreeItems','T', ['ThreeItems'],[1]]
cont5 = ['FourItems','T', ['FourItems'],[1]]
cont6 = ['TwoItems>Control','T', ['TwoItems','Control'],[1,-1]]
cont7 = ['ThreeItems>Control','T', ['ThreeItems','Control'],[1,-1]]
cont8 = ['FourItems>Control','T', ['FourItems','Control'],[1,-1]]