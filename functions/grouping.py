import xarray as xr
import re

def group_over_n_dose(ds_count , group_over_n_dose = 2, doses_label = "Last COVID-19 dose number"):
    list_ds = []
    list_dose_categories = list(ds_count[doses_label].values)
    list_dose_categories_grouped = list(range(group_over_n_dose))

    # Before grouping doses
    for n in list_dose_categories_grouped:
        ds_count_n_dose = ds_count.sel({doses_label: n}).drop(
            doses_label
        )
        list_ds.append(ds_count_n_dose)

    # Adding grouped data
    list_dose_categories_grouped.append(f"{group_over_n_dose}+")
    list_grouped_doses = [
        n_dose for n_dose in list_dose_categories if n_dose >= group_over_n_dose
    ]
    ds_count_grouped_doses = ds_count.sel(
        {doses_label: list_grouped_doses}
    ).sum(dim=doses_label)
    list_ds.append(ds_count_grouped_doses)

    ds_count_grouped = xr.concat(list_ds, dim=doses_label)
    ds_count_grouped = ds_count_grouped.assign_coords(
        {doses_label: list_dose_categories_grouped}
    )
    return ds_count_grouped

def sort_age_categories(list_age_categories):
    list_age_categories.sort(key=lambda x: int(re.compile("\d+").search(x)[0]))

dict_age_groups = {#'<20':['12-15', '12-17', '16-19'],
 '21 to 40':['20-24', '25-29', '30-34', '35-39'],
  '41 to 60':['40-44', '45-49', '5-11', '50-54', '55-59'],
   '61 to 80':['60-64', '65-69', '70-74',
       '75-79'], 
       # '>80':['80-84', '85-89', '90+']
       }

def group_age_groups(ds, label = 'Age group'):
    """This function add a dimension to groupby energy groups"""
    list_age_groups = [key for key in dict_age_groups]
    ds = ds.rename({label: "Sub_Age_group"})
    ds = xr.concat(
        [
            ds.sel(Sub_Age_group=dict_age_groups[age_group])
            for age_group in list_age_groups
        ],
        dim=label.replace(' ','_'),
    )
    ds = ds.assign_coords(coords={label.replace(' ','_'): list_age_groups})
    return ds