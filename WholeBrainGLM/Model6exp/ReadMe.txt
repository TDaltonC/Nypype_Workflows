Description & Goal

This model is designed to assess the differences between the three tasks. It should be compared to model 6 (same as this but the values aren't used as an exponate).

Value Model -- For this model the value of the options was estomated by a max-likelihood model that used all tasks ["CSBValue"] (model1 only used the control and scaling tasks). It also includes a fixed dumby for bunding and a different fixed dumby for scaling). This value is then used as the exponate of e.

Regressors

0: Value - Parametric value of the on screen option
1: Difficulty - Parametric difference in values of the on screen option and the off screen option
2: Control - Task regressor for Control trials
3: Scaling - Task regressor for Scaling trials
4: Bundling - Task regressor for Bundling trials

# Contrasts
cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Difficulty','T', ['Difficulty'],[1]]
cont3 = ['Scaling','T', ['Scaling'],[1]]
cont4 = ['Bundling','T', ['Bundling'],[1]]
cont5 = ['Scaling>Control','T', ['Scaling','Control'],[1,-1]]
cont6 = ['Bundling>Control','T', ['Bundling','Control'],[1,-1]]
cont7 = ['Bundling>Scaling','T', ['Bundling','Scaling'],[1,-1]]
cont8 = ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont9 = ['Scaling+Bundling>Control','T', ['Scaling','Bundling','Control'],[.5,.5,-1]]
contrasts = [cont0,cont1,cont2,cont3,cont4,cont5,cont6,cont7,cont8,cont9]

# ROI Masks
ROI_Masks = [os.path.abspath('../ROIs/HOMiddleFrontalGyrus.nii.gz'),
        os.path.abspath('../ROIs/lAG.nii.gz'),
        os.path.abspath('../ROIs/lIPS.nii.gz'),
        os.path.abspath('../ROIs/rIPS.nii.gz'),
        os.path.abspath('../ROIs/rLingual.nii.gz')]