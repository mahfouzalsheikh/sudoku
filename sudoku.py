import sys, getopt, datetime
from termcolor import colored
from time import sleep


# a function to print the game array
def printArray(array):
    print ""
    for row in array:
        string = []
        for item in row:
            if item==0:
                string.append(colored(str(item), 'white'))
            else:
                string.append(colored(str(item), 'green'))

        print '    '.join(string)
        print 
    print ""

# a fucntion to find the next cell to fill
def findNextEmptyCell(grid, i, j):
        # Try first with 
        for x in range(i,9):
                for y in range(j,9):
                        if grid[x][y] == 0:
                                return x,y
        for x in range(0,9):
                for y in range(0,9):
                        if grid[x][y] == 0:
                                return x,y
        return -1,-1

# a function to check if a value meets the constraints in i,j position 
def checkConstraints(grid, i, j, e):
        # check the row
        rowOk = all([e != grid[i][x] for x in range(9)])
        if rowOk:
                # check the columns
                columnOk = all([e != grid[x][j] for x in range(9)])
                if columnOk:
                        # check the 3 X 3 group the cell in
                        X = 3 *(i/3)
                        Y = 3 *(j/3)

                        for x in range(X, X+3):
                                for y in range(Y, Y+3):
                                        if grid[x][y] == e:
                                                return False
                        return True
        return False

# The backtracking function that solves the game
def solveSudoku(grid, i=0, j=0):
    i,j = findNextEmptyCell(grid, i, j)
    if i == -1:
            return True
    for e in range(1,10):
            if checkConstraints(grid,i,j,e):
                    grid[i][j] = e
                    if solveSudoku(grid, i, j):
                            return True
                    else:
                        # backtrack
                        grid[i][j] = 0
    return False


def main(argv):
    #### initialize the variables and read the user input 
    inputfile = ''
    outputfile = 'sudokupoutputfile.txt'
    try:
        opts, args = getopt.getopt(argv,"hi:o",[ "ifile=" , "ofile="])
    except getopt.GetoptError:
        print 'rollup.py -i <inputfile> -o <outputfile>'
        sys.exit(2)

    print opts   
    for opt, arg in opts:
        if opt == '-h':
            print 'rollup.py -i <inputfile> -o <outputfile> -c <comma separated column names>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    

    print "Input file is: ", inputfile
    print "Output file is:", outputfile

    
    #### read the content of the input file and find the headers of the table
    start_time  = datetime.datetime.now()

    with open(inputfile) as f:
        file_content = f.readlines()

    input_table = []


    for line in file_content:
        input_line = line.replace('\n','').split('\t')        
        input_line = [int(x) for x in input_line]
        input_table.append(input_line)
        


 
    #### run the rollup aggregation function on the input table and the input columns

    solveSudoku(input_table)
    
    printArray(input_table)
    #### writing the output to the output file 
    output_file  = open(outputfile, 'w')
    

    #### writing the rows in the output array to the output file


    for row in input_table:
        line = '\t'.join([str(x) for x in row]) +'\n'   
        output_file.write(line)
        #print row
    
    done_with = datetime.datetime.now() - start_time
    

    print "Done within:", done_with


if __name__ == "__main__":
    main(sys.argv[1:])







