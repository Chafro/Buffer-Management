import argparse
import time

'''Here an argument is taken from the command line for the name of the test file'''
parser = argparse.ArgumentParser()
parser.add_argument('--testfile')

''' Global variables used in functions'''
WT = True  # While True
NP = 0  # Number of Pages
FN = 0  # Function Number
TT = 0  # Total Ticks
BAP = 0  # Number of times buffer accessed for page
TBA = 0  # Total block accessed
HR = 0  # Hit Rate
BS = 4  # Buffer Size
BFS = 'F0'  # Best Frame
BP = []  # Buffer Pool format - [Frame#, Page#, FixCountWrite, FixCountRead, Dirty, Position/HitCount/Time]

'''Numbers assigned to each algorithm'''
Algors = {
    1: "Algorithm: Least Recently Used (LRU)",
    2: "Algorithm: Least Frequently Used (LFU)",
    3: "Algorithm: Most Frequently Used (MFU)",
    4: "Algorithm: First in First Out (FIFO)",
    5: "Algorithm: Least Recently Used (LRU) Clock Policy",
    6: "Algorithm: First in First Out (FIFO) Clock Policy"
}  # Algorithm Dictionary



'''This print_BP function is used to print the current pages in the buffer frames.'''
def print_BP():  # Print buffer pool
    print(Algors[FN])
    if FN == 1 or FN == 4:
        print("+---------+--------+------------------+-----------------+---------+----------+\n" +
              "| Frame # | Page # | Fix Count Writes | Fix Count Reads | Dirty ? | Position |\n" +
              "+---------+--------+------------------+-----------------+---------+----------+")
        for i in BP:
            print("|" + " " * (9 - len(str(i[0]))) + str(i[0]) + "|" + " " * (8 - len(str(i[1]))) + str(
                i[1]) + "|" + " " * (18 - len(str(i[2]))) + str(i[2]) + "|" + " " * (17 - len(str(i[3]))) + str(
                i[3]) + "|" + " " * (9 - len(str(i[4]))) + str(i[4]) + "|" + " " * (10 - len(str(i[5]))) + str(
                i[5]) + "|")
        print("+---------+--------+------------------+-----------------+---------+-----------+\n")

    elif FN == 2 or FN == 3:
        print("+---------+--------+------------------+-----------------+---------+-----------+\n" +
              "| Frame # | Page # | Fix Count Writes | Fix Count Reads | Dirty ? | Hit Count |\n" +
              "+---------+--------+------------------+-----------------+---------+-----------+")
        for i in BP:
            print("|" + " " * (9 - len(str(i[0]))) + str(i[0]) + "|" + " " * (8 - len(str(i[1]))) + str(
                i[1]) + "|" + " " * (18 - len(str(i[2]))) + str(i[2]) + "|" + " " * (17 - len(str(i[3]))) + str(
                i[3]) + "|" + " " * (9 - len(str(i[4]))) + str(i[4]) + "|" + " " * (11 - len(str(i[5]))) + str(
                i[5]) + "|")
        print("+---------+--------+------------------+-----------------+---------+-----------+\n")
    elif FN == 5 or FN == 6:
        print("+---------+--------+------------------+-----------------+---------+----------------------+\n" +
              "| Frame # | Page # | Fix Count Writes | Fix Count Reads | Dirty ? | Time In Nano Seconds |\n" +
              "+---------+--------+------------------+-----------------+---------+----------------------+")
        for i in BP:
            print("|" + " " * (9 - len(str(i[0]))) + str(i[0]) + "|" + " " * (8 - len(str(i[1]))) + str(
                i[1]) + "|" + " " * (18 - len(str(i[2]))) + str(i[2]) + "|" + " " * (17 - len(str(i[3]))) + str(
                i[3]) + "|" + " " * (9 - len(str(i[4]))) + str(i[4]) + "|" + " " * (22 - len(str(i[5]))) + str(
                i[5]) + "|")
        print("+---------+--------+------------------+-----------------+---------+----------------------+\n")


''' This pos Function update the postion of the frames in algorithm LRC and FIFO'''

def pos(pos):  # Increase or decrease the position of frames
    for i in BP:
        if pos >= i[5] and FN == 1:
            i[5] += 1
        if pos <= i[5] and FN == 4:
            i[5] -= 1


'''This buf Function places a new page in the best fit buffer frame based on the algorithm with a new page'''

def buf(fix, page_num, mode):  # Replace buffer frame with new page.
    global TT, BAP, BFS, TBA, FN
    TT += 10
    if (mode == 'write'):
        if (fix == 'fix'):
            if FN == 1 or FN == 2 or FN == 3:
                BP[BFS] = [BFS, page_num, 1, 0, 'y', 1]
            elif FN == 4:
                BP[BFS] = [BFS, page_num, 1, 0, 'y', len(BP)]
            elif FN == 5 or FN == 6:
                BP[BFS] = [BFS, page_num, 1, 0, 'y', time.time_ns()]
            TBA += 1
        else:
            return
    elif (mode == 'read'):
        if (fix == 'fix'):
            if FN == 1 or FN == 2 or FN == 3:
                BP[BFS] = [BFS, page_num, 0, 1, 'n', 1]
            elif FN == 4:
                BP[BFS] = [BFS, page_num, 0, 1, 'n', len(BP)]
            elif FN == 5 or FN == 6:
                BP[BFS] = [BFS, page_num, 0, 1, 'n', time.time_ns()]
            TBA += 1
        else:
            return


'''Function to added page to empty buffer'''
def add_page_empty_buffer(page_num,mode,fix):
    global TT, BAP, BFS, TBA, FN
    if (len(BP) == 0):
        if (mode == 'write'):
            if (fix == 'fix'):
                BP.append([0, page_num, 1, 0, 'y', 1])
                TBA += 1
                TT += 10
            else:
                return
        elif (mode == 'read'):
            if (fix == 'fix'):
                BP.append([0, page_num, 0, 1, 'n', 1])
                TBA += 1
                TT += 10
            else:
                return


'''Function to added page to empty buffer Clock policy'''
def add_page_empty_buffer_clock_policy(page_num,mode,fix):
    global TT, BAP, BFS, TBA, FN
    if (len(BP) == 0):
        if (mode == 'write'):
            if (fix == 'fix'):
                BP.append([0, page_num, 1, 0, 'y', time.time_ns()])
                TBA += 1
                TT += 10
            else:
                return
        elif (mode == 'read'):
            if (fix == 'fix'):
                BP.append([0, page_num, 0, 1, 'n', time.time_ns()])
                TBA += 1
                TT += 10
            else:
                return

''' Function to update pages in buffer'''

def fix_unfix_page_in_buffer(page_num,mode,fix):
    global TT, BAP, BFS, TBA, FN
    for i in BP:
        if (i[1] == page_num):
            if (mode == 'write'):
                if (fix == 'fix'):
                    i[2] += 1
                    if FN == 1:
                        if i[5] != 1 and FN == 1:
                            pos(i[5])
                        i[5] = 1
                    elif FN == 2 or FN == 3:
                        i[5] += 1
                    elif FN == 5:
                        i[5] = time.time_ns()
                    i[4] = 'y'
                    TBA += 1
                    BAP += 1
                    TT += 1
                elif (fix == 'unfix'):
                    if i[2] != 0:
                        i[2] -= 1
                    TT += 1

            elif (mode == 'read'):
                if (fix == 'fix'):
                    i[3] += 1
                    if FN == 1:
                        if i[5] != 1 and FN == 1:
                            pos(i[5])
                        i[5] = 1
                    elif FN == 2 or FN == 3:
                        i[5] += 1
                    elif FN == 5:
                        i[5] = time.time_ns()
                    TBA += 1
                    BAP += 1
                    TT += 1

                elif (fix == 'unfix'):
                    if i[3] != 0:
                        i[3] -= 1
                    TT += 1



'''Function to append new page in buffer if buffer not full'''
def buf_not_full(page_num,mode,fix):
    global TT, BAP, BFS, TBA, FN
    if (mode == 'write'):
        if (fix == 'fix'):
            if FN == 1:
                pos(len(BP))
            BP.append([len(BP), page_num, 1, 0, 'y', 1])
            TT += 10
            TBA += 1


        else:
            return
    elif (mode == 'read'):
        if (fix == 'fix'):
            if FN == 1:
                pos(len(BP))
            BP.append([len(BP), page_num, 0, 1, 'n', 1])
            TT += 10
            TBA += 1

        else:
            return


'''Function to append new page in buffer if buffer not full with time stamp'''
def buf_not_full_clock_policy(page_num,mode,fix):
    global TT, BAP, BFS, TBA, FN
    if (mode == 'write'):
        if (fix == 'fix'):
            BP.append([len(BP), page_num, 1, 0, 'y', time.time_ns()])
            TT += 10
            TBA += 1

        else:
            return
    elif (mode == 'read'):
        if (fix == 'fix'):
            BP.append([len(BP), page_num, 0, 1, 'n', time.time_ns()])
            TT += 10
            TBA += 1

        else:
            return

'''
This LRU function is and algorithm that replace the least recently used and available buffer frame with a new page base 
on the position the page is currently in. Positions of each frame are updated for every line that is read from the text 
file if the buffer with position 1 has changed.
'''

def LRU(fix, page_num, mode):  # Least recently used frame
    global TT, BAP, BFS, TBA

    # Condition states if the buffer is no full but has pages in it.
    if (len(BP) > 0 and len(BP) <= BS):

        # Condition states if page in buffer update buffer frame.
        if (page_num in [i[1] for i in BP]):
            fix_unfix_page_in_buffer(page_num,mode,fix)

        # Condition states if page not in buffer and buffer not full put page in buffer.
        elif (len(BP) < BS):
            buf_not_full(page_num, mode, fix)
        # Condition states if page not in buffer and buffer full find best frame to put the new page using LRU.
        else:
            for i in BP:
                if (i[2] == 0 and i[3] == 0):
                    if isinstance(BFS, str):
                        BFS = i[0]

                    elif isinstance(BFS, int):
                        if BP[BFS][5] < i[5]:
                            BFS = i[0]

            TT += 10
            if BFS != 'F0':
                if (BP[BFS][4] == 'y'):
                    TT += 10
                if BP[BFS][5] != 1:
                    pos(BP[BFS][5])
                buf(fix, page_num, mode)
                BFS = 'F0'

    # Condition states if buffer is empty put new page in buffer.
    add_page_empty_buffer(page_num,mode,fix)

    # print(BP)

''' 
This FU function is the base algorithm for the frequently used frame algorithms.
This function updates the usage records of each page in the frames.
'''

def FU(fix, page_num, mode):  # Frequently used frame
    global TT, BAP, BFS, TBA

    # Condition states if the buffer is no full but has pages in it.
    if (len(BP) > 0 and len(BP) <= BS):

        # Condition states if page in buffer update buffer frame.
        if (page_num in [i[1] for i in BP]):
            fix_unfix_page_in_buffer(page_num,mode,fix)

        # Condition states if page not in buffer and buffer not full put page in buffer.
        elif (len(BP) < BS):
            buf_not_full(page_num,mode,fix)

        # Condition states if page not in buffer and buffer full find best frame to put the new page using FU algorithms.
        else:
            if (FN == 2):
                LFU()
            elif (FN == 3):
                MFU()

            TT += 10

            if BFS != 'F0':
                if (BP[BFS][4] == 'y'):
                    TT += 10
                buf(fix, page_num, mode)
                BFS = 'F0'

    # Condition states if buffer is empty put new page in buffer.
    add_page_empty_buffer(page_num,mode,fix)
    # print(BP)

'''
This MFU function sorts the frames by most frequently used available frame and replaces the page inside the best frame 
with a new page.
'''
def MFU():  # Most Frequently used sort
    global TT
    global BFS
    for i in BP:
        if (i[2] == 0 and i[3] == 0):
            if isinstance(BFS, str):
                BFS = i[0]

            elif isinstance(BFS, int):
                if BP[BFS][5] < i[5]:
                    BFS = i[0]

'''
This MLFU function sorts the frames by least frequently used available frame and replaces the page inside the best frame 
with a new page.
'''
def LFU():  # Least Frequently used sort
    global TT
    global BFS
    for i in BP:
        if (i[2] == 0 and i[3] == 0):
            if isinstance(BFS, str):
                BFS = i[0]

            elif isinstance(BFS, int):
                if BP[BFS][5] > i[5]:
                    BFS = i[0]

'''
This FIFO function uses the first in first out rule to change the pages in the buffer pool. This function uses positions 
to keep track of the positions of the frame in the in queue and replace the first available best frame old page with a 
new page.
'''
def FIFO(fix, page_num, mode):  # First in First out frame
    global TT, BAP, BFS, TBA

    # Condition states if the buffer is no full but has pages in it.
    if (len(BP) > 0 and len(BP) <= BS):

        # Condition states if page in buffer update buffer frame.
        if (page_num in [i[1] for i in BP]):
            fix_unfix_page_in_buffer(page_num,mode,fix)

        # Condition states if page not in buffer and buffer not full put page in buffer.
        elif (len(BP) < BS):
            buf_not_full(page_num,mode,fix)

        # Condition states if page not in buffer and buffer full but page in buffer.
        else:
            for i in BP:
                if (i[2] == 0 and i[3] == 0):
                    if isinstance(BFS, str):
                        BFS = i[0]

                    elif isinstance(BFS, int):
                        if BP[BFS][5] > i[5]:
                            BFS = i[0]

            TT += 10
            if BFS != 'F0':
                if (BP[BFS][4] == 'y'):
                    TT += 10
                if BP[BFS][5] != BS:
                    pos(BP[BFS][5])
                buf(fix, page_num, mode)
                BFS = 'F0'
    else:
        # Condition states if buffer is empty put new page in buffer.
        add_page_empty_buffer(page_num,mode,fix)


''' 
Least Frequently Used algorithm using Clock Policy (LRUCP).
This function uses the same principle as the LRU but uses the system clock to keep track of the buffer frame's positions.
'''
def LRUCP(fix, page_num, mode):  # Least recently used frame using clock policy
    global TT, BAP, BFS, TBA

    # Condition states if the buffer is no full but has pages in it.
    if (len(BP) > 0 and len(BP) <= BS):

        # Condition states if page in buffer update buffer frame.
        if (page_num in [i[1] for i in BP]):
            fix_unfix_page_in_buffer(page_num,mode,fix)

        # Condition states if page not in buffer and buffer not full put page in buffer.
        elif (len(BP) < BS):
            buf_not_full_clock_policy(page_num, mode, fix)

        else:
            '''
            Condition states if page not in buffer and buffer full put page in best available buffer frame with the 
            lowest clock time.
            '''
            for i in BP:
                if (i[2] == 0 and i[3] == 0):
                    if isinstance(BFS, str):
                        BFS = i[0]

                    elif isinstance(BFS, int):
                        if BP[BFS][5] > i[5]:
                            BFS = i[0]

            TT += 10
            if BFS != 'F0':
                if (BP[BFS][4] == 'y'):
                    TT += 10
                buf(fix, page_num, mode)
                BFS = 'F0'

    # Condition states if buffer is empty put new page in buffer.
    add_page_empty_buffer_clock_policy(page_num,mode,fix)

    # print(BP)


def FIFOCP(fix, page_num, mode):  # First in First out frame using clock policy
    global TT, BAP, BFS, TBA

    # Condition states if the buffer is no full but has pages in it.
    if (len(BP) > 0 and len(BP) <= BS):

        # Condition states if page in buffer update buffer frame.
        if (page_num in [i[1] for i in BP]):
            fix_unfix_page_in_buffer(page_num,mode,fix)

        # Condition states if page not in buffer and buffer not full put page in buffer.
        elif (len(BP) < BS):
            buf_not_full_clock_policy(page_num,mode,fix)


        else:
            '''
            Condition states if page not in buffer and buffer full put page in best available buffer frame with the 
            lowest clock time.
            '''
            for i in BP:
                if (i[2] == 0 and i[3] == 0):
                    if isinstance(BFS, str):
                        BFS = i[0]

                    elif isinstance(BFS, int):
                        if BP[BFS][5] > i[5]:
                            BFS = i[0]

            TT += 10
            if BFS != 'F0':
                if (BP[BFS][4] == 'y'):
                    TT += 10
                buf(fix, page_num, mode)
                BFS = 'F0'

    # Condition states if buffer is empty put new page in buffer.
    add_page_empty_buffer_clock_policy(page_num,mode,fix)

''' Main function to start the alogorthims and read the test data. '''
if __name__ == '__main__':                          # Control Function
    start_time = time.time()                        # Start time to record the duration of the simulation.
    tfilen = parser.parse_args().testfile           # Taking file name from command line.
    tfile = open(tfilen, 'r')                       # Opening file.
    initsim = tfile.readline().strip().split(',')   # Reading first line of file.

    # print("running")
    # print(initsim)

    '''
    The first line of the file should have specific value for simulation to begin and this condition checks for the 
    init key word to start simulation with the buffer size, number of pages and number of the function to be used.
    '''
    if initsim[0] == 'init':
        BS = int(initsim[1])
        NP = int(initsim[2])
        FN = int(initsim[3])
        WT = True
        while WT:  # function runs until file has reach the end of file.
            fileln = tfile.readline().replace(" ", "")  # Removes spaces from the instruction.
            # print(fileln)

            # Condition to check if there is a line after the current line of instructions.
            if '\n' in fileln:
                fileln = fileln.strip().split(',') # separate file line into readable list.

                # Choose function to use base on function number.
                if FN == 1 and len(fileln) == 3 and int(fileln[1]) >= 0:
                    LRU(fileln[0], int(fileln[1]), fileln[2])
                elif (FN == 2 or FN == 3) and len(fileln) == 3 and int(fileln[1]) >= 0:
                    FU(fileln[0], int(fileln[1]), fileln[2])
                elif FN == 4 and len(fileln) == 3 and int(fileln[1]) >= 0:
                    FIFO(fileln[0], int(fileln[1]), fileln[2])
                elif FN == 5 and len(fileln) == 3 and int(fileln[1]) >= 0:
                    LRUCP(fileln[0], int(fileln[1]), fileln[2])
                elif FN == 6 and len(fileln) == 3 and int(fileln[1]) >= 0:
                    FIFOCP(fileln[0], int(fileln[1]), fileln[2])
            else:
                WT = False  # While condition changed to false since there are no next line symbols to in dicate a next instruction

                fileln = fileln.strip().split(',') # separate file line into readable list.

                # Choose function to use base on function number.
                if FN == 1 and len(fileln) == 3 and int(fileln[1]) >= 0:
                    LRU(fileln[0], int(fileln[1]), fileln[2])
                elif (FN == 2 or FN == 3) and len(fileln) == 3 and int(fileln[1]) >= 0:
                    FU(fileln[0], int(fileln[1]), fileln[2])
                elif FN == 4 and len(fileln) == 3 and int(fileln[1]) >= 0:
                    FIFO(fileln[0], int(fileln[1]), fileln[2])
                elif FN == 5 and len(fileln) == 3 and int(fileln[1]) >= 0:
                    LRUCP(fileln[0], int(fileln[1]), fileln[2])
                elif FN == 6 and len(fileln) == 3 and int(fileln[1]) >= 0:
                    FIFOCP(fileln[0], int(fileln[1]), fileln[2])

            #print_BP() # Print Current buffer frames
            # print(TT)

    '''Calculations for Report table'''
    if TBA != 0:
        HR = BAP / TBA
    OWC = 0
    ORC = 0
    for i in BP:
        OWC += i[2]
        ORC += i[3]

    '''Report Table for Simulation'''
    print("\n" + Algors[FN])
    print("Number of buffer references: " + str(BAP))
    print("Number of blocks Accessed: " + str(TBA))
    print("Outstanding Writes: " + str(OWC))
    print("Outstanding Reads: " + str(ORC))
    print('Total ticks consumed: ' + str(TT))
    print('Hit Rate: ' + str(HR))
    print("Time taken to run  %s seconds" % (time.time() - start_time))
