Description & Goal

This model is designed to assess how goods values interactions are computed. What brain regions are active for positive interactions (peanut butter and jelly)? for nagative interactions(katchup and coke)? It should be compared to model 8. 
It should be compared to Model_Goods_Interaction2, it has two interaction terms. One for positive interactions and one for negative interactions. 
Value Modle -- This model uses a Drift diffusion model to assess the value of each option. The value of each option is asumed to be drawn from the same distribution for all subjects. 

(also visualize the distributions of interactions)

Regressors

0: Value - Parametric value of the on screen option
1: Difficulty - Parametric difference in values of the on screen option and the off screen option
2: Control - Task regressor for Control trials
3: Scaling - Task regressor for Scaling trials
4: Bundling - Task regressor for Bundling trials
5: Interaction - Value of an option -minus- the sum of the values of the parts 

Contrasts

# Contrasts
cont0 = ['Value','T', ['Value'],[1]]
cont1 = ['Difficulty','T', ['Difficulty'],[1]]
cont2 = ['Interaction','T',['Interaction'],[1]]

contrasts = [cont0,cont1,cont2]