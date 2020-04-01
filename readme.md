# Models for Epidemics

I have made some models of epidemics in python just for dissemination purposes.
These are not based on actual data nor are validated. Just have been made
for my own purposes of understanding how the acutations of governments can
have a real impact on the spread of Covid-19 epidemics.

The code is based on pre-existing python example of [Modeling A Zombie Apocalypse](https://scipy-cookbook.readthedocs.io/items/Zombie_Apocalypse_ODEINT.html)

## Prerequisites

Python 3.x
Numpy  1.8.1
Scipy  1.3.2
Matplotlib 3.1.1


## SIR

Implements the well know Susceptible-Infected-Recovered model. That I know for
sure this model fits well to the early stages of the infection because has been
used by [Modelling Uncertainty Quantification](http://covid19.webs.upv.es/) group
for fitting the data from Spain and predict the peak of the epidemics.

```{python}
python modelo_sir.py
```

## SIRM

This model just adds a constant rate of deaths to the SIR model it doesn't affects
to the dynamics of the system.

```{python}
python modelo_sirm.py
```

## SIARM

In this model, just another group has been added that can spread the epidemics but
don't fall ill, I have named it *A* for **Asyntomatics**.

```{python}
python modelo_siarm.py
```

## Discreto

This model is a discrete state adaptation of the SIARM model to look for changes in
the dynamics due to the fact of considering the epidemics a continuous system instead
of a discrete system.

```{python}
python discreto.py
```

## Simula individuos

This model simulates an isolated village (by default with 1000 inhabitants) suffering
an outbreak, without restrictions of movements in the individuals 

```{python}
python simula_individuos.py
```

## Authors

* **Juanma Belda** - [Faking Physics](https://twitter.com/fakingphysics)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



