Description & Goal

This model is designed to assess how many on screen items are requred to see dlPFC activity. 
Is 2 items enough? What about 3 items? Does it only work with a parametric regressor?
This should be compaired to model_Complex2

Regressors

2: Control - Task regressor for Control trials
3: TwoItems - Task regressor for when 2 items are on screen
4: ThreeItems - Task regressor for when 3 items are on screen
5: FourItems - Task regressor for when 4 items are on screen

Contrasts

cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['TwoItems','T', ['TwoItems'],[1]]
cont2 = ['ThreeItems','T', ['ThreeItems'],[1]]
cont3 = ['FourItems','T', ['FourItems'],[1]]
cont4 = ['TwoItems>Control','T', ['TwoItems','Control'],[1,-1]]
cont5 = ['ThreeItems>Control','T', ['ThreeItems','Control'],[1,-1]]
cont6 = ['FourItems>Control','T', ['FourItems','Control'],[1,-1]]