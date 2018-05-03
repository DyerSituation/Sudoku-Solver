#!/usr/bin/env python
# coding:utf-8

"""
Usage:
$ python3 driver.py <81-digit-board>
$ python3 driver.py   => this assumes a 'sudokus_start.txt'

Saves output to output.txt
"""

import sys

ROW = "ABCDEFGHI"
COL = "123456789"
TIME_LIMIT = 20.  # max seconds per board
out_filename = 'output.txt'
src_filename = 'sudokus_start.txt'


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def string_to_board(s):
    """
        Helper function to convert a string to board dictionary.
        Scans board L to R, Up to Down.
    """
    return {ROW[r] + COL[c]: int(s[9 * r + c])
            for r in range(9) for c in range(9)}


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def write_solved(board, f_name=out_filename, mode='w+'):
    """
        Solve board and write to desired file, overwriting by default.
        Specify mode='a+' to append.
    """
    result = backtracking(board)
    print(result)  # TODO: Comment out prints when timing runs.
    print()

    # Write board to file
    outfile = open(f_name, mode)
    outfile.write(result)
    outfile.write('\n')
    outfile.close()

    return result

class CSP:
    def __init__(self, board):
        self.board = board
        self.unassigned = []
        for key, value in self.board.iteritems():
            if value == 0:
                self.unassigned.append(key)
        
    
def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    solved_board = board
    
    #make CSP
    csp = CSP(board)
    solved_board = helper(csp)
    print solved_board
    # time.sleep(5.)
    return board_to_string(solved_board)

def helper(csp):
    board = csp.board
    #check if complete
    if 0 not in board.values():
        return board
    var = selectUnassigned(csp)
    domain = getDomain(var, csp)
    for value in domain:
        #add value
        board[var] = value
        csp.board = board
        csp.unassigned.remove(var)
        result = helper(csp)
        if result != "fail":
            return result
        board[var] = 0
        csp.unassigned.append(var)
    return "fail" 

def selectUnassigned(csp):
    minVar = ""
    minD = sys.maxint
    for var in csp.unassigned:
        domain = getDomain(var, csp)
        if len(domain) < minD:
            minD = len(domain)
            minVar = var
    return minVar

def getDomain(var, csp):
    #TODO
    board = csp.board
    domain = [1,2,3,4,5,6,7,8,9]

    
    #row
        #letter
    for num in COL:
        index = var[0] + num
        seen = board[index]
        if seen in domain:
            domain.remove(seen)
        
    #column
        #number
    for c in ROW:
        index = c + var[1]
        seen = board[index]
        if seen in domain:
            domain.remove(seen)

    #square
        #abc, def, ghi. 123, 456, 789
        if var[0] in ROW[0:3]:
            squareRow = ROW[0:3]
            
        if var[0] in ROW[3:6]:
            squareRow = ROW[3:6]
            
        if var[0] in ROW[6:9]:
            squareRow = ROW[6:9]
            
        if var[1] in COL[0:3]:
            squareColumn = COL[0:3]
            
        if var[1] in COL[3:6]:
            squareColumn = COL[3:6]
            
        if var[1] in COL[6:9]:
            squareColumn = COL[6:9]
            
        for letter in squareRow:
            for number in squareColumn:
                index = letter + number
                seen = board[index]
                if seen in domain:
                    domain.remove(seen)
                
    return domain
        

    
if __name__ == '__main__':

    if len(sys.argv) > 1:  # Run a single board, as done during grading
        board = string_to_board(sys.argv[1])
        write_solved(board)

    else:
        print("Running all from sudokus_start")

        #  Read boards from source.
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation
            board = string_to_board(line)
            print_board(board)  # TODO: Comment this out when timing runs.

            # Append solved board to output.txt
            write_solved(board, mode='a+')

        print("Finished all boards in file.")