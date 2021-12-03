"""
Tests for pval module
"""

import unittest

import numpy as np
from sklearn.cluster import AgglomerativeClustering
# import matplotlib.pyplot as plt

from pval_module.stattests import stattest_clusters_approx
from pval_module.stattests import wald_test


class TestPvalModule(unittest.TestCase):
    """ Unittest class holding tests for pval module

    Args:
        None in addition to those inherited from unittest.Testcase
    Attributes:
        None in addition to those inherited from unittest.Testcase
    Methods:

    Functions:
    """

    def test_smoke_gao(self):
        """
        simple smoke test to make sure stattest_clusters_approx function runs
        :return: nothing
        """
        x = np.array([[5, 3],
                      [10, 15],
                      [15, 12],
                      [24, 10],
                      [30, 30],
                      [85, 70],
                      [71, 80],
                      [60, 78],
                      [70, 55],
                      [80, 91], ])
        k = 2
        cl_fun = AgglomerativeClustering
        positional_arguments = []
        keyword_arguments = {'n_clusters': k, 'affinity': 'euclidean',
                             'linkage': 'average'}
        cluster = cl_fun(*positional_arguments, **keyword_arguments)
        cluster.fit_predict(x)
        k1 = 0
        k2 = 1
        stattest_clusters_approx(x, k1, k2, cluster.labels_, cl_fun,
                                 positional_arguments, keyword_arguments, )
        self.assertTrue(True)


    def test_smoke_wald(self):
        """
        simple smoke test to make sure wald_test function runs
        :return: nothing
        """
        x = np.array([[5, 3],
                      [10, 15],
                      [15, 12],
                      [24, 10],
                      [30, 30],
                      [85, 70],
                      [71, 80],
                      [60, 78],
                      [70, 55],
                      [80, 91], ])
        k = 2
        cl_fun = AgglomerativeClustering
        positional_arguments = []
        keyword_arguments = {'n_clusters': k, 'affinity': 'euclidean',
                             'linkage': 'average'}
        cluster = cl_fun(*positional_arguments, **keyword_arguments)
        cluster.fit_predict(x)
        k1 = 0
        k2 = 1
        wald_test(x, k1, k2, cluster.labels_)
        self.assertTrue(True)


    def test_penguin_gao_10000(self):
        """
        One-shot test using Penguin data used in R tutorial with ndraws same
        as shown in R tutorial.
        :return: same results as when using R stattest_clusters_approx function:
        stat = 10.11433, stderr ~ .01084133, pval > .5
        """
        penguin_data = np.genfromtxt(
            'tests/data_for_tests/penguin_data_subset.txt',
            delimiter=' ', skip_header=1)
        k = 5
        # set linkage to average to match R script
        positional_arguments = []
        keyword_arguments = {'n_clusters': k, 'affinity': 'euclidean',
                             'linkage': 'average'}
        cluster = AgglomerativeClustering(**keyword_arguments)
        cluster.fit_predict(penguin_data)
        # flipped these axes to match figure in R
        # plt.scatter(penguin_data[:, 1], penguin_data[:, 0],
        # c=cluster.labels_, cmap='rainbow')
        # print (cluster.labels_)
        # plt.show()
        k1 = 0
        k2 = 1
        stat, pval, stderr = stattest_clusters_approx(penguin_data, k1, k2,
                                                      cluster.labels_,
                                                      AgglomerativeClustering,
                                                      positional_arguments,
                                                      keyword_arguments,
                                                      ndraws=10000)
        passing = True
        assert np.isclose(stat, 10.11433)
        try:
            assert np.isclose(stderr, 0.01084133, atol=.001)
        except AssertionError:
            passing = False
            print("stderr is {}, should be within .001 of "
                  "0.01084133".format(stderr))
        try:
            assert pval > .5
        except AssertionError:
            passing = False
            print("pval is {}, should be > .5".format(pval))
        self.assertTrue(passing)


    def test_penguin_wald(self):
        """
        One-shot test using Penguin data used in R tutorial
        :return: same results as shown when using R wald_test function,
        stat =  10.11433; pval = 0.006226331
        """
        penguin_data = np.genfromtxt(
            'tests/data_for_tests/penguin_data_subset.txt', delimiter=' ',
            skip_header=1)
        k = 5
        positional_arguments = []
        keyword_arguments = {'n_clusters': k, 'affinity': 'euclidean',
                             'linkage': 'average'}
        cluster = AgglomerativeClustering(*positional_arguments,
                                          **keyword_arguments)
        cluster.fit_predict(penguin_data)
        k1 = 0
        k2 = 1
        stat, pval = wald_test(penguin_data, k1, k2, cluster.labels_)
        assert np.isclose(stat, 10.11433)
        assert np.isclose(pval, 0.006226331)
        self.assertTrue(True)


    def test_penguin_gao_200(self):
        """
        One-shot test using Penguin data used in R tutorial with
        consistent parameters except ndraws=200 (to expedite function running
        while testing)
        :return: same results as when using R stattest_clusters_approx function:
        stat = 10.11433; stderr ~ .07; p > .3
        """
        penguin_data = np.genfromtxt(
            'tests/data_for_tests/penguin_data_subset.txt',
            delimiter=' ', skip_header=1)
        k = 5
        # set linkage to average to match R script
        positional_arguments = []
        keyword_arguments = {'n_clusters': k, 'affinity': 'euclidean',
                             'linkage': 'average'}
        cluster = AgglomerativeClustering(**keyword_arguments)
        cluster.fit_predict(penguin_data)
        k1 = 0
        k2 = 1
        stat, pval, stderr = stattest_clusters_approx(penguin_data, k1, k2,
                                                      cluster.labels_,
                                                      AgglomerativeClustering,
                                                      positional_arguments,
                                                      keyword_arguments,
                                                      ndraws=200)
        passing = True
        assert np.isclose(stat, 10.11433)
        try:
            assert np.isclose(stderr, 0.07, atol=.02)
        except AssertionError:
            passing = False
            print("stderr is {}, should be within .02 of "
                  "0.07".format(stderr))
        try:
            assert pval > .3
        except AssertionError:
            passing = False
            print("pval is {}, should be >.3".format(pval))
        self.assertTrue(passing)


    ###### GAO TESTS PERMUTING PARAMETERS
    def test_penguin_gao_isoFalse_sigNone_siginvNone_200(self):
        """
        One-shot test using Penguin data used in R tutorial with
        consistent parameters except iso is False, and ndraws=200 (to expedite
        function running while testing)
        :return: same results as when using R stattest_clusters_approx function:
        stat = 1.223436; stderr ~ .07; p > .3 (with ndraw=200 there can be a
        lot of variability here)
        """
        penguin_data = np.genfromtxt(
            'tests/data_for_tests/penguin_data_subset.txt',
            delimiter=' ', skip_header=1)
        k = 5
        # set linkage to average to match R script
        positional_arguments = []
        keyword_arguments = {'n_clusters': k, 'affinity': 'euclidean',
                             'linkage': 'average'}
        cluster = AgglomerativeClustering(**keyword_arguments)
        cluster.fit_predict(penguin_data)
        k1 = 0
        k2 = 1
        stat, pval, stderr = stattest_clusters_approx(penguin_data, k1, k2,
                                                      cluster.labels_,
                                                      AgglomerativeClustering,
                                                      positional_arguments,
                                                      keyword_arguments,
                                                      iso=False,
                                                      ndraws=200)
        passing = True
        assert np.isclose(stat, 1.223436)
        try:
            assert np.isclose(stderr, 0.07, atol=.03)
        except AssertionError:
            passing = False
            print("stderr is {}, should be within .03 of "
                  "0.07".format(stderr))
        try:
            assert pval > .3
        except AssertionError:
            passing = False
            print("pval is {}, should be greater than .3".format(pval))
        self.assertTrue(passing)


    def test_penguin_gao_isoFalse_sigNone_siginvqxqndarray_200(self):
        """
        One-shot test using Penguin data used in R tutorial with
        consistent parameters except iso is False, ndraws=200 (to expedite
        function running while testing), and siginv provided
        :return: same results as when using R stattest_clusters_approx function
        with these parameters:
        stat = 8.134167; stderr < .009; p < .05 (with ndraw=200 there can be a
        lot of variability here, these may be a bad stderr and pval thresholds)
        """
        penguin_data = np.genfromtxt(
            'tests/data_for_tests/penguin_data_subset.txt',
            delimiter=' ', skip_header=1)
        k = 5
        # set linkage to average to match R script
        positional_arguments = []
        keyword_arguments = {'n_clusters': k, 'affinity': 'euclidean',
                             'linkage': 'average'}
        cluster = AgglomerativeClustering(**keyword_arguments)
        cluster.fit_predict(penguin_data)
        k1 = 0
        k2 = 1
        siginv = np.array([[1, 1], [1, 1]])
        stat, pval, stderr = stattest_clusters_approx(penguin_data, k1, k2,
                                                      cluster.labels_,
                                                      AgglomerativeClustering,
                                                      positional_arguments,
                                                      keyword_arguments,
                                                      iso=False,
                                                      siginv=siginv,
                                                      ndraws=2000)
        passing = True
        assert np.isclose(stat, 8.134167)
        try:
            assert stderr < .009
        except AssertionError:
            passing = False
            print("stderr is {}, should be less than "
                  "0.009".format(stderr))
        try:
            assert pval < .05
        except AssertionError:
            passing = False
            print("pval is {}, should be less than .05".format(pval))
        self.assertTrue(passing)


    def test_penguin_gao_isoTrue_sig5_200(self):
        """
        One-shot test using Penguin data used in R tutorial with
        consistent parameters except ndraws=200 (to expedite function running
        while testing), and sig is 5
        :return: same results as when using R stattest_clusters_approx function
        with these parameters:
        stat = 10.11433; stderr < .1; p > .1 (with ndraw=200 there can be a
        lot of variability here, these may be a bad stderr and pval thresholds)
        """
        penguin_data = np.genfromtxt(
            'tests/data_for_tests/penguin_data_subset.txt',
            delimiter=' ', skip_header=1)
        k = 5
        # set linkage to average to match R script
        positional_arguments = []
        keyword_arguments = {'n_clusters': k, 'affinity': 'euclidean',
                             'linkage': 'average'}
        cluster = AgglomerativeClustering(**keyword_arguments)
        cluster.fit_predict(penguin_data)
        k1 = 0
        k2 = 1
        stat, pval, stderr = stattest_clusters_approx(penguin_data, k1, k2,
                                                      cluster.labels_,
                                                      AgglomerativeClustering,
                                                      positional_arguments,
                                                      keyword_arguments,
                                                      iso=True,
                                                      sig=5,
                                                      ndraws=200)
        passing = True
        assert np.isclose(stat, 10.11433)
        try:
            assert stderr < .1
        except AssertionError:
            passing = False
            print("stderr is {}, should be less than "
                  "0.1".format(stderr))
        try:
            assert pval > .1
        except AssertionError:
            passing = False
            print("pval is {}, should be greater than .1".format(pval))
        self.assertTrue(passing)


#sig only matters if iso is true

#siginv only matters is iso is false


#test that makes sure RuntimeError thrown if survives == 0 in
# stattest_clusters_approx (run with ndraws = 1)

