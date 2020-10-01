import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


def recursive_vif_optimizer(df):

    go = True
    while go:
        x = df.iloc[:,:-1]
        x_1 = x
        x_1 = sm.add_constant(x_1)
        vif = [variance_inflation_factor(x_1.values, i) for i in range(x_1.shape[1])]
        vif = pd.DataFrame({'vif':vif[1:]}, index=x.columns)
        max_vif = vif.max().values[0]
        if max_vif > 5:
            column_to_drop = vif.idxmax()[0]
            df = df.drop(columns=[column_to_drop])
            go = True
        else:
            go = False
            print('Multicollinearity has been reduced.')
        
    return df


def backward_elimination(df):

    x = df.iloc[:,:-1]
    y = df['future_fantasy_points']

    columns = list(x.columns)

    while len(columns) > 0:
        
        x_1 = x[columns]
        x_1 = sm.add_constant(x_1)

        model = sm.OLS(y, x_1).fit()
        p = pd.Series(model.pvalues.values[1:], index=columns)
        
        pmax = max(p)
        features_with_p_max = p.idxmax()

        if pmax > 0.05:
            columns.remove(features_with_p_max)
        else:
            print('All variables are significant.')
            columns.append('future_fantasy_points')
            break

    return df[columns]
