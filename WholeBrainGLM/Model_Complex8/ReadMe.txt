Description & Goal

This model is designed to assess how many on screen items are requred to see dlPFC activity. 
Is 2 items enough? What about 3 items? Does it only work with a parametric regressor?
This should be compaired to model_Complex6

Regressors

0: Value - Parametric value (as provided by the DDM model (model6)) of the on screen option
1: Difficulty - Parametric difference in values (as provided by the DDM model (model6)) of the on screen option and the off screen option
2: Control - Task regressor for Control trials
3: Scaling - Task regressor for Scaling trials
4: Bundling - Task regressor for Bundling trials
5: TwoItems - Task regressor for when 2 items are on screen
6: ThreeItems - Task regressor for when 3 items are on screen
7: FourItems - Task regressor for when 4 items are on screen

# Contrasts
cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Difficulty','T', ['Difficulty'],[1]]
cont3 = ['sTwoItems>bTwoItems','T', ['sTwoItems','bTwoItems'],[1,-1]]
cont4 = ['sThreeItems>bThreeItems','T', ['sThreeItems','bThreeItems'],[1,-1]]
cont5 = ['sFourItems>bFourItems','T', ['sFourItems','bFourItems'],[1,-1]]
cont6 = ['sTwoItems>Control','T', ['sTwoItems','Control'],[1,-1]]
cont7 = ['sThreeItems>Control','T', ['sThreeItems','Control'],[1,-1]]
cont8 = ['sFourItems>Control','T', ['sFourItems','Control'],[1,-1]]
cont9 = ['bTwoItems>Control','T', ['bTwoItems','Control'],[1,-1]]
cont10 = ['bThreeItems>Control','T', ['bThreeItems','Control'],[1,-1]]
cont11 = ['bFourItems>Control','T', ['bFourItems','Control'],[1,-1]]

contrasts = [cont0,cont1,cont2,cont3,cont4,cont5,cont6,cont7,cont8,cont9,cont10,cont11]