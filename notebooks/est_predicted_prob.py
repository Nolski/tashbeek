import numpy as np

from math import sqrt, log, pi
from scipy.optimize import fmin
from scipy.special import erf
from scipy.stats import norm

def ll(beta, y, x):
    pred_prob = norm.cdf(np.matmul(x, beta))

    pred_prob_log = np.log(pred_prob)
    inverse_y = (1 - y)
    inverse_log_pred_prob = np.log(1 - pred_prob)

    s = (y * pred_prob_log) + (inverse_y * inverse_log_pred_prob)
    loglikelihood = np.sum(s)

    sigma = 1
    npdf = norm.pdf(beta / sigma)

    return loglikelihood + np.sum(np.log(npdf))


def predicted_probability(y, x):
    guess = np.zeros((x.shape[1], 1))
    # Maximise the values for the logit
    betahat = fmin(lambda beta, y, x: -ll(beta, y, x), x0=guess, args=(y, x), maxiter=5000)
    return norm.cdf(np.matmul(x, betahat))
