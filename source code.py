from MFIS_Read_Functions import *

#Saving the input variables as all the fuzzy sets in a fuzzy-set-dictionary

fuzzy_sets = readFuzzySetsFile('InputVarSets.txt')

#Saving all the applications we need to evaluate in a list

applications = readApplicationsFile()


#Split the fuzzy sets in the dictionary and evaluate each of the applications in the corresponding set

for setId, fuzzy_set in fuzzy_sets.items():

    # STEP1: FUZZIFICATION
    for app in applications:
        for var_label, value in app.data:
            if var_label == fuzzy_set.var:
                fuzzy_set.memDegree = skf.interp_membership(fuzzy_set.x, fuzzy_set.y, value)
                print(fuzzy_set.memDegree)


