
import os

from data import merging_all_datasets
from Polynomial_Regression import polynomial_regression
##from data import upload_data_bq

## print(os.path.dirname(os.path.dirname(__file__)))


polynomial_regression(merging_all_datasets, 'total target (wind, solar, hydro)')
