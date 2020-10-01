##Fantacy-League-Basketball-Performance-Pridiction

This is a work in progress.

## Summary

In this notebook, the ordinary least squares (OLS) method  will be used to estimate all parameters in a linear regression model. All relevant literature refers to this modeling method as "linear regression" and thus will be referred to as such here. 

This model utilizes (blank) features scraped from [basketball-reference.com](https://www.basketball-reference.com/)'s seasons tables ([totals](https://www.basketball-reference.com/leagues/NBA_2019_totals.html) and [advanced](https://www.basketball-reference.com/leagues/NBA_2019_advanced.html)) and predicts the total fantasy points a player will score the following year, otherwise referred to as __future_fantasy_points__ in the dataset. This metric was calculated following data collection according to [Yahoo's ruleset](https://help.yahoo.com/kb/fantasy-basketball/default-league-settings-fantasy-basketball-sln6919.html). 

It's interesting to note that every iteration of a player is considered separately. For example, 2012 LeBron James is a separate record from 2013 LeBron James. This is to say that 2012 LeBron James' __future_fantasy_points__ attribute is the same as his 2013 total fantasy points attribute, or __fantasy_points__ in the pre-processed data.

While around (blank) records were scraped from basketball-reference, only (blank) records exist in the processed dataset. Consider players who were in the league for only one season. These players do not have __future_fantasy_points__ to predict and thus were dropped during the data-processing phase. Of course, the 2018-2019 season was only used to compute __future_fantasy_points__ for 2017-2018 records. See a subset of the data below.

Note: All data used comes from seasons ending in (blank) to 2019.

(insert df preview)

## Linear Regression

The goal of a linear regression is always the same, in general, and that's to extract a random sample from a population and then to use that random sample to estimate the properties of the population. 

A good question to ask in terms of basketball and this model would be as follows: "By how much does a player's fantasy points next year change for each point scored the year before?" The answer to this question, the weight, is exactly what we're trying to optimize, along with the other (blank) features' weights. 

Below is the linear regression formula, where Y is __future_fantasy_points__ and, in accordance with the example above, $\beta_1$ is the weight attributed to points scored ($x_1$). 

\begin{equation*} Y = \beta_0 + \beta_1 * x_1 + \beta_2 * x_2  +  ...  +  \epsilon \end{equation*}

$\beta_0$, the intercept, and $\epsilon$, the random error, will both be touched on shortly.