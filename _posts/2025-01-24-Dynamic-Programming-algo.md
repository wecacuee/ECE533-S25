---
layout: post
title: "The Dynamic Programming algorithms"
date: 2025-01-23 00:00
categories: lecture
---

In this course, we are reading [Bertsekas' RL book](https://web.mit.edu/dimitrib/www/RLCOURSECOMPLETE.pdf) 11 pages at a time.

The book starts by referring to the recent advances in the RL, especially
AlphaGo and AlphaZero. Even more recent development is the that 
DeepMind founder, Demis Hassabis, won 2024 Nobel prize in Chemistry for his
contributions to AlphaFold2, an RL algorithm for predicting protein folding.

<img src="https://www.nobelprize.org/images/165765-portrait-mini-2x.jpg"
height="200px" />

To understand [AlphaGo which came out in 2016](https://www.nature.com/articles/nature16961), here's nice clip from [the movie with the same name](https://www.youtube.com/watch?v=WXuK6gekU1Y&start=2831)

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/WXuK6gekU1Y?si=lzOocxPjO42aqDEy&amp;start=2831" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

##### Two stages: Offline training and online play
![]("{{site.baseurl}}/assets/2025-01-23-offline-online.png"){:width="600px"/>

##### Policy network and value Network
<img src="{{site.baseurl}}/assets/2025-01-23-two.png" width="600px"/>

##### Policy evaluation and policy improvement
<img src="{{site.baseurl}}/assets/2025-01-23-fig-1.1.1.png" width="600px"/>

##### Offline training and Online play 

<img src="{{site.baseurl}}/assets/2025-01-23-fig-1.1.2.png" width="600px"/>

##### Alternative names of RL

Approximations in the value space, also known as *approximate dynamic
programming* or *neuro-dynamic programming*. *Reinforcement learning* includes
both approximations in the value space and in the policy space.
This can be used in control theory as *model predictive control*

## 1.2.1 Finite Horizon Problem Formulation

<img src="{{site.baseurl}}/assets/2025-01-23-fig-1.2.1.png" />

The *cost to go* is defined as the summation of step cost $g_k(x_k, u_k)$ with a
*terminal cost* $g_N(x_N)$.

\begin{align}
J(x_0; u_0, \dots, u_{N-1}) &= g_N(x_N) + \sum_{k=0}^{N-1} g_k(x_k, u_k), \\
& x_{k+1} &= f_k(x_k, u_k)
\end{align}

We want to minimize the cost over all sequences $\{u_0,\dots, u_{N-1}\}$ to
find the optimal cost-to-go of $x_0$,
\begin{align}
J^*(x_0) =  \min_{u_k, k \in [0, \dots, N-1]} J(x_0; u_0, \dots, u_{N-1})
\end{align}


<img src="{{site.baseurl}}/assets/2025-01-23-fig-1.2.2.png" />

<img src="{{site.baseurl}}/assets/2025-01-23-fig-1.2.3.png" />
