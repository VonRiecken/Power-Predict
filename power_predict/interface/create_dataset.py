from power_predict.logic.data import *

df = merging_all_datasets()

save_dataset_locally(df_to_save=df, dataset_name='merged_dataset')
