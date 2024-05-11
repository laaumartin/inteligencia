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

#step2 
for app in applications:
        print("Measurement for Application ID:", app.appId)
        for rule in rules:
            print("Rule:", rule.ruleName)
            # Calculate the fitness of the rule
            min_mem_degree = 1.0
            for antecedent_setid in rule.antecedent:
                antecedent_set = None
                if antecedent_setid in app.data:
                    antecedent_set = app.data[antecedent_setid]
                else:
                    antecedent_set = risk_fuzzy_sets.get(antecedent_setid) # esto no funciona lo del get 

                if antecedent_set:
                    mem_degree = antecedent_set.memDegree
                    print("Antecedent:", antecedent_setid, "Membership Degree:", mem_degree)
                    min_mem_degree = min(min_mem_degree, mem_degree)
                else:
                    print("Antecedent set not found:", antecedent_setid)

            # Calculate the fitness of the rule
            consequent_setid = rule.consequent
            consequent_set = None
            if consequent_setid in app.data:
                consequent_set = app.data[consequent_setid]

            if consequent_set:
                rule_fit = min_mem_degree * consequent_set.memDegree
                print("Rule Fit:", rule_fit)
            else:
                print("Consequent set not found:", consequent_setid)
        print()
