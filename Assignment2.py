import csv

def read_periodic_table(pt, file_name):    
    print "Reading the periodic table ..." 
    with open(file_name, "rb") as my_file:
        inputdata = csv.DictReader(my_file, delimiter=",")
        
        for row in inputdata:
            row["Atomic Mass"] = float(row["Atomic Mass"])
            row["Atomic Number"] = int(row["Atomic Number"])
            pt[row["Symbol"]] = row
#
# Read the rows of input data and store them in a dictionary
# You might want to convert the atomic mass and atomic number to
# integers right away.
#
    print
    print "Read %d elements from %s." % (len(pt), file_name)
    return


def read_known_solutions(known_solutions, file_name):    
    print "Reading known solutions ..." 
    with open(file_name,"rb") as my_file:
        inputdata = csv.DictReader(my_file, fieldnames=["String", "YesOrNo", "Solution", "Weight"], delimiter=",")

        for row in inputdata:
            row["YesOrNo"] = bool(row["YesOrNo"])
            row["Weight"] = float(row["Weight"])
            known_solutions[row["String"]] = (row["YesOrNo"], row["Solution"], row["Weight"])
#
# Store known solutions in the csv file into the know_solutions dictionary
# Note that known_solutions["O"] should be something like (True, "O", 16)
# You might have to convert the string "True" to True and weight to a
# floating point number
# 
    print "Read %d solutions from %s." % (len(known_solutions), file_name)
    print
    return

#
#  This function writes the known solutions into th file knownsolutions.csv
#


def write_known_solutions(known_solutions, file_name):    

    with open(file_name, "wb") as my_file:
        solution_writer = csv.writer(my_file, delimiter=",")
        for str in known_solutions:
            row =  known_solutions[str]
            solution_writer.writerow([str, row[0], row[1], row[2]])

    print len(known_solutions), "solutions saved in", "knownsolutions.csv"
    return



def mumkin(str):
    global number_of_calls
    number_of_calls += 1

    if str.lower() in known_solutions:
        if (known_solutions[str.lower()][2]) != 0:
            return known_solutions[str.lower()] 
        else:
            return (False, str, 0)
        
    if len(str) == 0:
        return (True, "", 0)
    

# Intialize is_possible, current_best_wt and current_best_sol

    is_possible = False
    current_best_wt = 0
    current_best_sol = str

    for ell in [3, 2, 1]:
#        print "trying ell= %d" % ell
#        print "str=%s, is_possible= %s, wt = %f, sol= %s" % (str, (is_possible), current_best_wt, current_best_sol)

        if len(str) >= ell and str[:ell].capitalize() in pt:
            (hai_mumkin, solution, his_weight) = mumkin(str[ell:])
            

            if hai_mumkin:
                is_possible = True
                my_weight = (his_weight + pt[str[:ell].capitalize()]["Atomic Mass"])
                
                if my_weight >= current_best_wt:
                    is_possible = True
                    current_best_wt = my_weight
                    current_best_sol = str[:ell].capitalize() + solution

            known_solutions[str] = [is_possible, current_best_sol, current_best_wt]
                    

# Update current_best_wt and current_best_sol
                    
# Where should you update know_solutions
#
    return (is_possible, current_best_sol, current_best_wt)

#
#
#

pt = {}
read_periodic_table(pt, "periodictable.csv")

known_solutions = {}
read_known_solutions(known_solutions, "knownsolutions.csv")

while True:
    str = raw_input("Enter a string: ")
    if str == "": break

    number_of_calls = 0
   
    (yes_or_no, solution, weight) = mumkin(str)

    if yes_or_no:
       print "Solution (and net molar mass) = (%s, %f a.u.)" % (solution, weight)
    else:
        print "Sorry!"

    print "Number of calls =", number_of_calls
    print

write_known_solutions(known_solutions,"knownsolutions.csv")
