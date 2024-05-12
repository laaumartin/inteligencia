from MFIS_Read_Functions import *
import skfuzzy as fuzz

Inputsets = readFuzzySetsFile('Files/InputVarSets.txt')
Risksets = readFuzzySetsFile('Files/Risks.txt')
rules = readRulesFile()
applications = readApplicationsFile()

# Split the fuzzy sets in the dictionary and evaluate each of the applications in the corresponding set
for app in applications:

    # STEP1: FUZZIFICATION
    for setId, fuzzy_set in Inputsets.items():
        # print(setId)
        for var_label, value in app.data:
            if var_label == fuzzy_set.var:
                fuzzy_set.memDegree = skf.interp_membership(fuzzy_set.x, fuzzy_set.y, value)
                # print(fuzzy_set.memDegree)

    # STEP2: RULE EVALUATION
    # print("Measurement for Application ID:", app.appId)
    risk_functions = []
    for rule in rules:
        # print("Rule:", rule.ruleName)
        antecedent_result = []  # here we store membership degree of each antecedent
        for antecedent_setid in rule.antecedent:  # taking the antecedents 1 by 1
            for setId, fuzzy_set in Inputsets.items():
                if antecedent_setid == setId:
                    antecedent_result.append(fuzzy_set.memDegree)
        # print("Antecedent: ", antecedent_result)
        # Let's compute similarity degree ==  evaluate the conjunction of the rule antecedents (min)
        min_memDegree = 1
        for ant_memDegree in antecedent_result:
            if ant_memDegree < min_memDegree:
                min_memDegree = ant_memDegree
        similarity_degree = min_memDegree
        # Now let's cut the consequent membership function at the level of the antecedent degree
        for setId, riskset in Risksets.items():
            if setId == rule.consequent:
                consequent_result = [rule.consequent, similarity_degree]
                # print(consequent_result)
                # using clipping
                conseq_membership_function = np.fmin(riskset.y, similarity_degree)
                risk_functions.append(conseq_membership_function)

    # STEP3: COMPOSITION
    # Now we unificate the output of all the rules, using aggregation
    max_result_function = risk_functions[0]
    for function in risk_functions:
        max_result_function = np.fmax(function, max_result_function)

    # Get the output variable range
    x_output = []
    for setId, riskset in Risksets.items():
        x_output = riskset.x

    # Plot the aggregated membership function
    #plt.plot(x_output, max_result_function)
    #plt.xlabel('Output Variable')
    #plt.ylabel('Membership Degree')
    #plt.title('Aggregated Risk Level')
    #plt.show()

    # STEP4: DEFUZZIFICATION
    # Now we need to get the centroid of the aggregated membership function
    centroid = fuzz.defuzz(x_output, max_result_function, 'centroid')

    # Calculate the membership degree for each risk label using the centroid value and save in "Results.txt"
    with open("Files/Results.txt", "a") as file:
        final_risk = None
        file.write(f"[Application {app.appId}]")
        for setId, riskset in Risksets.items():
            riskset.memDegree = skf.interp_membership(riskset.x, riskset.y, centroid)
            # write the results in the file
            file.write(f" {riskset.label} : {riskset.memDegree}\t")
        file.write(f"\n")


